-- fle_runtime: makes FLE's injected Lua survive save/load and multiplayer joins.
--
-- FLE defines its tools by sending Lua over RCON that stores functions in
-- `storage` (storage.actions, storage.utils, ...). Factorio cannot serialize
-- functions, so the first save fails, and a client joining a multiplayer game
-- (which loads a fresh save) never sees the injected code and desyncs.
--
-- A scenario that includes this file (`require("fle_runtime")` from its
-- control.lua and add it as an event_handler lib, or call the hooks directly)
-- changes that:
--   * fle_runtime.exec(name, source) records the source in storage (strings
--     serialize fine) and runs it with `storage` bound to a proxy. Function
--     values written through the proxy go to a non-persisted table; data goes
--     through to the real storage.
--   * on_load replays every recorded source in order, rebuilding the functions
--     on the server and on every joining client alike. Data writes are dropped
--     during replay because the data is already in the save.
--   * script.on_event / script.on_nth_tick calls made by FLE code are
--     multiplexed with the scenario's own handlers instead of replacing them.
--
-- RCON commands must resolve `storage` through fle_runtime.storage; the
-- Python side does this when it detects the `fle_runtime` global.

local runtime = {
  fns = {}, -- non-persisted: function-valued storage keys (actions, utils, ...)
  replaying = false,
  replay_errors = {}, -- name -> error message from the last on_load replay
  current_source = nil, -- name of the script being run (owner of handlers it registers)
  event_handlers = {}, -- event id -> ordered list of {source, fn}
  base_handlers = {}, -- event id -> scenario handler captured before FLE's (or false)
  nth_handlers = {}, -- tick period -> ordered list of {source, fn}
}

-- Keys whose tables hold functions. Anything assigned a function value is
-- routed to `fns` as well.
local FUNCTION_TABLES = { actions = true, utils = true }

local storage_proxy = setmetatable({}, {
  __index = function(_, key)
    local fn = runtime.fns[key]
    if fn ~= nil then
      return fn
    end
    return storage[key]
  end,
  __newindex = function(_, key, value)
    if FUNCTION_TABLES[key] or type(value) == "function" then
      runtime.fns[key] = value
    elseif not runtime.replaying then
      storage[key] = value
    end
  end,
  __pairs = function()
    return next, storage, nil
  end,
})

-- Handlers are kept per source script, so several scripts can listen to the
-- same event (in the order they were first registered) and re-sending a
-- script replaces only its own handler.
local function set_handler(list, source, fn)
  for i, entry in ipairs(list) do
    if entry.source == source then
      if fn then
        entry.fn = fn
      else
        table.remove(list, i)
      end
      return
    end
  end
  if fn then
    list[#list + 1] = { source = source, fn = fn }
  end
end

-- An error in an event handler ends the whole game ("non-recoverable error"),
-- so injected handlers run protected: a failure is recorded in
-- storage.fle_runtime.handler_errors (source -> {message, tick, count}) and the
-- other handlers still run. pcall is deterministic, so clients stay in sync.
local function call_handler(entry, event)
  local ok, err = pcall(entry.fn, event)
  if ok then
    return
  end
  local store = storage.fle_runtime
  store.handler_errors = store.handler_errors or {}
  local record = store.handler_errors[entry.source]
  if record then
    record.count = record.count + 1
    record.message = tostring(err)
    record.tick = event.tick
  else
    store.handler_errors[entry.source] = { message = tostring(err), tick = event.tick, count = 1 }
  end
end

local function dispatch_event(event)
  local base = runtime.base_handlers[event.name]
  if base then
    base(event)
  end
  local list = runtime.event_handlers[event.name]
  if list then
    for _, entry in ipairs(list) do
      call_handler(entry, event)
    end
  end
end

local function dispatch_nth(event)
  local list = runtime.nth_handlers[event.nth_tick]
  if list then
    for _, entry in ipairs(list) do
      call_handler(entry, event)
    end
  end
end

local function register_event(event, handler, filters)
  local list = runtime.event_handlers[event] or {}
  runtime.event_handlers[event] = list
  if runtime.base_handlers[event] == nil then
    runtime.base_handlers[event] = script.get_event_handler(event) or false
  end
  set_handler(list, runtime.current_source or "?", handler)
  if #list > 0 or runtime.base_handlers[event] then
    script.on_event(event, dispatch_event, filters)
  else
    script.on_event(event, nil)
  end
end

local function register_nth(tick, handler)
  local list = runtime.nth_handlers[tick] or {}
  runtime.nth_handlers[tick] = list
  set_handler(list, runtime.current_source or "?", handler)
  script.on_nth_tick(tick, #list > 0 and dispatch_nth or nil)
end

-- `script` as seen by FLE code: event registration is multiplexed, the rest
-- is forwarded to the real LuaBootstrap. Scenario code must not use
-- on_nth_tick periods that injected scripts use (they would replace it).
local script_proxy = setmetatable({
  on_event = function(event, handler, filters)
    if type(event) == "table" then
      for _, e in pairs(event) do
        register_event(e, handler)
      end
      return
    end
    register_event(event, handler, filters)
  end,
  on_nth_tick = function(tick, handler)
    if tick == nil then
      -- Clear only the calling script's periodic handlers.
      for period, _ in pairs(runtime.nth_handlers) do
        register_nth(period, nil)
      end
      return
    end
    if type(tick) == "table" then
      for _, t in pairs(tick) do
        register_nth(t, handler)
      end
      return
    end
    register_nth(tick, handler)
  end,
}, { __index = function(_, key) return script[key] end })

local env = setmetatable({ storage = storage_proxy, script = script_proxy }, { __index = _ENV, __newindex = _ENV })

local function run(name, source)
  local chunk, err = load(source, "=" .. name, "t", env)
  if not chunk then
    error("fle_runtime: cannot load " .. name .. ": " .. err)
  end
  local previous = runtime.current_source
  runtime.current_source = name
  local ok, run_err = pcall(chunk)
  runtime.current_source = previous
  if not ok then
    error(run_err, 0)
  end
end

local lib = {}

--- Record `source` under `name` and run it. Re-sending a name replaces it.
function lib.exec(name, source)
  -- A save made before the scenario gained the runtime never ran on_init.
  storage.fle_runtime = storage.fle_runtime or { sources = {}, order = {} }
  local store = storage.fle_runtime
  -- Record only sources that ran: a failing chunk would otherwise be
  -- replayed, and fail again, on every load. run() re-raises the error.
  run(name, source)
  if not store.sources[name] then
    store.order[#store.order + 1] = name
  end
  store.sources[name] = source
end

--- Forget every recorded source (e.g. before a full tool reload).
function lib.reset()
  storage.fle_runtime = { sources = {}, order = {} }
  runtime.fns = {}
end

--- Sources whose replay failed during the last on_load, as name -> error.
function lib.replay_errors()
  return runtime.replay_errors
end

--- Errors raised by injected event handlers, as source -> {message, tick, count}.
function lib.handler_errors()
  local store = storage.fle_runtime
  return store and store.handler_errors or {}
end

--- Forget recorded handler errors (after they have been reported).
function lib.clear_handler_errors()
  if storage.fle_runtime then
    storage.fle_runtime.handler_errors = nil
  end
end

--- Registered injected handlers, as {[event id or "nth:<period>"] = {source, ...}}.
function lib.handlers()
  local out = {}
  for event, list in pairs(runtime.event_handlers) do
    local names = {}
    for _, entry in ipairs(list) do
      names[#names + 1] = entry.source
    end
    out[event] = names
  end
  for tick, list in pairs(runtime.nth_handlers) do
    local names = {}
    for _, entry in ipairs(list) do
      names[#names + 1] = entry.source
    end
    out["nth:" .. tick] = names
  end
  return out
end

lib.storage = storage_proxy
lib.env = env

lib.on_init = function()
  storage.fle_runtime = storage.fle_runtime or { sources = {}, order = {} }
end

lib.on_configuration_changed = lib.on_init

lib.on_load = function()
  local store = storage.fle_runtime
  if not store then
    return
  end
  runtime.replaying = true
  runtime.replay_errors = {}
  for _, name in ipairs(store.order) do
    -- Top-level side effects that need `game` cannot run in on_load. A failed
    -- chunk keeps whatever it defined before the error; the Python side
    -- re-injects it live (see replay_errors). Sources should be replay-safe.
    local ok, err = pcall(run, name, store.sources[name])
    if not ok then
      runtime.replay_errors[name] = tostring(err)
    end
  end
  runtime.replaying = false
end

-- Console commands (/c, /sc) run in the level environment, so FLE's Python
-- side reaches the runtime through this global.
fle_runtime = lib

return lib
