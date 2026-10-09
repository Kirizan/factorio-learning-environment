"""Support for scenarios that embed fle_runtime.lua (persistent injected Lua).

See fle_runtime.lua for the why. This module wraps the RCON client so that,
when the running scenario provides the `fle_runtime` global:

* console commands resolve `storage` through the runtime's proxy, so
  `storage.actions.<tool>` finds the non-persisted function tables, and
* scripts are injected with `fle_runtime.exec(name, source)` so they are
  recorded in the save and replayed on load.

Without the global, every call passes through unchanged.
"""

from __future__ import annotations

import re
from pathlib import Path

RUNTIME_LUA = Path(__file__).with_name("fle_runtime.lua")

_LUA_COMMAND = re.compile(r"^/(sc|c|silent-command|command)\s", re.IGNORECASE)
_STORAGE_PREFIX = "local storage = fle_runtime.storage "


def long_bracket(source: str) -> str:
    """Quote `source` as a Lua long string that cannot be closed early."""
    level = 0
    # The closing bracket must not appear inside, nor form across the end (source ending in "]").
    while f"]{'=' * level}]" in source + "]":
        level += 1
    eq = "=" * level
    # A leading newline after [[ is dropped by Lua, so add one to keep it.
    return f"[{eq}[\n{source}]{eq}]"


def exec_command(name: str, source: str) -> str:
    return f"/sc fle_runtime.exec({long_bracket(name)}, {long_bracket(source)})"


class RuntimeAwareRCON:
    """Delegating wrapper around factorio_rcon.RCONClient."""

    def __init__(self, client):
        self._client = client
        self._has_runtime: bool | None = None

    def __getattr__(self, name):
        return getattr(self._client, name)

    @property
    def has_runtime(self) -> bool:
        if self._has_runtime is None:
            try:
                response = self._client.send_command(
                    "/sc rcon.print(tostring(fle_runtime ~= nil))"
                )
            except Exception:
                return False
            self._has_runtime = (response or "").strip() == "true"
        return self._has_runtime

    def rewrite(self, command: str) -> str:
        if not self.has_runtime:
            return command
        match = _LUA_COMMAND.match(command)
        if not match:
            return command
        return command[: match.end()] + _STORAGE_PREFIX + command[match.end() :]

    def send_command(self, command: str):
        return self._client.send_command(self.rewrite(command))

    def send_commands(self, commands: dict):
        return self._client.send_commands(
            {key: self.rewrite(cmd) for key, cmd in commands.items()}
        )

    def inject(self, name: str, source: str, prefix: str = "/sc"):
        """Send a Lua script that defines functions or registers handlers."""
        if self.has_runtime:
            return self._client.send_command(exec_command(name, source))
        return self._client.send_command(f"{prefix} {source}")
