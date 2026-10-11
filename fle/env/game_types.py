from __future__ import annotations
import enum
from difflib import get_close_matches
from fle.env import entities as ent


class ResourceName(enum.Enum):
    Coal = "coal"
    IronOre = "iron-ore"
    CopperOre = "copper-ore"
    Stone = "stone"
    Water = "water"
    CrudeOil = "crude-oil"
    UraniumOre = "uranium-ore"
    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    AmmoniacalSolution = "ammoniacal-solution"
    Calcite = "calcite"
    FluorineVent = "fluorine-vent"
    Lava = "lava"
    LithiumBrine = "lithium-brine"
    Scrap = "scrap"
    SulfuricAcidGeyser = "sulfuric-acid-geyser"
    TungstenOre = "tungsten-ore"
    # --- END GENERATED: space-age ---


class PrototypeMetaclass(enum.EnumMeta):
    def __getattr__(cls, name):
        # Try to get the attribute normally first
        try:
            return cls._member_map_[name]
        except KeyError:
            # Get all valid prototype names
            valid_names = [member.name for member in cls]

            # Find closest matches
            matches = get_close_matches(name, valid_names, n=3, cutoff=0.6)

            suggestion_msg = ""
            if matches:
                suggestion_msg = f". Did you mean: {', '.join(matches)}?"

            raise AttributeError(
                f"'{cls.__name__}' has no attribute '{name}'{suggestion_msg}"
            )


class RecipeName(enum.Enum):
    """
    Recipe names that can be used in the game for fluids
    """

    NuclearFuelReprocessing = "nuclear-fuel-reprocessing"
    UraniumProcessing = "uranium-processing"
    SulfuricAcid = (
        "sulfuric-acid"  # Recipe for producing sulfuric acid with a chemical plant
    )
    BasicOilProcessing = (
        "basic-oil-processing"  # Recipe for producing petroleum gas with a oil refinery
    )
    AdvancedOilProcessing = "advanced-oil-processing"  # Recipe for producing petroleum gas, heavy oil and light oil with a oil refinery
    CoalLiquefaction = (
        "coal-liquefaction"  # Recipe for producing petroleum gas in a oil refinery
    )
    HeavyOilCracking = (
        "heavy-oil-cracking"  # Recipe for producing light oil in a chemical plant
    )
    LightOilCracking = (
        "light-oil-cracking"  # Recipe for producing petroleum gas in a chemical plant
    )

    SolidFuelFromHeavyOil = "solid-fuel-from-heavy-oil"  # Recipe for producing solid fuel in a chemical plant
    SolidFuelFromLightOil = "solid-fuel-from-light-oil"  # Recipe for producing solid fuel in a chemical plant
    SolidFuelFromPetroleumGas = "solid-fuel-from-petroleum-gas"  # Recipe for producing solid fuel in a chemical plant

    FillCrudeOilBarrel = "crude-oil-barrel"
    FillHeavyOilBarrel = "heavy-oil-barrel"
    FillLightOilBarrel = "light-oil-barrel"
    FillLubricantBarrel = "lubricant-barrel"
    FillPetroleumGasBarrel = "petroleum-gas-barrel"
    FillSulfuricAcidBarrel = "sulfuric-acid-barrel"
    FillWaterBarrel = "water-barrel"

    EmptyCrudeOilBarrel = "empty-crude-oil-barrel"
    EmptyHeavyOilBarrel = "empty-heavy-oil-barrel"
    EmptyLightOilBarrel = "empty-light-oil-barrel"
    EmptyLubricantBarrel = "empty-lubricant-barrel"
    EmptyPetroleumGasBarrel = "empty-petroleum-gas-barrel"
    EmptySulfuricAcidBarrel = "empty-sulfuric-acid-barrel"
    EmptyWaterBarrel = "empty-water-barrel"
    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    AcidNeutralisation = "acid-neutralisation"
    AdvancedCarbonicAsteroidCrushing = "advanced-carbonic-asteroid-crushing"
    AdvancedMetallicAsteroidCrushing = "advanced-metallic-asteroid-crushing"
    AdvancedOxideAsteroidCrushing = "advanced-oxide-asteroid-crushing"
    AdvancedThrusterFuel = "advanced-thruster-fuel"
    AdvancedThrusterOxidizer = "advanced-thruster-oxidizer"
    AmmoniaRocketFuel = "ammonia-rocket-fuel"
    AmmoniacalSolutionSeparation = "ammoniacal-solution-separation"
    Biolubricant = "biolubricant"
    Bioplastic = "bioplastic"
    Biosulfur = "biosulfur"
    BurntSpoilage = "burnt-spoilage"
    CarbonicAsteroidCrushing = "carbonic-asteroid-crushing"
    CarbonicAsteroidReprocessing = "carbonic-asteroid-reprocessing"
    CastingCopper = "casting-copper"
    CastingCopperCable = "casting-copper-cable"
    CastingIron = "casting-iron"
    CastingIronGearWheel = "casting-iron-gear-wheel"
    CastingIronStick = "casting-iron-stick"
    CastingLowDensityStructure = "casting-low-density-structure"
    CastingPipe = "casting-pipe"
    CastingPipeToGround = "casting-pipe-to-ground"
    CastingSteel = "casting-steel"
    CoalSynthesis = "coal-synthesis"
    ConcreteFromMoltenIron = "concrete-from-molten-iron"
    CopperBacteriaCultivation = "copper-bacteria-cultivation"
    Electrolyte = "electrolyte"
    EmptyFluoroketoneColdBarrel = "empty-fluoroketone-cold-barrel"
    EmptyFluoroketoneHotBarrel = "empty-fluoroketone-hot-barrel"
    FishBreeding = "fish-breeding"
    Fluoroketone = "fluoroketone"
    FluoroketoneCooling = "fluoroketone-cooling"
    HolmiumSolution = "holmium-solution"
    IceMelting = "ice-melting"
    IronBacteriaCultivation = "iron-bacteria-cultivation"
    JellynutProcessing = "jellynut-processing"
    KovarexEnrichmentProcess = "kovarex-enrichment-process"
    Lubricant = "lubricant"
    MetallicAsteroidCrushing = "metallic-asteroid-crushing"
    MetallicAsteroidReprocessing = "metallic-asteroid-reprocessing"
    MoltenCopper = "molten-copper"
    MoltenCopperFromLava = "molten-copper-from-lava"
    MoltenIron = "molten-iron"
    MoltenIronFromLava = "molten-iron-from-lava"
    NutrientsFromBioflux = "nutrients-from-bioflux"
    NutrientsFromBiterEgg = "nutrients-from-biter-egg"
    NutrientsFromFish = "nutrients-from-fish"
    NutrientsFromSpoilage = "nutrients-from-spoilage"
    NutrientsFromYumakoMash = "nutrients-from-yumako-mash"
    OxideAsteroidCrushing = "oxide-asteroid-crushing"
    OxideAsteroidReprocessing = "oxide-asteroid-reprocessing"
    RocketFuelFromJelly = "rocket-fuel-from-jelly"
    SimpleCoalLiquefaction = "simple-coal-liquefaction"
    SolidFuelFromAmmonia = "solid-fuel-from-ammonia"
    SteamCondensation = "steam-condensation"
    ThrusterFuel = "thruster-fuel"
    ThrusterOxidizer = "thruster-oxidizer"
    WoodProcessing = "wood-processing"
    YumakoProcessing = "yumako-processing"
    # --- END GENERATED: space-age ---


class Prototype(enum.Enum, metaclass=PrototypeMetaclass):
    AssemblingMachine1 = "assembling-machine-1", ent.AssemblingMachine
    AssemblingMachine2 = "assembling-machine-2", ent.AdvancedAssemblingMachine
    AssemblingMachine3 = "assembling-machine-3", ent.AdvancedAssemblingMachine
    Centrifuge = "centrifuge", ent.AssemblingMachine

    BurnerInserter = "burner-inserter", ent.BurnerInserter
    FastInserter = "fast-inserter", ent.Inserter
    # Factorio 2.0: express-inserter removed, filter-inserter removed (all inserters can filter)
    # stack-filter-inserter renamed to bulk-inserter

    LongHandedInserter = "long-handed-inserter", ent.Inserter
    BulkInserter = (
        "bulk-inserter",
        ent.Inserter,
    )  # Factorio 2.0: old stack-inserter renamed to bulk-inserter
    # Backwards compatibility aliases - map to closest equivalent.
    # (No StackInserter alias: in 2.0 + Space Age "stack-inserter" is a
    # distinct prototype, so aliasing it to bulk-inserter would be wrong.)
    FilterInserter = (
        "fast-inserter",
        ent.Inserter,
    )  # Factorio 2.0: filter-inserter removed, use fast-inserter
    StackFilterInserter = (
        "bulk-inserter",
        ent.Inserter,
    )  # Factorio 2.0: renamed to bulk-inserter

    Inserter = "inserter", ent.Inserter

    BurnerMiningDrill = "burner-mining-drill", ent.BurnerMiningDrill
    ElectricMiningDrill = "electric-mining-drill", ent.ElectricMiningDrill

    StoneFurnace = "stone-furnace", ent.Furnace
    SteelFurnace = "steel-furnace", ent.Furnace
    ElectricFurnace = "electric-furnace", ent.ElectricFurnace

    Splitter = "splitter", ent.Splitter
    FastSplitter = "fast-splitter", ent.Splitter
    ExpressSplitter = "express-splitter", ent.Splitter

    Rail = "rail", ent.Rail

    TransportBelt = "transport-belt", ent.TransportBelt
    FastTransportBelt = "fast-transport-belt", ent.TransportBelt
    ExpressTransportBelt = "express-transport-belt", ent.TransportBelt
    ExpressUndergroundBelt = "express-underground-belt", ent.UndergroundBelt
    FastUndergroundBelt = "fast-underground-belt", ent.UndergroundBelt
    UndergroundBelt = "underground-belt", ent.UndergroundBelt
    OffshorePump = "offshore-pump", ent.OffshorePump
    PumpJack = "pumpjack", ent.PumpJack
    Pump = "pump", ent.Pump
    Boiler = "boiler", ent.Boiler
    OilRefinery = "oil-refinery", ent.OilRefinery
    ChemicalPlant = "chemical-plant", ent.ChemicalPlant

    SteamEngine = "steam-engine", ent.Generator
    SolarPanel = "solar-panel", ent.SolarPanel

    UndergroundPipe = "pipe-to-ground", ent.Pipe
    HeatPipe = "heat-pipe", ent.Pipe
    Pipe = "pipe", ent.Pipe

    SteelChest = "steel-chest", ent.Chest
    IronChest = "iron-chest", ent.Chest
    WoodenChest = "wooden-chest", ent.Chest
    IronGearWheel = "iron-gear-wheel", ent.Entity
    StorageTank = "storage-tank", ent.StorageTank

    SmallElectricPole = "small-electric-pole", ent.ElectricityPole
    MediumElectricPole = "medium-electric-pole", ent.ElectricityPole
    BigElectricPole = "big-electric-pole", ent.BigElectricityPole

    Coal = "coal", None
    Wood = "wood", None
    Sulfur = "sulfur", None
    IronOre = "iron-ore", None
    CopperOre = "copper-ore", None
    Stone = "stone", None
    Concrete = "concrete", None
    UraniumOre = "uranium-ore", None

    IronPlate = "iron-plate", None  # Crafting requires smelting 1 iron ore
    IronStick = "iron-stick", None
    SteelPlate = "steel-plate", None  # Crafting requires smelting 5 iron plates
    CopperPlate = "copper-plate", None  # Crafting requires smelting 1 copper ore
    StoneBrick = "stone-brick", None  # Crafting requires smelting 2 stone
    CopperCable = "copper-cable", None
    PlasticBar = "plastic-bar", None
    Barrel = "barrel", None  # Factorio 2.0: "empty-barrel" renamed to "barrel"
    EmptyBarrel = "barrel", None  # Backwards-compatible alias of Barrel
    Battery = "battery", None
    SulfuricAcid = "sulfuric-acid", None
    Uranium235 = "uranium-235", None
    Uranium238 = "uranium-238", None

    Lubricant = "lubricant", None
    PetroleumGas = "petroleum-gas", None
    AdvancedOilProcessing = (
        "advanced-oil-processing",
        None,
    )  # These are recipes, not prototypes.
    CoalLiquefaction = (
        "coal-liquefaction",
        None,
    )  # These are recipes, not prototypes.
    CoalLiquifaction = (
        "coal-liquefaction",
        None,
    )  # Backwards-compatible alias (misspelt) of CoalLiquefaction
    SolidFuel = "solid-fuel", None  # These are recipes, not prototypes.
    LightOil = "light-oil", None
    HeavyOil = "heavy-oil", None

    ElectronicCircuit = "electronic-circuit", None
    AdvancedCircuit = "advanced-circuit", None
    ProcessingUnit = "processing-unit", None
    EngineUnit = "engine-unit", None
    ElectricEngineUnit = "electric-engine-unit", None

    Lab = "lab", ent.Lab
    Accumulator = "accumulator", ent.Accumulator
    GunTurret = "gun-turret", ent.GunTurret

    PiercingRoundsMagazine = "piercing-rounds-magazine", ent.Ammo
    FirearmMagazine = "firearm-magazine", ent.Ammo
    Grenade = "grenade", None

    Radar = "radar", ent.Entity
    StoneWall = "stone-wall", ent.Entity
    Gate = "gate", ent.Entity
    SmallLamp = "small-lamp", ent.Entity

    NuclearReactor = "nuclear-reactor", ent.Reactor
    UraniumFuelCell = "uranium-fuel-cell", None
    HeatExchanger = "heat-exchanger", ent.HeatExchanger

    AutomationSciencePack = "automation-science-pack", None
    MilitarySciencePack = "military-science-pack", None
    LogisticsSciencePack = "logistic-science-pack", None
    ProductionSciencePack = "production-science-pack", None
    UtilitySciencePack = "utility-science-pack", None
    ChemicalSciencePack = "chemical-science-pack", None

    ProductivityModule = "productivity-module", None
    ProductivityModule2 = "productivity-module-2", None
    ProductivityModule3 = "productivity-module-3", None

    FlyingRobotFrame = "flying-robot-frame", None

    RocketSilo = "rocket-silo", ent.RocketSilo
    Rocket = "rocket", ent.Rocket
    RocketPart = "rocket-part", None
    LowDensityStructure = "low-density-structure", None
    RocketFuel = "rocket-fuel", None
    SpaceSciencePack = "space-science-pack", None

    BeltGroup = "belt-group", ent.BeltGroup
    PipeGroup = "pipe-group", ent.PipeGroup
    ElectricityGroup = "electricity-group", ent.ElectricityGroup

    # Logistic Chests
    PassiveProviderChest = "passive-provider-chest", ent.LogisticChest
    ActiveProviderChest = "active-provider-chest", ent.LogisticChest
    StorageChest = "storage-chest", ent.LogisticChest
    RequesterChest = "requester-chest", ent.LogisticChest
    BufferChest = "buffer-chest", ent.LogisticChest

    # Beacon
    Beacon = "beacon", ent.Beacon

    # Modules (items only)
    SpeedModule = "speed-module", None
    SpeedModule2 = "speed-module-2", None
    SpeedModule3 = "speed-module-3", None
    EfficiencyModule = "efficiency-module", None
    EfficiencyModule2 = "efficiency-module-2", None
    EfficiencyModule3 = "efficiency-module-3", None

    # Power
    Substation = "substation", ent.BigElectricityPole
    SteamTurbine = "steam-turbine", ent.Generator

    # Circuit Network
    ArithmeticCombinator = "arithmetic-combinator", ent.Combinator
    DeciderCombinator = "decider-combinator", ent.Combinator
    ConstantCombinator = "constant-combinator", ent.ConstantCombinator
    PowerSwitch = "power-switch", ent.PowerSwitch
    ProgrammableSpeaker = "programmable-speaker", ent.Entity

    # Trains
    TrainStop = "train-stop", ent.TrainStop
    RailSignal = "rail-signal", ent.RailSignal
    RailChainSignal = "rail-chain-signal", ent.RailSignal
    Locomotive = "locomotive", ent.RollingStock
    CargoWagon = "cargo-wagon", ent.Wagon
    FluidWagon = "fluid-wagon", ent.Wagon

    # Logistics
    Roboport = "roboport", ent.Roboport

    # Defense
    LaserTurret = "laser-turret", ent.Turret
    FlamethrowerTurret = "flamethrower-turret", ent.FluidTurret
    ArtilleryTurret = "artillery-turret", ent.ArtilleryTurret
    LandMine = "land-mine", ent.Entity

    # Vehicles
    Car = "car", ent.Vehicle
    Tank = "tank", ent.Tank
    Spidertron = "spidertron", ent.Vehicle

    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    AgriculturalSciencePack = "agricultural-science-pack", None
    AgriculturalTower = "agricultural-tower", ent.AgriculturalTower
    Ammonia = "ammonia", None
    AmmoniacalSolution = "ammoniacal-solution", None
    ArtificialJellynutSoil = "artificial-jellynut-soil", None
    ArtificialYumakoSoil = "artificial-yumako-soil", None
    ArtilleryShell = "artillery-shell", None
    ArtilleryTargetingRemote = "artillery-targeting-remote", None
    ArtilleryWagon = "artillery-wagon", ent.Wagon
    AsteroidCollector = "asteroid-collector", ent.AsteroidCollector
    AtomicBomb = "atomic-bomb", None
    BatteryEquipment = "battery-equipment", None
    BatteryMk2Equipment = "battery-mk2-equipment", None
    BatteryMk3Equipment = "battery-mk3-equipment", None
    BeltImmunityEquipment = "belt-immunity-equipment", None
    BigMiningDrill = "big-mining-drill", ent.BigMiningDrill
    Biochamber = "biochamber", ent.Biochamber
    Bioflux = "bioflux", None
    Biolab = "biolab", ent.Biolab
    BiterEgg = "biter-egg", None
    Calcite = "calcite", None
    CannonShell = "cannon-shell", None
    CaptiveBiterSpawner = "captive-biter-spawner", ent.CaptiveBiterSpawner
    CaptureRobotRocket = "capture-robot-rocket", None
    Carbon = "carbon", None
    CarbonFiber = "carbon-fiber", None
    CarbonicAsteroidChunk = "carbonic-asteroid-chunk", None
    CargoBay = "cargo-bay", ent.CargoBay
    CargoLandingPad = "cargo-landing-pad", ent.CargoLandingPad
    CliffExplosives = "cliff-explosives", None
    ClusterGrenade = "cluster-grenade", None
    CombatShotgun = "combat-shotgun", None
    ConstructionRobot = "construction-robot", None
    CopperBacteria = "copper-bacteria", None
    CopperWire = "copper-wire", None
    CrudeOil = "crude-oil", None
    CrudeOilBarrel = "crude-oil-barrel", None
    Crusher = "crusher", ent.Crusher
    CryogenicPlant = "cryogenic-plant", ent.CryogenicPlant
    CryogenicSciencePack = "cryogenic-science-pack", None
    DefenderCapsule = "defender-capsule", None
    DepletedUraniumFuelCell = "depleted-uranium-fuel-cell", None
    DestroyerCapsule = "destroyer-capsule", None
    DischargeDefenseEquipment = "discharge-defense-equipment", None
    DischargeDefenseRemote = "discharge-defense-remote", None
    DisplayPanel = "display-panel", ent.Entity
    DistractorCapsule = "distractor-capsule", None
    Electrolyte = "electrolyte", None
    ElectromagneticPlant = "electromagnetic-plant", ent.ElectromagneticPlant
    ElectromagneticSciencePack = "electromagnetic-science-pack", None
    EnergyShieldEquipment = "energy-shield-equipment", None
    EnergyShieldMk2Equipment = "energy-shield-mk2-equipment", None
    ExoskeletonEquipment = "exoskeleton-equipment", None
    ExplosiveCannonShell = "explosive-cannon-shell", None
    ExplosiveRocket = "explosive-rocket", None
    ExplosiveUraniumCannonShell = "explosive-uranium-cannon-shell", None
    Explosives = "explosives", None
    FissionReactorEquipment = "fission-reactor-equipment", None
    Flamethrower = "flamethrower", None
    FlamethrowerAmmo = "flamethrower-ammo", None
    Fluorine = "fluorine", None
    FluoroketoneCold = "fluoroketone-cold", None
    FluoroketoneColdBarrel = "fluoroketone-cold-barrel", None
    FluoroketoneHot = "fluoroketone-hot", None
    FluoroketoneHotBarrel = "fluoroketone-hot-barrel", None
    Foundation = "foundation", None
    Foundry = "foundry", ent.Foundry
    FusionGenerator = "fusion-generator", ent.FusionGenerator
    FusionPlasma = "fusion-plasma", None
    FusionPowerCell = "fusion-power-cell", None
    FusionReactor = "fusion-reactor", ent.FusionReactor
    FusionReactorEquipment = "fusion-reactor-equipment", None
    GreenWire = "green-wire", None
    HazardConcrete = "hazard-concrete", None
    HeatingTower = "heating-tower", ent.HeatingTower
    HeavyArmor = "heavy-armor", None
    HeavyOilBarrel = "heavy-oil-barrel", None
    HolmiumOre = "holmium-ore", None
    HolmiumPlate = "holmium-plate", None
    HolmiumSolution = "holmium-solution", None
    Ice = "ice", None
    IcePlatform = "ice-platform", None
    IronBacteria = "iron-bacteria", None
    Jelly = "jelly", None
    Jellynut = "jellynut", None
    JellynutSeed = "jellynut-seed", None
    Landfill = "landfill", None
    Lava = "lava", None
    LightArmor = "light-armor", None
    LightOilBarrel = "light-oil-barrel", None
    LightningCollector = "lightning-collector", ent.LightningCollector
    LightningRod = "lightning-rod", ent.LightningAttractor
    Lithium = "lithium", None
    LithiumBrine = "lithium-brine", None
    LithiumPlate = "lithium-plate", None
    LogisticRobot = "logistic-robot", None
    LubricantBarrel = "lubricant-barrel", None
    MechArmor = "mech-armor", None
    MetallicAsteroidChunk = "metallic-asteroid-chunk", None
    MetallurgicSciencePack = "metallurgic-science-pack", None
    ModularArmor = "modular-armor", None
    MoltenCopper = "molten-copper", None
    MoltenIron = "molten-iron", None
    NightVisionEquipment = "night-vision-equipment", None
    NuclearFuel = "nuclear-fuel", None
    Nutrients = "nutrients", None
    OvergrowthJellynutSoil = "overgrowth-jellynut-soil", None
    OvergrowthYumakoSoil = "overgrowth-yumako-soil", None
    OxideAsteroidChunk = "oxide-asteroid-chunk", None
    PentapodEgg = "pentapod-egg", None
    PersonalLaserDefenseEquipment = "personal-laser-defense-equipment", None
    PersonalRoboportEquipment = "personal-roboport-equipment", None
    PersonalRoboportMk2Equipment = "personal-roboport-mk2-equipment", None
    PetroleumGasBarrel = "petroleum-gas-barrel", None
    PiercingShotgunShell = "piercing-shotgun-shell", None
    Pistol = "pistol", None
    PoisonCapsule = "poison-capsule", None
    PowerArmor = "power-armor", None
    PowerArmorMk2 = "power-armor-mk2", None
    PromethiumAsteroidChunk = "promethium-asteroid-chunk", None
    PromethiumSciencePack = "promethium-science-pack", None
    QualityModule = "quality-module", None
    QualityModule2 = "quality-module-2", None
    QualityModule3 = "quality-module-3", None
    QuantumProcessor = "quantum-processor", None
    RailRamp = "rail-ramp", ent.Entity
    RailSupport = "rail-support", ent.Entity
    Railgun = "railgun", None
    RailgunAmmo = "railgun-ammo", None
    RailgunTurret = "railgun-turret", ent.RailgunTurret
    RawFish = "raw-fish", None
    Recycler = "recycler", ent.Recycler
    RedWire = "red-wire", None
    RefinedConcrete = "refined-concrete", None
    RefinedHazardConcrete = "refined-hazard-concrete", None
    RepairPack = "repair-pack", None
    RocketLauncher = "rocket-launcher", None
    RocketTurret = "rocket-turret", ent.RocketTurret
    Scrap = "scrap", None
    SelectorCombinator = "selector-combinator", ent.Combinator
    Shotgun = "shotgun", None
    ShotgunShell = "shotgun-shell", None
    SlowdownCapsule = "slowdown-capsule", None
    SolarPanelEquipment = "solar-panel-equipment", None
    SpacePlatformFoundation = "space-platform-foundation", None
    SpacePlatformHub = "space-platform-hub", ent.SpacePlatformHub
    SpacePlatformStarterPack = "space-platform-starter-pack", None
    SpidertronRemote = "spidertron-remote", None
    Spoilage = "spoilage", None
    StackInserter = "stack-inserter", ent.Inserter
    Steam = "steam", None
    SubmachineGun = "submachine-gun", None
    SulfuricAcidBarrel = "sulfuric-acid-barrel", None
    Supercapacitor = "supercapacitor", None
    Superconductor = "superconductor", None
    TeslaAmmo = "tesla-ammo", None
    TeslaTurret = "tesla-turret", ent.TeslaTurret
    Teslagun = "teslagun", None
    Thruster = "thruster", ent.Thruster
    ThrusterFuel = "thruster-fuel", None
    ThrusterOxidizer = "thruster-oxidizer", None
    ToolbeltEquipment = "toolbelt-equipment", None
    TreeSeed = "tree-seed", None
    TungstenCarbide = "tungsten-carbide", None
    TungstenOre = "tungsten-ore", None
    TungstenPlate = "tungsten-plate", None
    TurboSplitter = "turbo-splitter", ent.Splitter
    TurboTransportBelt = "turbo-transport-belt", ent.TransportBelt
    TurboUndergroundBelt = "turbo-underground-belt", ent.UndergroundBelt
    UraniumCannonShell = "uranium-cannon-shell", None
    UraniumRoundsMagazine = "uranium-rounds-magazine", None
    Water = "water", None
    WaterBarrel = "water-barrel", None
    Yumako = "yumako", None
    YumakoMash = "yumako-mash", None
    YumakoSeed = "yumako-seed", None
    # --- END GENERATED: space-age ---

    def __init__(self, prototype_name, entity_class_name):
        self.prototype_name = prototype_name
        self.entity_class = entity_class_name

    @property
    def WIDTH(self):
        return self.entity_class._width.default  # Access the class attribute directly

    @property
    def HEIGHT(self):
        return self.entity_class._height.default


prototype_by_name = {prototype.value[0]: prototype for prototype in Prototype}
prototype_by_title = {str(prototype): prototype for prototype in Prototype}


class Technology(enum.Enum):
    # Science pack technologies (Factorio 2.0 prerequisites)
    SteamPower = "steam-power"  # Starting tech, no prerequisites
    AutomationSciencePack = "automation-science-pack"  # Requires steam-power

    # Basic automation technologies
    Automation = "automation"  # Unlocks assembling machine 1
    Automation2 = "automation-2"  # Unlocks assembling machine 2
    Automation3 = "automation-3"  # Unlocks assembling machine 3

    # Logistics technologies
    Logistics = "logistics"  # Unlocks basic belts and inserters
    Logistics2 = "logistics-2"  # Unlocks fast belts and inserters
    Logistics3 = "logistics-3"  # Unlocks express belts and inserters

    # Circuit technologies
    # CircuitNetwork = "circuit-network"
    # Factorio 2.0: advanced-electronics(-2) became advanced-circuit / processing-unit
    AdvancedCircuit = "advanced-circuit"
    ProcessingUnit = "processing-unit"
    AdvancedElectronics = "advanced-circuit"  # Backwards-compatible alias
    AdvancedElectronics2 = "processing-unit"  # Backwards-compatible alias

    # Power technologies
    Electronics = "electronics"
    ElectricEnergy = "electric-energy-distribution-1"
    ElectricEnergy2 = "electric-energy-distribution-2"
    SolarEnergy = "solar-energy"
    ElectricEngineering = "electric-engine"
    BatteryTechnology = "battery"
    # AdvancedBattery = "battery-mk2-equipment"
    NuclearPower = "nuclear-power"

    # Mining technologies
    SteelProcessing = "steel-processing"
    AdvancedMaterialProcessing = "advanced-material-processing"
    AdvancedMaterialProcessing2 = "advanced-material-processing-2"

    # Military technologies
    MilitaryScience = "military"
    # MilitaryScience2 = "military-2"
    # MilitaryScience3 = "military-3"
    # MilitaryScience4 = "military-4"
    # Artillery = "artillery"
    # Flamethrower = "flamethrower"
    # LandMines = "land-mines"
    # Turrets = "turrets"
    # LaserTurrets = "laser-turrets"
    # RocketSilo = "rocket-silo"

    # Armor and equipment
    ModularArmor = "modular-armor"
    PowerArmor = "power-armor"
    PowerArmor2 = "power-armor-mk2"
    NightVision = "night-vision-equipment"
    EnergyShield = "energy-shield-equipment"
    EnergyShield2 = "energy-shield-mk2-equipment"

    # Train technologies
    RailwayTransportation = "railway"
    # AutomatedRailTransportation = "automated-rail-transportation"
    # RailSignals = "rail-signals"

    # Oil processing
    OilProcessing = "oil-processing"
    AdvancedOilProcessing = "advanced-oil-processing"
    SulfurProcessing = "sulfur-processing"
    Plastics = "plastics"
    Lubricant = "lubricant"

    # Modules
    # Modules = "modules"
    # SpeedModule = "speed-module"
    # SpeedModule2 = "speed-module-2"
    # SpeedModule3 = "speed-module-3"
    ProductivityModule = "productivity-module"
    ProductivityModule2 = "productivity-module-2"
    ProductivityModule3 = "productivity-module-3"
    # EfficiencyModule = "efficiency-module"
    # EfficiencyModule2 = "efficiency-module-2"
    # EfficiencyModule3 = "efficiency-module-3"

    # Robot technologies
    Robotics = "robotics"
    # ConstructionRobotics = "construction-robotics"
    # LogisticRobotics = "logistic-robotics"
    # LogisticSystem = "logistic-system"
    # CharacterLogisticSlots = "character-logistic-slots"
    # CharacterLogisticSlots2 = "character-logistic-slots-2"

    # Science technologies
    LogisticsSciencePack = "logistic-science-pack"
    MilitarySciencePack = "military-science-pack"
    ChemicalSciencePack = "chemical-science-pack"
    ProductionSciencePack = "production-science-pack"
    # UtilitySciencePack = "utility-science-pack"
    # SpaceSciencePack = "space-science-pack"

    # Inserter technologies
    FastInserter = "fast-inserter"
    StackInserter = "stack-inserter"
    # Factorio 2.0: stack-inserter-capacity-bonus-N merged into inserter-capacity-bonus-N
    InserterCapacityBonus1 = "inserter-capacity-bonus-1"
    InserterCapacityBonus2 = "inserter-capacity-bonus-2"
    StackInserterCapacity1 = "inserter-capacity-bonus-1"  # Backwards-compatible alias
    StackInserterCapacity2 = "inserter-capacity-bonus-2"  # Backwards-compatible alias

    # Storage technologies
    StorageTanks = "fluid-handling"
    # Factorio 2.0: barrel-filling removed; barrels are unlocked by fluid-handling
    # Warehouses = "warehousing"

    # Vehicle technologies
    # Automobiles = "automobilism"
    # TankTechnology = "tank"
    # SpiderVehicle = "spidertron"

    # Weapon technologies
    # Factorio 2.0: grenades tech removed; grenade is unlocked by military-2
    Military2 = "military-2"
    # ClusterGrenades = "cluster-grenades"
    # RocketLauncher = "rocketry"
    # ExplosiveRocketry = "explosive-rocketry"
    # AtomicBomb = "atomic-bomb"
    # CombatRobotics = "combat-robotics"
    # CombatRobotics2 = "combat-robotics-2"
    # CombatRobotics3 = "combat-robotics-3"

    # Misc technologies
    Landfill = "landfill"
    # Factorio 2.0: character-inventory-slots does not exist (use toolbelt)
    Toolbelt = "toolbelt"
    ResearchSpeed1 = "research-speed-1"
    ResearchSpeed = "research-speed-1"  # Backwards-compatible alias
    # BrakinPower = "braking-force"

    # # Endgame technologies
    SpaceScience = "space-science-pack"
    RocketFuel = "rocket-fuel"
    LowDensityStructure = "low-density-structure"
    RocketSiloTechnology = "rocket-silo"
    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    AdvancedAsteroidProcessing = "advanced-asteroid-processing"
    AdvancedCombinators = "advanced-combinators"
    AgriculturalSciencePack = "agricultural-science-pack"
    Agriculture = "agriculture"
    ArtificialSoil = "artificial-soil"
    Artillery = "artillery"
    ArtilleryShellDamage1 = "artillery-shell-damage-1"
    ArtilleryShellRange1 = "artillery-shell-range-1"
    ArtilleryShellSpeed1 = "artillery-shell-speed-1"
    AsteroidProductivity = "asteroid-productivity"
    AsteroidReprocessing = "asteroid-reprocessing"
    AtomicBomb = "atomic-bomb"
    AutomatedRailTransportation = "automated-rail-transportation"
    Automobilism = "automobilism"
    BacteriaCultivation = "bacteria-cultivation"
    BatteryEquipment = "battery-equipment"
    BatteryMk2Equipment = "battery-mk2-equipment"
    BatteryMk3Equipment = "battery-mk3-equipment"
    BeltImmunityEquipment = "belt-immunity-equipment"
    BigMiningDrill = "big-mining-drill"
    Biochamber = "biochamber"
    Bioflux = "bioflux"
    BiofluxProcessing = "bioflux-processing"
    Biolab = "biolab"
    BiterEggHandling = "biter-egg-handling"
    BrakingForce1 = "braking-force-1"
    BrakingForce2 = "braking-force-2"
    BrakingForce3 = "braking-force-3"
    BrakingForce4 = "braking-force-4"
    BrakingForce5 = "braking-force-5"
    BrakingForce6 = "braking-force-6"
    BrakingForce7 = "braking-force-7"
    BulkInserter = "bulk-inserter"
    CalciteProcessing = "calcite-processing"
    CaptiveBiterSpawner = "captive-biter-spawner"
    Captivity = "captivity"
    CarbonFiber = "carbon-fiber"
    CircuitNetwork = "circuit-network"
    CliffExplosives = "cliff-explosives"
    CoalLiquefaction = "coal-liquefaction"
    Concrete = "concrete"
    ConstructionRobotics = "construction-robotics"
    CryogenicPlant = "cryogenic-plant"
    CryogenicSciencePack = "cryogenic-science-pack"
    Defender = "defender"
    Destroyer = "destroyer"
    DischargeDefenseEquipment = "discharge-defense-equipment"
    Distractor = "distractor"
    EffectTransmission = "effect-transmission"
    EfficiencyModule = "efficiency-module"
    EfficiencyModule2 = "efficiency-module-2"
    EfficiencyModule3 = "efficiency-module-3"
    ElectricEnergyAccumulators = "electric-energy-accumulators"
    ElectricMiningDrill = "electric-mining-drill"
    ElectricWeaponsDamage1 = "electric-weapons-damage-1"
    ElectricWeaponsDamage2 = "electric-weapons-damage-2"
    ElectricWeaponsDamage3 = "electric-weapons-damage-3"
    ElectricWeaponsDamage4 = "electric-weapons-damage-4"
    ElectromagneticPlant = "electromagnetic-plant"
    ElectromagneticSciencePack = "electromagnetic-science-pack"
    ElevatedRail = "elevated-rail"
    Engine = "engine"
    EpicQuality = "epic-quality"
    ExoskeletonEquipment = "exoskeleton-equipment"
    ExplosiveRocketry = "explosive-rocketry"
    Explosives = "explosives"
    FishBreeding = "fish-breeding"
    FissionReactorEquipment = "fission-reactor-equipment"
    Flamethrower = "flamethrower"
    Flammables = "flammables"
    FluidWagon = "fluid-wagon"
    FollowerRobotCount1 = "follower-robot-count-1"
    FollowerRobotCount2 = "follower-robot-count-2"
    FollowerRobotCount3 = "follower-robot-count-3"
    FollowerRobotCount4 = "follower-robot-count-4"
    FollowerRobotCount5 = "follower-robot-count-5"
    Foundation = "foundation"
    Foundry = "foundry"
    FusionReactor = "fusion-reactor"
    FusionReactorEquipment = "fusion-reactor-equipment"
    Gate = "gate"
    GunTurret = "gun-turret"
    Health = "health"
    HeatingTower = "heating-tower"
    HeavyArmor = "heavy-armor"
    HolmiumProcessing = "holmium-processing"
    InserterCapacityBonus3 = "inserter-capacity-bonus-3"
    InserterCapacityBonus4 = "inserter-capacity-bonus-4"
    InserterCapacityBonus5 = "inserter-capacity-bonus-5"
    InserterCapacityBonus6 = "inserter-capacity-bonus-6"
    InserterCapacityBonus7 = "inserter-capacity-bonus-7"
    Jellynut = "jellynut"
    KovarexEnrichmentProcess = "kovarex-enrichment-process"
    Lamp = "lamp"
    LandMine = "land-mine"
    Laser = "laser"
    LaserShootingSpeed1 = "laser-shooting-speed-1"
    LaserShootingSpeed2 = "laser-shooting-speed-2"
    LaserShootingSpeed3 = "laser-shooting-speed-3"
    LaserShootingSpeed4 = "laser-shooting-speed-4"
    LaserShootingSpeed5 = "laser-shooting-speed-5"
    LaserShootingSpeed6 = "laser-shooting-speed-6"
    LaserShootingSpeed7 = "laser-shooting-speed-7"
    LaserTurret = "laser-turret"
    LaserWeaponsDamage1 = "laser-weapons-damage-1"
    LaserWeaponsDamage2 = "laser-weapons-damage-2"
    LaserWeaponsDamage3 = "laser-weapons-damage-3"
    LaserWeaponsDamage4 = "laser-weapons-damage-4"
    LaserWeaponsDamage5 = "laser-weapons-damage-5"
    LaserWeaponsDamage6 = "laser-weapons-damage-6"
    LaserWeaponsDamage7 = "laser-weapons-damage-7"
    LegendaryQuality = "legendary-quality"
    LightningCollector = "lightning-collector"
    LithiumProcessing = "lithium-processing"
    LogisticRobotics = "logistic-robotics"
    LogisticSystem = "logistic-system"
    LowDensityStructureProductivity = "low-density-structure-productivity"
    MechArmor = "mech-armor"
    MetallurgicSciencePack = "metallurgic-science-pack"
    Military3 = "military-3"
    Military4 = "military-4"
    MiningProductivity1 = "mining-productivity-1"
    MiningProductivity2 = "mining-productivity-2"
    MiningProductivity3 = "mining-productivity-3"
    Modules = "modules"
    NuclearFuelReprocessing = "nuclear-fuel-reprocessing"
    OilGathering = "oil-gathering"
    OvergrowthSoil = "overgrowth-soil"
    PersonalLaserDefenseEquipment = "personal-laser-defense-equipment"
    PersonalRoboportEquipment = "personal-roboport-equipment"
    PersonalRoboportMk2Equipment = "personal-roboport-mk2-equipment"
    PhysicalProjectileDamage1 = "physical-projectile-damage-1"
    PhysicalProjectileDamage2 = "physical-projectile-damage-2"
    PhysicalProjectileDamage3 = "physical-projectile-damage-3"
    PhysicalProjectileDamage4 = "physical-projectile-damage-4"
    PhysicalProjectileDamage5 = "physical-projectile-damage-5"
    PhysicalProjectileDamage6 = "physical-projectile-damage-6"
    PhysicalProjectileDamage7 = "physical-projectile-damage-7"
    PlanetDiscoveryAquilo = "planet-discovery-aquilo"
    PlanetDiscoveryFulgora = "planet-discovery-fulgora"
    PlanetDiscoveryGleba = "planet-discovery-gleba"
    PlanetDiscoveryVulcanus = "planet-discovery-vulcanus"
    PlasticBarProductivity = "plastic-bar-productivity"
    ProcessingUnitProductivity = "processing-unit-productivity"
    PromethiumSciencePack = "promethium-science-pack"
    QualityModule = "quality-module"
    QualityModule2 = "quality-module-2"
    QualityModule3 = "quality-module-3"
    QuantumProcessor = "quantum-processor"
    Radar = "radar"
    RailSupportFoundations = "rail-support-foundations"
    Railgun = "railgun"
    RailgunDamage1 = "railgun-damage-1"
    RailgunShootingSpeed1 = "railgun-shooting-speed-1"
    Recycling = "recycling"
    RefinedFlammables1 = "refined-flammables-1"
    RefinedFlammables2 = "refined-flammables-2"
    RefinedFlammables3 = "refined-flammables-3"
    RefinedFlammables4 = "refined-flammables-4"
    RefinedFlammables5 = "refined-flammables-5"
    RefinedFlammables6 = "refined-flammables-6"
    RefinedFlammables7 = "refined-flammables-7"
    RepairPack = "repair-pack"
    ResearchProductivity = "research-productivity"
    ResearchSpeed2 = "research-speed-2"
    ResearchSpeed3 = "research-speed-3"
    ResearchSpeed4 = "research-speed-4"
    ResearchSpeed5 = "research-speed-5"
    ResearchSpeed6 = "research-speed-6"
    RocketFuelProductivity = "rocket-fuel-productivity"
    RocketPartProductivity = "rocket-part-productivity"
    RocketTurret = "rocket-turret"
    Rocketry = "rocketry"
    ScrapRecyclingProductivity = "scrap-recycling-productivity"
    SolarPanelEquipment = "solar-panel-equipment"
    SpacePlatform = "space-platform"
    SpacePlatformThruster = "space-platform-thruster"
    SpeedModule = "speed-module"
    SpeedModule2 = "speed-module-2"
    SpeedModule3 = "speed-module-3"
    Spidertron = "spidertron"
    SteelAxe = "steel-axe"
    SteelPlateProductivity = "steel-plate-productivity"
    StoneWall = "stone-wall"
    StrongerExplosives1 = "stronger-explosives-1"
    StrongerExplosives2 = "stronger-explosives-2"
    StrongerExplosives3 = "stronger-explosives-3"
    StrongerExplosives4 = "stronger-explosives-4"
    StrongerExplosives5 = "stronger-explosives-5"
    StrongerExplosives6 = "stronger-explosives-6"
    StrongerExplosives7 = "stronger-explosives-7"
    Tank = "tank"
    TeslaWeapons = "tesla-weapons"
    ToolbeltEquipment = "toolbelt-equipment"
    TransportBeltCapacity1 = "transport-belt-capacity-1"
    TransportBeltCapacity2 = "transport-belt-capacity-2"
    TreeSeeding = "tree-seeding"
    TungstenCarbide = "tungsten-carbide"
    TungstenSteel = "tungsten-steel"
    TurboTransportBelt = "turbo-transport-belt"
    UraniumAmmo = "uranium-ammo"
    UraniumMining = "uranium-mining"
    UraniumProcessing = "uranium-processing"
    UtilitySciencePack = "utility-science-pack"
    WeaponShootingSpeed1 = "weapon-shooting-speed-1"
    WeaponShootingSpeed2 = "weapon-shooting-speed-2"
    WeaponShootingSpeed3 = "weapon-shooting-speed-3"
    WeaponShootingSpeed4 = "weapon-shooting-speed-4"
    WeaponShootingSpeed5 = "weapon-shooting-speed-5"
    WeaponShootingSpeed6 = "weapon-shooting-speed-6"
    WorkerRobotsSpeed1 = "worker-robots-speed-1"
    WorkerRobotsSpeed2 = "worker-robots-speed-2"
    WorkerRobotsSpeed3 = "worker-robots-speed-3"
    WorkerRobotsSpeed4 = "worker-robots-speed-4"
    WorkerRobotsSpeed5 = "worker-robots-speed-5"
    WorkerRobotsSpeed6 = "worker-robots-speed-6"
    WorkerRobotsSpeed7 = "worker-robots-speed-7"
    WorkerRobotsStorage1 = "worker-robots-storage-1"
    WorkerRobotsStorage2 = "worker-robots-storage-2"
    WorkerRobotsStorage3 = "worker-robots-storage-3"
    Yumako = "yumako"
    # --- END GENERATED: space-age ---


# Helper dictionary to look up technology by name string
technology_by_name = {tech.value: tech for tech in Technology}


class Resource:
    Coal = "coal", ent.ResourcePatch
    IronOre = "iron-ore", ent.ResourcePatch
    CopperOre = "copper-ore", ent.ResourcePatch
    Stone = "stone", ent.ResourcePatch
    Water = "water", ent.ResourcePatch
    CrudeOil = "crude-oil", ent.ResourcePatch
    UraniumOre = "uranium-ore", ent.ResourcePatch
    Wood = "wood", ent.ResourcePatch
    # --- BEGIN GENERATED: space-age (scripts/gen_space_age_enums.py) ---
    AmmoniacalSolution = "ammoniacal-solution", ent.ResourcePatch
    Calcite = "calcite", ent.ResourcePatch
    FluorineVent = "fluorine-vent", ent.ResourcePatch
    Lava = "lava", ent.ResourcePatch
    LithiumBrine = "lithium-brine", ent.ResourcePatch
    Scrap = "scrap", ent.ResourcePatch
    SulfuricAcidGeyser = "sulfuric-acid-geyser", ent.ResourcePatch
    TungstenOre = "tungsten-ore", ent.ResourcePatch
    # --- END GENERATED: space-age ---
