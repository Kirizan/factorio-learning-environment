"""Agent tools act on the surface the agent character is on (Space Age planets).

Needs a live server with the space-age mod (FLE_DLC=1); skipped otherwise.
"""

import pytest

from fle.env.entities import Position
from fle.env.game_types import Prototype


def lua(instance, code: str) -> str:
    return instance.rcon_client.send_command(f"/sc {code}")


@pytest.fixture()
def on_vulcanus(instance):
    has_vulcanus = lua(instance, "rcon.print(tostring(game.planets.vulcanus ~= nil))")
    if has_vulcanus.strip() != "true":
        pytest.skip("space-age mod not loaded")
    lua(
        instance,
        "local s = game.surfaces.vulcanus or game.planets.vulcanus.create_surface() "
        "s.request_to_generate_chunks({0, 0}, 3) s.force_generate_chunk_requests() "
        "for _, e in pairs(s.find_entities_filtered{force = 'player', area = {{-40, -40}, {40, 40}}}) do "
        "if e.type ~= 'character' then e.destroy() end end "
        "local c = storage.agent_characters[1] "
        "local p = s.find_non_colliding_position('character', {0, 0}, 100, 1) "
        "c.teleport(p, s)",
    )
    yield
    lua(
        instance,
        "local c = storage.agent_characters[1] c.teleport({0, 0}, game.surfaces[1])",
    )


def agent_position(instance) -> Position:
    raw = lua(
        instance,
        "local p = storage.agent_characters[1].position rcon.print(p.x .. ',' .. p.y)",
    )
    x, y = (float(v) for v in raw.split(","))
    return Position(x=x, y=y)


def count_on(instance, surface: str, name: str) -> int:
    raw = lua(
        instance,
        f"rcon.print(#game.surfaces['{surface}'].find_entities_filtered{{name='{name}'}})",
    )
    return int(raw)


def test_agent_surface_follows_character(instance, on_vulcanus):
    assert (
        lua(instance, "rcon.print(storage.utils.agent_surface(1).name)").strip()
        == "vulcanus"
    )


def test_place_entity_on_agent_surface(game, instance, on_vulcanus):
    before = count_on(instance, "vulcanus", "iron-chest")
    pos = agent_position(instance)
    game.place_entity(Prototype.IronChest, position=Position(x=pos.x + 3, y=pos.y))
    assert count_on(instance, "vulcanus", "iron-chest") == before + 1


def test_connect_belts_on_agent_surface(game, instance, on_vulcanus):
    before = count_on(instance, "vulcanus", "transport-belt")
    pos = agent_position(instance)
    game.connect_entities(
        Position(x=pos.x + 2, y=pos.y + 2),
        Position(x=pos.x + 2, y=pos.y + 8),
        Prototype.TransportBelt,
    )
    assert count_on(instance, "vulcanus", "transport-belt") > before


def test_production_stats_sum_all_surfaces(instance, on_vulcanus):
    raw = lua(
        instance,
        "local f = game.forces.player "
        "f.get_item_production_statistics('vulcanus').on_flow('iron-gear-wheel', 7) "
        "local input = storage.utils.total_flow_counts(f, 'item') "
        "rcon.print(input['iron-gear-wheel'] or 0)",
    )
    assert int(raw) >= 7
