"""Offline checks of the game-type enums against a prototype dump.

The dump is a set of JSON files produced from a running Factorio 2.0 game
(techs.json plus data/{recipes,items,entities,fluids}.json). Point
``FLE_PROTOTYPE_DUMP`` at the directory holding them; tests that need the dump
are skipped when it is missing. No Factorio server is required.
"""

import json
import os
from pathlib import Path

import pytest

from fle.env.game_types import (
    Prototype,
    RecipeName,
    Resource,
    ResourceName,
    Technology,
    prototype_by_name,
    technology_by_name,
)

DEFAULT_DUMP = Path.home() / "projects/factorio_agent/fle-spaceage/playbook"
DUMP_DIR = Path(os.environ.get("FLE_PROTOTYPE_DUMP", DEFAULT_DUMP))

# FLE-internal names that are intentionally not game prototypes.
FLE_PSEUDO_PROTOTYPES = {"belt-group", "pipe-group", "electricity-group"}
# Recipe names that live in Prototype for historical reasons.
RECIPES_IN_PROTOTYPE = {"advanced-oil-processing", "coal-liquefaction"}
# Resource.Wood is a pseudo-resource used by nearest() to find trees.
FLE_PSEUDO_RESOURCES = {"wood"}


def _load(name):
    return json.loads((DUMP_DIR / name).read_text())


@pytest.fixture(scope="module")
def dump():
    if not (DUMP_DIR / "techs.json").is_file():
        pytest.skip(f"prototype dump not found at {DUMP_DIR}")
    return {
        "techs": _load("techs.json"),
        "recipes": _load("data/recipes.json"),
        "items": _load("data/items.json"),
        "entities": _load("data/entities.json"),
        "fluids": _load("data/fluids.json"),
    }


def _resource_members():
    return {
        name: value
        for name, value in vars(Resource).items()
        if not name.startswith("_") and isinstance(value, tuple)
    }


def test_prototype_values_exist_in_dump(dump):
    known = set(dump["items"]) | set(dump["entities"]) | set(dump["fluids"])
    missing = [
        (name, member.value[0])
        for name, member in Prototype.__members__.items()
        if member.value[0] not in known
        and member.value[0] not in FLE_PSEUDO_PROTOTYPES
        and not (
            member.value[0] in RECIPES_IN_PROTOTYPE
            and member.value[0] in dump["recipes"]
        )
    ]
    assert not missing, f"Prototype values not in dump: {missing}"


def test_technology_values_exist_in_dump(dump):
    missing = [
        (name, member.value)
        for name, member in Technology.__members__.items()
        if member.value not in dump["techs"]
    ]
    assert not missing, f"Technology values not in dump: {missing}"


def test_recipe_values_exist_in_dump(dump):
    missing = [
        (name, member.value)
        for name, member in RecipeName.__members__.items()
        if member.value not in dump["recipes"]
    ]
    assert not missing, f"RecipeName values not in dump: {missing}"


def test_resource_values_exist_in_dump(dump):
    known = set(dump["entities"]) | set(dump["fluids"])
    missing = [
        (name, value[0])
        for name, value in _resource_members().items()
        if value[0] not in known and value[0] not in FLE_PSEUDO_RESOURCES
    ]
    missing += [
        (name, member.value)
        for name, member in ResourceName.__members__.items()
        if member.value not in known
    ]
    assert not missing, f"Resource values not in dump: {missing}"


def test_lookup_tables_cover_every_canonical_member():
    # Enum aliases share a value with their canonical member, so the lookup
    # dicts must still resolve every value to a canonical member.
    for member in Prototype:
        assert prototype_by_name[member.value[0]] is member
    for member in Technology:
        assert technology_by_name[member.value] is member


def test_prototype_names_are_unique_per_canonical_member():
    names = [member.value[0] for member in Prototype]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"distinct Prototype members share a prototype name: {dupes}"


def test_resource_names_are_unique():
    names = [value[0] for value in _resource_members().values()]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate Resource names: {dupes}"


def test_renamed_members_resolve_to_2_0_names():
    assert Prototype.EmptyBarrel is Prototype.Barrel
    assert Prototype.Barrel.value[0] == "barrel"
    assert Prototype.CoalLiquifaction is Prototype.CoalLiquefaction
    assert Technology.AdvancedElectronics is Technology.AdvancedCircuit
    assert Technology.AdvancedElectronics2 is Technology.ProcessingUnit
    assert Technology.StackInserterCapacity1.value == "inserter-capacity-bonus-1"
    assert "RocketControlUnit" not in Prototype.__members__
    assert "Satellite" not in Prototype.__members__


def test_namespace_imports_cleanly():
    import fle.env.namespace  # noqa: F401


# Pre-existing FLE footprints that disagree with the 2.0 prototypes (beyond a
# plain rotation). Tracked separately; new members must match the dump.
KNOWN_FOOTPRINT_MISMATCHES = {
    "offshore-pump",
    "big-electric-pole",
    "substation",
    "constant-combinator",
    "power-switch",
    "cargo-wagon",
    "fluid-wagon",
    "artillery-wagon",
    "tank",
    "artillery-turret",
}


def test_entity_footprints_match_dump(dump):
    wrong = []
    for member in Prototype:
        name, cls = member.value
        attrs = getattr(cls, "__private_attributes__", {}) if cls else {}
        if name not in dump["entities"] or "_width" not in attrs:
            continue
        if name in KNOWN_FOOTPRINT_MISMATCHES:
            continue
        entity = dump["entities"][name]
        if sorted([member.WIDTH, member.HEIGHT]) != sorted(
            [entity["tile_width"], entity["tile_height"]]
        ):
            wrong.append((name, (member.WIDTH, member.HEIGHT)))
    assert not wrong, f"Prototype footprints differ from the dump: {wrong}"


def test_space_age_members_resolve():
    from fle.env import entities as ent

    expected = {
        "foundry": ent.Foundry,
        "electromagnetic-plant": ent.ElectromagneticPlant,
        "biochamber": ent.Biochamber,
        "cryogenic-plant": ent.CryogenicPlant,
        "recycler": ent.Recycler,
        "agricultural-tower": ent.AgriculturalTower,
        "big-mining-drill": ent.BigMiningDrill,
        "turbo-transport-belt": ent.TransportBelt,
        "turbo-underground-belt": ent.UndergroundBelt,
        "turbo-splitter": ent.Splitter,
        "stack-inserter": ent.Inserter,
        "space-platform-hub": ent.SpacePlatformHub,
        "asteroid-collector": ent.AsteroidCollector,
        "thruster": ent.Thruster,
        "cargo-landing-pad": ent.CargoLandingPad,
        "cargo-bay": ent.CargoBay,
        "lightning-rod": ent.LightningAttractor,
        "lightning-collector": ent.LightningCollector,
        "heating-tower": ent.HeatingTower,
        "fusion-reactor": ent.FusionReactor,
        "fusion-generator": ent.FusionGenerator,
        "railgun-turret": ent.RailgunTurret,
        "tesla-turret": ent.TeslaTurret,
    }
    for name, cls in expected.items():
        assert prototype_by_name[name].entity_class is cls, name
    for item in (
        "tungsten-carbide",
        "holmium-plate",
        "superconductor",
        "carbon-fiber",
        "bioflux",
        "nutrients",
        "metallurgic-science-pack",
        "electromagnetic-science-pack",
        "agricultural-science-pack",
        "cryogenic-science-pack",
        "promethium-science-pack",
        "promethium-asteroid-chunk",
        "space-platform-starter-pack",
    ):
        assert prototype_by_name[item].entity_class is None, item
    assert Prototype.StackInserter.value[0] == "stack-inserter"
    assert Prototype.ElectromagneticPlant is prototype_by_name["electromagnetic-plant"]
    assert technology_by_name["mining-productivity-3"]
    assert Technology.Foundry.value == "foundry"
    assert RecipeName.MoltenIron.value == "molten-iron"
    assert Resource.TungstenOre == ("tungsten-ore", ent.ResourcePatch)
    assert Resource.Lava[0] == "lava"
    assert ResourceName.Calcite.value == "calcite"


def test_generator_is_idempotent(dump):
    import importlib.util

    script = Path(__file__).resolve().parents[2] / "scripts/gen_space_age_enums.py"
    spec = importlib.util.spec_from_file_location("gen_space_age_enums", script)
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    assert gen.main([str(DUMP_DIR), "--check"]) == 0
