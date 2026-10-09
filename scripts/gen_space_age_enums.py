#!/usr/bin/env python3
"""Generate Factorio 2.0 / Space Age members for fle/env/game_types.py.

Reads a prototype dump taken from a running game (techs.json plus
data/{items,entities,fluids,recipes}.json) and rewrites the generated blocks
delimited by::

    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    # --- END GENERATED: space-age ---

inside ResourceName, RecipeName, Prototype, Technology and Resource. Only
names that are not already declared by hand (outside the generated blocks)
are emitted, so hand-written members always win. Output is sorted and
deterministic: re-running against the same dump produces no diff.

Usage:
    python scripts/gen_space_age_enums.py [DUMP_DIR] [--check]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAME_TYPES = REPO_ROOT / "fle" / "env" / "game_types.py"
DEFAULT_DUMP = Path.home() / "projects/factorio_agent/fle-spaceage/playbook"

BEGIN = "# --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---"
END = "# --- END GENERATED: space-age ---"
LINE_LIMIT = 88  # ruff's default line length

# Item types that are UI tools rather than things a player builds or handles.
TOOL_ITEM_TYPES = {
    "blueprint",
    "blueprint-book",
    "copy-paste-tool",
    "deconstruction-item",
    "selection-tool",
    "upgrade-item",
}

# Entity prototype type -> existing entity class, used when entities.py has no
# class named after the prototype itself (e.g. ent.Foundry for "foundry").
TYPE_TO_CLASS = {
    "ammo-turret": "GunTurret",
    "artillery-wagon": "RollingStock",
    "assembling-machine": "AssemblingMachine",
    "display-panel": "Entity",
    "electric-turret": "Turret",
    "furnace": "Furnace",
    "inserter": "Inserter",
    "lab": "Lab",
    "lightning-attractor": "LightningAttractor",
    "mining-drill": "ElectricMiningDrill",
    "rail-ramp": "Entity",
    "rail-support": "Entity",
    "reactor": "Reactor",
    "selector-combinator": "Combinator",
    "splitter": "Splitter",
    "transport-belt": "TransportBelt",
    "underground-belt": "UndergroundBelt",
}

# Entity types whose items are handled as plain items, not placed by agents
# (robots are deployed by roboports, seeds are planted by agricultural towers).
ITEM_ONLY_ENTITY_TYPES = {"construction-robot", "logistic-robot", "plant"}

# Rolling stock in FLE uses a single orientation-agnostic footprint.
DIMENSION_CHECK_EXEMPT = {"artillery-wagon"}

# Fluids pumped from tiles by an offshore pump (like water); tile data is not
# part of the dump, so these are listed explicitly and checked against it.
OFFSHORE_FLUIDS = ["ammoniacal-solution", "lava"]


def camel(name: str) -> str:
    """'electromagnetic-plant' -> 'ElectromagneticPlant', 'mk2' stays 'Mk2'."""
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_]", name))


def load_dump(dump_dir: Path) -> dict:
    def load(rel):
        return json.loads((dump_dir / rel).read_text())

    return {
        "techs": load("techs.json"),
        "items": load("data/items.json"),
        "entities": load("data/entities.json"),
        "fluids": load("data/fluids.json"),
        "recipes": load("data/recipes.json"),
    }


def _block_spans(source: str):
    """Yield (class_name, begin_idx, end_idx) for each generated block."""
    for match in re.finditer(r"^( *)" + re.escape(BEGIN) + r"\n", source, re.M):
        end = source.index(END, match.end())
        end = source.index("\n", end) + 1
        owner = re.findall(r"^class (\w+)", source[: match.start()], re.M)[-1]
        yield owner, match.start(), end, match.group(1)


def strip_generated(source: str) -> str:
    out, pos = [], 0
    for _, start, end, indent in _block_spans(source):
        out.append(source[pos:start])
        out.append(f"{indent}{BEGIN}\n{indent}{END}\n")
        pos = end
    out.append(source[pos:])
    return "".join(out)


def load_handwritten(source: str):
    """Execute game_types.py with the generated blocks emptied."""
    sys.path.insert(0, str(REPO_ROOT))
    module = types.ModuleType("_game_types_handwritten")
    exec(compile(strip_generated(source), str(GAME_TYPES), "exec"), module.__dict__)
    return module


def _fmt(name: str, values: list[str]) -> list[str]:
    """Format one enum member the way ruff would."""
    rhs = ", ".join(values)
    line = f"    {name} = {rhs}"
    if len(line) <= LINE_LIMIT:
        return [line]
    if len(values) == 1:
        return [f"    {name} = (", f"        {values[0]}", "    )"]
    return [f"    {name} = ("] + [f"        {v}," for v in values] + ["    )"]


def _unique_member(name, value, taken, kind):
    if name in taken:
        raise SystemExit(
            f"{kind}: generated member {name} ({value}) clashes with an existing "
            "member of the same name; add it by hand with a distinct name"
        )
    taken.add(name)
    return name


def entity_class_for(item_name, item, dump, ent):
    place = item.get("place_result")
    entity = dump["entities"].get(place) if place else None
    if entity is None or entity["type"] in ITEM_ONLY_ENTITY_TYPES:
        return None
    cls_name = camel(place)
    if not hasattr(ent, cls_name):
        cls_name = TYPE_TO_CLASS.get(entity["type"])
        if cls_name is None:
            raise SystemExit(
                f"no entity class for {place!r} (type {entity['type']!r}); add a "
                f"class {camel(place)} to fle/env/entities.py or a TYPE_TO_CLASS entry"
            )
    cls = getattr(ent, cls_name)
    width = getattr(cls, "__private_attributes__", {}).get("_width")
    height = getattr(cls, "__private_attributes__", {}).get("_height")
    if width is not None and height is not None and place not in DIMENSION_CHECK_EXEMPT:
        footprint = sorted([width.default, height.default])
        actual = sorted([entity["tile_width"], entity["tile_height"]])
        if footprint != actual:
            raise SystemExit(
                f"{place}: ent.{cls_name} is {width.default}x{height.default} but the "
                f"entity is {entity['tile_width']}x{entity['tile_height']}; add a "
                f"class {camel(place)} with the right footprint"
            )
    return cls_name


def generate(dump: dict, hw) -> dict[str, list[str]]:
    ent = hw.ent
    blocks: dict[str, list[str]] = {}

    # Prototype: items and fluids not already declared.
    have = {m.value[0] for m in hw.Prototype.__members__.values()}
    taken = set(hw.Prototype.__members__)
    entries = []
    for name, item in dump["items"].items():
        if name in have or name.startswith("parameter-"):
            continue
        if item["type"] in TOOL_ITEM_TYPES:
            continue
        place = item.get("place_result")
        if item["hidden"] and not (place and place in dump["entities"]):
            continue  # internal/editor item (keep hidden items that place a real entity)
        entries.append((name, entity_class_for(name, item, dump, ent)))
    for name, fluid in dump["fluids"].items():
        if name in have or name in dump["items"] or fluid["hidden"]:
            continue
        if name.startswith("parameter-"):
            continue
        entries.append((name, None))
    lines = []
    for name, cls in sorted(entries):
        member = _unique_member(camel(name), name, taken, "Prototype")
        lines += _fmt(member, [f'"{name}"', f"ent.{cls}" if cls else "None"])
    blocks["Prototype"] = lines

    # Technology: every technology in the dump.
    have = {m.value for m in hw.Technology.__members__.values()}
    taken = set(hw.Technology.__members__)
    lines = []
    for name in sorted(dump["techs"]):
        if name in have or dump["techs"][name].get("hidden"):
            continue
        lines += _fmt(
            _unique_member(camel(name), name, taken, "Technology"), [f'"{name}"']
        )
    blocks["Technology"] = lines

    # RecipeName: recipes that must be selected by name because no item shares
    # their name (fluid, multi-product and alternative recipes). Recycling
    # recipes are chosen automatically by the recycler and are skipped.
    have = {m.value for m in hw.RecipeName.__members__.values()}
    taken = set(hw.RecipeName.__members__)
    lines = []
    for name in sorted(dump["recipes"]):
        recipe = dump["recipes"][name]
        if name in have or recipe["hidden"] or name in dump["items"]:
            continue
        if name.endswith("-recycling") or name.startswith("parameter-"):
            continue
        lines += _fmt(
            _unique_member(camel(name), name, taken, "RecipeName"), [f'"{name}"']
        )
    blocks["RecipeName"] = lines

    # Resources: resource entities plus offshore-pumpable fluids.
    for fluid in OFFSHORE_FLUIDS:
        if fluid not in dump["fluids"]:
            raise SystemExit(f"offshore fluid {fluid!r} missing from the dump")
    resources = sorted(
        [n for n, e in dump["entities"].items() if e["type"] == "resource"]
        + OFFSHORE_FLUIDS
    )
    have = {m.value for m in hw.ResourceName.__members__.values()}
    taken = set(hw.ResourceName.__members__)
    blocks["ResourceName"] = [
        line
        for name in resources
        if name not in have
        for line in _fmt(
            _unique_member(camel(name), name, taken, "ResourceName"), [f'"{name}"']
        )
    ]
    hw_resources = {
        k: v
        for k, v in vars(hw.Resource).items()
        if not k.startswith("_") and isinstance(v, tuple)
    }
    have = {v[0] for v in hw_resources.values()}
    taken = set(hw_resources)
    blocks["Resource"] = [
        line
        for name in resources
        if name not in have
        for line in _fmt(
            _unique_member(camel(name), name, taken, "Resource"),
            [f'"{name}"', "ent.ResourcePatch"],
        )
    ]
    return blocks


def render(source: str, blocks: dict[str, list[str]]) -> str:
    out, pos, seen = [], 0, set()
    for owner, start, end, indent in _block_spans(source):
        if owner not in blocks:
            raise SystemExit(f"unexpected generated block in class {owner}")
        seen.add(owner)
        out.append(source[pos:start])
        body = "".join(line + "\n" for line in blocks[owner])
        out.append(f"{indent}{BEGIN}\n{body}{indent}{END}\n")
        pos = end
    out.append(source[pos:])
    missing = set(blocks) - seen
    if missing:
        raise SystemExit(f"no generated block markers in: {', '.join(sorted(missing))}")
    return "".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("dump_dir", nargs="?", type=Path, default=DEFAULT_DUMP)
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if game_types.py is stale"
    )
    args = parser.parse_args(argv)

    source = GAME_TYPES.read_text()
    blocks = generate(load_dump(args.dump_dir), load_handwritten(source))
    updated = render(source, blocks)
    counts = ", ".join(
        f"{k}={len([x for x in v if '=' in x])}" for k, v in blocks.items()
    )
    if args.check:
        if updated != source:
            print(f"{GAME_TYPES} is out of date ({counts})", file=sys.stderr)
            return 1
        print(f"up to date ({counts})")
        return 0
    if updated != source:
        GAME_TYPES.write_text(updated)
        print(f"updated {GAME_TYPES} ({counts})")
    else:
        print(f"no changes ({counts})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
