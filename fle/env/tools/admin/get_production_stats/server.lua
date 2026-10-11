storage.actions.production_stats = function(player)
    local production_diff = {}
    local consumption_diff = {}
    local harvested_items = storage.harvested_items
    local crafted_items = storage.crafted_items
    -- Get total production counts for force
    local force = game.forces.player
    -- Factorio 2.0: statistics are per surface; report the whole force's totals
    local item_input_counts, item_production_counts = storage.utils.total_flow_counts(force, "item")
    local fluid_input_counts, fluid_production_counts = storage.utils.total_flow_counts(force, "fluid")

    for name, count in pairs(item_input_counts) do
        consumption_diff[name] = count
    end

    for name, count in pairs(item_production_counts) do
        production_diff[name] = count
    end

    for name, count in pairs(fluid_input_counts) do
        consumption_diff[name] = count
    end

    for name, count in pairs(fluid_production_counts) do
        production_diff[name] = count
    end
    return {
        output = consumption_diff,
        input = production_diff,
        harvested = harvested_items,
        crafted = crafted_items
    }
end

storage.actions.reset_production_stats = function(player)
    local force = game.forces.player
    -- Factorio 2.0: statistics are per surface; reset all of them
    for _, surface in pairs(game.surfaces) do
        force.get_item_production_statistics(surface).clear()
        force.get_fluid_production_statistics(surface).clear()
    end

    storage.harvested_items = {}
    storage.crafted_items = {}
end

