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
  event_handlers = {}, -- event id -> FLE handler
  base_handlers = {}, -- event id -> scenario handler captured before FLE's
  nth_handlers = {}, -- tick period -> FLE handler
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

local function dispatch_event(event)
  local base = runtime.base_handlers[event.name]
  if base then
    base(event)
  end
  local handler = runtime.event_handlers[event.name]
  if handler then
    handler(event)
  end
end

-- `script` as seen by FLE code: event registration is multiplexed, the rest
-- is forwarded to the real LuaBootstrap.
local script_proxy = setmetatable({
  on_event = function(event, handler, filters)
    if type(event) == "table" then
      for _, e in pairs(event) do
        runtime.event_handlers[e] = handler
        if runtime.base_handlers[e] == nil then
          runtime.base_handlers[e] = script.get_event_handler(e) or false
        end
        script.on_event(e, dispatch_event)
      end
      return
    end
    runtime.event_handlers[event] = handler
    if runtime.base_handlers[event] == nil then
      runtime.base_handlers[event] = script.get_event_handler(event) or false
    end
    script.on_event(event, dispatch_event, filters)
  end,
  on_nth_tick = function(tick, handler)
    -- Scenario libs must not use on_nth_tick periods FLE uses; FLE owns them.
    if type(tick) == "table" then
      for _, t in pairs(tick) do
        runtime.nth_handlers[t] = handler
        script.on_nth_tick(t, handler)
      end
      return
    end
    if tick == nil then
      script.on_nth_tick(nil)
      runtime.nth_handlers = {}
      return
    end
    runtime.nth_handlers[tick] = handler
    script.on_nth_tick(tick, handler)
  end,
}, { __index = function(_, key) return script[key] end })

-- Globals the scripts define (e.g. FLE's `dump`) land in the level environment
-- so console commands see them; only `storage` and `script` are overridden.
local env = setmetatable({ storage = storage_proxy, script = script_proxy }, { __index = _ENV, __newindex = _ENV })

local function run(name, source)
  local chunk, err = load(source, "=" .. name, "t", env)
  if not chunk then
    error("fle_runtime: cannot load " .. name .. ": " .. err)
  end
  chunk()
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
