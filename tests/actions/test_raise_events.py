"""Agent tools tell other mods what they change.

Placing raises script_raised_built, picking up script_raised_destroy, and
in-place changes (rotation, recipe) raise script_raised_teleported with an
unchanged position (Factorio has no raisable "changed" event). A recorder or
any other mod listening to these events then sees everything the agent does.
"""

import pytest

from fle.env.entities import Direction, Position
from fle.env.game_types import Prototype

EVENTS = ("script_raised_built", "script_raised_destroy", "script_raised_teleported")


def lua(instance, code: str) -> str:
    return instance.rcon_client.send_command(f"/sc {code}")


@pytest.fixture()
def raised(instance):
    """Record raised events as 'event:entity-name' lines in a global log."""
    events = ", ".join(f"defines.events.{e}" for e in EVENTS)
    lua(
        instance,
        "fle_test_raised = {} "
        f"script.on_event({{{events}}}, function(e) "
        "local name = e.entity and e.entity.valid and e.entity.name or '?' "
        "local p = e.entity and e.entity.valid and e.entity.position "
        "local same = e.old_position and p and e.old_position.x == p.x "
        "and e.old_position.y == p.y "
        "table.insert(fle_test_raised, e.name .. ':' .. name .. (same and ':same' or '')) end)",
    )

    def read() -> list[str]:
        raw = lua(instance, "rcon.print(table.concat(fle_test_raised, ','))") or ""
        names = {
            str(int(v)): k
            for k, v in ((e, lua(instance, f"rcon.print(defines.events.{e})")) for e in EVENTS)
        }
        out = []
        for item in filter(None, raw.strip().split(",")):
            event, _, rest = item.partition(":")
            out.append(f"{names.get(event, event)}:{rest}")
        return out

    yield read
    lua(instance, f"script.on_event({{{events}}}, nil) fle_test_raised = nil")


@pytest.fixture()
def game(configure_game):
    return configure_game(
        inventory={"assembling-machine-1": 2, "transport-belt": 10, "wooden-chest": 2}
    )


def test_place_rotate_recipe_pickup_raise_events(game, raised):
    origin = Position(x=0, y=0)
    game.move_to(origin)
    machine = game.place_entity(Prototype.AssemblingMachine1, position=Position(x=4, y=0))
    belt = game.place_entity(
        Prototype.TransportBelt, position=Position(x=0, y=4), direction=Direction.RIGHT
    )
    chest = game.place_entity(Prototype.WoodenChest, position=Position(x=-3, y=0))
    game.rotate_entity(belt, Direction.DOWN)
    game.set_entity_recipe(machine, Prototype.IronGearWheel)
    game.pickup_entity(chest)

    log = raised()
    for name in ("assembling-machine-1", "transport-belt", "wooden-chest"):
        assert f"script_raised_built:{name}" in log, log
    assert "script_raised_teleported:transport-belt:same" in log, log
    assert "script_raised_teleported:assembling-machine-1:same" in log, log
    assert "script_raised_destroy:wooden-chest" in log, log


def test_connect_entities_raises_built(game, raised):
    game.move_to(Position(x=0, y=0))
    game.connect_entities(
        Position(x=0, y=2), Position(x=0, y=8), connection_type=Prototype.TransportBelt
    )
    built = [e for e in raised() if e == "script_raised_built:transport-belt"]
    assert len(built) >= 6, built
