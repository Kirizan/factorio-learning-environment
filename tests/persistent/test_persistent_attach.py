"""persistent=True must not reset an ongoing game. Needs a live server."""

from fle.env.instance import FactorioInstance


def test_persistent_attach_keeps_research_and_inventory(instance):
    lua = instance.rcon_client.send_command
    speed = lua("/sc rcon.print(game.speed)").strip()
    attached = None
    try:
        # The fixture researches everything, so un-research one tech: a reset
        # would research it again. A reset would also change the speed.
        lua("/sc game.forces.player.technologies['logistics'].researched = false")
        lua("/sc game.speed = 3")
        lua(
            "/sc storage.agent_characters[1].get_main_inventory().insert{name='iron-plate', count=42}"
        )
        attached = FactorioInstance(
            address=instance.address or "localhost",
            tcp_port=instance.tcp_port,
            fast=True,
            persistent=True,
            peaceful=False,
            all_technologies_researched=False,
            clear_entities=False,
            inventory={},
            cache_scripts=True,
        )
        send = attached.rcon_client.send_command
        assert (
            send(
                "/sc rcon.print(tostring(game.forces.player.technologies['logistics'].researched))"
            ).strip()
            == "false"
        )
        assert send("/sc rcon.print(game.speed)").strip() == "3"
        count = send(
            "/sc rcon.print(storage.agent_characters[1].get_main_inventory().get_item_count('iron-plate'))"
        )
        assert int(count) >= 42
    finally:
        lua(
            f"/sc game.speed = {speed} "
            "game.forces.player.technologies['logistics'].researched = true"
        )
        if attached is not None:
            attached.cleanup()
