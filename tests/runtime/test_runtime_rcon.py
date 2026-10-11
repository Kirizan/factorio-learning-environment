"""Unit tests for fle.env.runtime (no Factorio server needed)."""

from fle.env.runtime import RuntimeAwareRCON, exec_command, long_bracket


class FakeClient:
    def __init__(self, has_runtime: bool):
        self.has_runtime = has_runtime
        self.sent = []

    def send_command(self, command):
        self.sent.append(command)
        if command.startswith("/sc rcon.print(tostring(fle_runtime"):
            return "true" if self.has_runtime else "false"
        return ""

    def send_commands(self, commands):
        return {k: self.send_command(v) for k, v in commands.items()}


def test_long_bracket_cannot_be_closed_early():
    assert long_bracket("a") == "[[\na]]"
    assert long_bracket("x]]y") == "[=[\nx]]y]=]"
    assert long_bracket("x]]y]=]z") == "[==[\nx]]y]=]z]==]"
    # A trailing "]" would merge with the closing bracket.
    assert long_bracket("t[1]") == "[=[\nt[1]]=]"


def test_exec_command_quotes_name_and_source():
    assert exec_command("agent/x.lua", "storage.actions.x = 1") == (
        "/sc fle_runtime.exec([[\nagent/x.lua]], [[\nstorage.actions.x = 1]])"
    )


def test_rewrite_binds_storage_only_for_lua_commands_when_runtime_present():
    client = FakeClient(has_runtime=True)
    rcon = RuntimeAwareRCON(client)
    rcon.send_command("/sc rcon.print(1)")
    rcon.send_command("/silent-command a = 1")
    rcon.send_command("/server-save x")
    assert client.sent[1:] == [
        "/sc local storage = fle_runtime.storage rcon.print(1)",
        "/silent-command local storage = fle_runtime.storage a = 1",
        "/server-save x",
    ]


def test_passthrough_without_runtime():
    client = FakeClient(has_runtime=False)
    rcon = RuntimeAwareRCON(client)
    rcon.send_command("/sc rcon.print(1)")
    rcon.inject("agent/x.lua", "storage.actions.x = 1", prefix="/c")
    assert client.sent[1:] == ["/sc rcon.print(1)", "/c storage.actions.x = 1"]


def test_inject_uses_exec_with_runtime():
    client = FakeClient(has_runtime=True)
    RuntimeAwareRCON(client).inject("n", "src")
    assert client.sent[-1] == "/sc fle_runtime.exec([[\nn]], [[\nsrc]])"
