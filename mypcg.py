import random
from gdpc import Editor, Block, WorldSlice, Rect

def main():
    print("Initializing Editor (buffering enabled)...")
    editor = Editor(buffering=True)
    
    
    build_area = editor.getBuildArea()
    (x1, y1, z1) = build_area.begin
    (x2, y2, z2) = build_area.end
    print(f"Build area: begin=({x1}, {y1}, {z1})  end=({x2}, {y2}, {z2})")
    
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_z, max_z = min(z1, z2), max(z1, z2)
    size_x, size_z = max_x - min_x, max_z - min_z
    build_rect = Rect((min_x, min_z), (size_x, size_z))
    print(f"Using build rectangle: pos=({min_x}, {min_z}), size=({size_x}, {size_z})")
    
    world_slice = WorldSlice(build_rect)
    print("World slice loaded.")
    
    # Randomize house dimensions for variation
    HOUSE_WIDTH = random.randint(10, 20)
    HOUSE_DEPTH = random.randint(8, 16)
    WALL_HEIGHT = random.randint(4, 8)
    print(f"House dimensions (randomized): width={HOUSE_WIDTH}, depth={HOUSE_DEPTH}, wall height={WALL_HEIGHT}")
    
    
    FOUNDATION_OPTIONS = [
        "minecraft:stone_bricks", "minecraft:cobblestone", "minecraft:andesite", 
        "minecraft:polished_andesite", "minecraft:brick_block", "minecraft:quartz_block",
        "minecraft:red_nether_bricks", "minecraft:prismarine"
    ]
    WALL_OPTIONS = [
        "minecraft:oak_planks", "minecraft:birch_planks", "minecraft:jungle_planks", 
        "minecraft:acacia_planks", "minecraft:spruce_planks", "minecraft:red_terracotta",
        "minecraft:orange_terracotta", "minecraft:yellow_terracotta", "minecraft:green_terracotta",
        "minecraft:blue_terracotta", "minecraft:purple_terracotta", "minecraft:light_blue_terracotta"
    ]
    foundation_material = random.choice(FOUNDATION_OPTIONS)
    wall_material = random.choice(WALL_OPTIONS)
    roof_material = "minecraft:glass"  # Transparent, see-through glass
    print(f"Selected foundation: {foundation_material}")
    print(f"Selected walls: {wall_material}")
    print("Roof will use transparent glass.")
    
    # Determine a suitable build location on natural ground
    print("Evaluating terrain for build location...")
    build_location = find_flattest_spot(world_slice, min_x, min_z, max_x, max_z, HOUSE_WIDTH, HOUSE_DEPTH)
    if not build_location:
        print("No suitable flat spot found based on allowed ground criteria; using default build area origin.")
        build_location = (min_x, min_z, y1)
    base_x, base_z, base_y = build_location
    print(f"Build location chosen at: ({base_x}, {base_y}, {base_z})")
    
    # Get heightmap from world slice
    heightmap = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    
    print("Filling gap underneath house...")
    fill_underneath(editor, heightmap, min_x, min_z, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH)
    
    # Build house components
    print("Clearing construction area...")
    clear_area(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH)
    
    print("Building foundation...")
    build_foundation(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH, foundation_material)
    
    print("Building walls...")
    build_walls(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH, WALL_HEIGHT, wall_material)
    
    print("Building roof...")
    build_glass_roof(editor, base_x, base_y + WALL_HEIGHT, base_z, HOUSE_WIDTH, HOUSE_DEPTH, roof_material)
    
    print("Installing windows...")
    install_windows_with_skip(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH, WALL_HEIGHT)
    
    print("Installing house door...")
    install_automatic_door(editor, base_x, base_y, base_z, HOUSE_WIDTH)
    
    print("Furnishing interior...")
    furnish_interior(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH, WALL_HEIGHT)
    
    print("Adding flower garden...")
    add_flower_garden(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH)
    
    print("Adding exterior lighting...")
    add_exterior_lighting(editor, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH)
    
    print("Building washroom...")
    washroom_door_outside = build_washroom(editor, heightmap, min_x, min_z, base_x, base_y, base_z, HOUSE_WIDTH, HOUSE_DEPTH, WALL_HEIGHT)
    
    print("Building connecting path from house to washroom...")
    house_door_outside = (base_x + HOUSE_WIDTH // 2, base_z - 2)
    build_path(editor, house_door_outside[0], base_y, house_door_outside[1],
               washroom_door_outside[0], base_y, washroom_door_outside[1])
    
    print("Flushing buffer... House construction complete.")
    editor.flushBuffer()
    print("All changes flushed. Build process finished.")

def find_flattest_spot(world_slice, min_x, min_z, max_x, max_z, width, depth):
    heightmap = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    best_score = float('inf')
    best_loc = None
    ALLOWED_GROUND = {"minecraft:grass_block", "minecraft:dirt", "minecraft:stone",
                      "minecraft:sand", "minecraft:gravel", "minecraft:podzol", "minecraft:coarse_dirt"}
    for x in range(min_x, max_x - width + 1):
        for z in range(min_z, max_z - depth + 1):
            heights = []
            for dx in range(width):
                for dz in range(depth):
                    hx = (x + dx) - min_x
                    hz = (z + dz) - min_z
                    h = int(heightmap[hx][hz])
                    heights.append(h)
            diff = max(heights) - min(heights)
            avg = sum(heights) // len(heights)
            valid = True
            for dx in range(width):
                for dz in range(depth):
                    local_x = (x + dx) - min_x
                    local_z = (z + dz) - min_z
                    ground_y = avg - 1
                    block = world_slice.getBlock((local_x, ground_y, local_z))
                    if block.id not in ALLOWED_GROUND:
                        valid = False
                        break
                if not valid:
                    break
            if valid and diff < best_score:
                best_score = diff
                best_loc = (x, z, avg)
    print("Terrain evaluation complete.")
    return best_loc

def fill_underneath(editor, heightmap, min_x, min_z, start_x, base_y, start_z, width, depth):
    for xi in range(start_x, start_x + width):
        for zi in range(start_z, start_z + depth):
            local_x = xi - min_x
            local_z = zi - min_z
            terrain_height = int(heightmap[local_x][local_z])
            for fill_y in range(terrain_height + 1, base_y):
                editor.placeBlock((xi, fill_y, zi), Block("minecraft:grass_block"))
    print("Underneath gap filled with natural blocks.")

def clear_area(editor, x, y, z, width, depth):
    for xi in range(x, x + width):
        for zi in range(z, z + depth):
            for yy in range(y, y + 6):
                editor.placeBlock((xi, yy, zi), Block("minecraft:air"))
    print("Construction area cleared.")

def build_foundation(editor, x, y, z, width, depth, material):
    for xi in range(x, x + width):
        for zi in range(z, z + depth):
            editor.placeBlock((xi, y, zi), Block(material))
    print("Foundation built.")

def build_walls(editor, x, y, z, width, depth, height, material):
    for level_y in range(y + 1, y + height + 1):
        for xi in range(x, x + width):
            editor.placeBlock((xi, level_y, z), Block(material))
            editor.placeBlock((xi, level_y, z + depth - 1), Block(material))
        for zi in range(z + 1, z + depth - 1):
            editor.placeBlock((x, level_y, zi), Block(material))
            editor.placeBlock((x + width - 1, level_y, zi), Block(material))
    print("Walls built.")

def build_glass_roof(editor, x, roof_y, z, width, depth, roof_material):
    for xi in range(x, x + width):
        for zi in range(z, z + depth):
            editor.placeBlock((xi, roof_y, zi), Block(roof_material))
    top_y = roof_y + 1
    for xi in range(x, x + width):
        editor.placeBlock((xi, top_y, z), Block("minecraft:sea_lantern"))
        editor.placeBlock((xi, top_y, z + depth - 1), Block("minecraft:sea_lantern"))
    for zi in range(z, z + depth):
        editor.placeBlock((x, top_y, zi), Block("minecraft:sea_lantern"))
        editor.placeBlock((x + width - 1, top_y, zi), Block("minecraft:sea_lantern"))
    print("Roof built.")

def install_windows_with_skip(editor, x, y, z, width, depth, wall_height):
    window_y = y + 2
    door_x = x + width // 2
    for xi in range(x + 1, x + width - 1):
        if xi in [door_x - 1, door_x, door_x + 1]:
            editor.placeBlock((xi, window_y, z), Block("minecraft:oak_planks"))
        else:
            editor.placeBlock((xi, window_y, z), Block("minecraft:glass_pane"))
    for xi in range(x + 1, x + width - 1):
        editor.placeBlock((xi, window_y, z + depth - 1), Block("minecraft:glass_pane"))
    for zi in range(z + 1, z + depth - 1):
        editor.placeBlock((x, window_y, zi), Block("minecraft:glass_pane"))
        editor.placeBlock((x + width - 1, window_y, zi), Block("minecraft:glass_pane"))
    print("Windows installed.")

def install_automatic_door(editor, x, y, z, width):
    door_x = x + width // 2
    door_z = z
    editor.placeBlock((door_x, y + 1, door_z), Block("minecraft:air"))
    editor.placeBlock((door_x, y + 2, door_z), Block("minecraft:air"))
    editor.placeBlock((door_x, y + 1, door_z), Block("minecraft:oak_door", {"facing": "south", "half": "lower"}))
    editor.placeBlock((door_x, y + 2, door_z), Block("minecraft:oak_door", {"half": "upper"}))
    outside_z = door_z - 1
    editor.placeBlock((door_x, y, outside_z), Block("minecraft:stone"))
    editor.placeBlock((door_x, y + 1, outside_z), Block("minecraft:oak_pressure_plate"))
    inside_z = door_z + 1
    editor.placeBlock((door_x, y, inside_z), Block("minecraft:stone"))
    editor.placeBlock((door_x, y + 1, inside_z), Block("minecraft:oak_pressure_plate"))
    print("House door installed.")

def furnish_interior(editor, x, y, z, width, depth, wall_height):
    bed_x = x + 3
    bed_z = z + 3
    editor.placeBlock((bed_x, y + 1, bed_z), Block("minecraft:red_bed", {"facing": "east"}))
    editor.placeBlock((bed_x + 1, y + 1, bed_z), Block("minecraft:red_bed", {"facing": "east"}))
    ctable_x = x + width - 3
    ctable_z = z + 2
    editor.placeBlock((ctable_x, y + 1, ctable_z), Block("minecraft:crafting_table"))
    editor.placeBlock((ctable_x - 1, y + 1, ctable_z), Block("minecraft:chest"))
    for shelf_x in range(x + 2, x + width - 2):
        editor.placeBlock((shelf_x, y + 1, z + depth - 2), Block("minecraft:bookshelf"))
    for (lx, lz) in [(x + width//2, z + depth//2),
                     (x + width//2 - 1, z + depth//2),
                     (x + width//2, z + depth//2 - 1),
                     (x + width//2 - 1, z + depth//2 - 1)]:
        editor.placeBlock((lx, y + 1, lz), Block("minecraft:sea_lantern"))
        editor.placeBlock((lx, y + wall_height, lz), Block("minecraft:sea_lantern"))
    fire_x, fire_z = x + 2, z + depth//2
    editor.placeBlock((fire_x, y + 1, fire_z), Block("minecraft:stone_bricks"))
    editor.placeBlock((fire_x, y + 2, fire_z), Block("minecraft:campfire"))
    editor.placeBlock((fire_x, y + wall_height, fire_z), Block("minecraft:air"))
    tv_x = x + (width//2) - 2
    tv_y = y + 2
    tv_z = z + depth - 1
    install_tv(editor, tv_x, tv_y, tv_z, playing=True)
    print("Interior furnished.")

def install_tv(editor, x, y, z, playing=False):
    screen = "minecraft:glowstone" if playing else "minecraft:black_stained_glass"
    for dx in range(5):
        for dy in range(4):
            if dx == 0 or dx == 4 or dy == 0 or dy == 3:
                editor.placeBlock((x+dx, y+dy, z), Block("minecraft:quartz_block"))
            else:
                editor.placeBlock((x+dx, y+dy, z), Block(screen))
    print("TV installed and playing." if playing else "TV installed.")

def add_flower_garden(editor, x, y, z, width, depth):
    garden_depth = 4
    start_z = z + depth
    flowers = ["minecraft:dandelion", "minecraft:poppy", "minecraft:blue_orchid",
               "minecraft:allium", "minecraft:azure_bluet", "minecraft:red_tulip",
               "minecraft:orange_tulip", "minecraft:white_tulip", "minecraft:pink_tulip",
               "minecraft:oxeye_daisy"]
    for xi in range(x, x + width):
        for zi in range(start_z, start_z + garden_depth):
            editor.placeBlock((xi, y, zi), Block(random.choice(flowers)))
    print("Flower garden added.")

def add_exterior_lighting(editor, x, y, z, width, depth):
    for (cx, cz) in [(x, z), (x + width - 1, z), (x, z + depth - 1), (x + width - 1, z + depth - 1)]:
        editor.placeBlock((cx, y + 2, cz), Block("minecraft:torch"))
    print("Exterior lighting placed.")

def build_washroom(editor, heightmap, min_x, min_z, x, y, z, width, depth, wall_height):
    side = random.choice(["left", "right"])
    wash_width = 5
    wash_depth = 4
    wash_wall_height = 4
    if side == "left":
        wash_x = x - (wash_width + 4)
        wash_z = z + 2
    else:
        wash_x = x + width + 3
        wash_z = z + 2
    for xi in range(wash_x - 1, wash_x + wash_width + 1):
        for zi in range(wash_z - 1, wash_z + wash_depth + 1):
            for yy in range(y, y + 6):
                editor.placeBlock((xi, yy, zi), Block("minecraft:air"))
    for xi in range(wash_x, wash_x + wash_width):
        for zi in range(wash_z, wash_z + wash_depth):
            editor.placeBlock((xi, y, zi), Block("minecraft:stone_bricks"))
    for level_y in range(y + 1, y + wash_wall_height + 1):
        for xi in range(wash_x, wash_x + wash_width):
            editor.placeBlock((xi, level_y, wash_z), Block("minecraft:oak_planks"))
            editor.placeBlock((xi, level_y, wash_z + wash_depth - 1), Block("minecraft:oak_planks"))
        for zi in range(wash_z + 1, wash_z + wash_depth - 1):
            editor.placeBlock((wash_x, level_y, zi), Block("minecraft:oak_planks"))
            editor.placeBlock((wash_x + wash_width - 1, level_y, zi), Block("minecraft:oak_planks"))
    roof_y = y + wash_wall_height + 1
    for xi in range(wash_x, wash_x + wash_width):
        for zi in range(wash_z, wash_z + wash_depth):
            editor.placeBlock((xi, roof_y, zi), Block("minecraft:glass"))
    center_x = wash_x + wash_width // 2
    center_z = wash_z + wash_depth // 2
    editor.placeBlock((center_x, roof_y - 1, center_z), Block("minecraft:sea_lantern"))
    door_x = wash_x + wash_width // 2
    door_z = wash_z
    editor.placeBlock((door_x, y + 1, door_z), Block("minecraft:air"))
    editor.placeBlock((door_x, y + 2, door_z), Block("minecraft:air"))
    editor.placeBlock((door_x, y + 1, door_z), Block("minecraft:oak_door", {"facing": "south", "half": "lower"}))
    editor.placeBlock((door_x, y + 2, door_z), Block("minecraft:oak_door", {"half": "upper"}))
    outside_z = door_z - 1
    editor.placeBlock((door_x, y, outside_z), Block("minecraft:stone"))
    editor.placeBlock((door_x, y + 1, outside_z), Block("minecraft:oak_pressure_plate"))
    inside_z = door_z + 1
    editor.placeBlock((door_x, y, inside_z), Block("minecraft:stone"))
    editor.placeBlock((door_x, y + 1, inside_z), Block("minecraft:oak_pressure_plate"))
    editor.placeBlock((door_x, y + 1, door_z + 2), Block("minecraft:oak_pressure_plate"))
    # Fill gap underneath the washroom with natural blocks
    fill_underneath(editor, heightmap, min_x, min_z, wash_x, y, wash_z, wash_width, wash_depth)
    sink_x = wash_x + wash_width // 2
    sink_z = wash_z + wash_depth // 2
    editor.placeBlock((sink_x, y + 1, sink_z), Block("minecraft:cauldron"))
    toilet_x = wash_x + 1
    toilet_z = wash_z + wash_depth - 2
    editor.placeBlock((toilet_x, y + 1, toilet_z), Block("minecraft:quartz_stairs", {"facing": "north"}))
    for (cx, cz) in [(wash_x, wash_z), (wash_x + wash_width - 1, wash_z),
                     (wash_x, wash_z + wash_depth - 1), (wash_x + wash_width - 1, wash_z + wash_depth - 1)]:
        editor.placeBlock((cx, y + 2, cz), Block("minecraft:torch"))
    print(f"Washroom built on the {side} side at ({wash_x}, {wash_z}).")
    return (door_x, door_z - 1)

def build_path(editor, x1, y, z1, x2, y2, z2):
    step_x = 1 if x2 >= x1 else -1
    path_end_x = x2 - step_x
    for cur_x in range(x1, path_end_x + step_x, step_x):
        editor.placeBlock((cur_x, y, z1), Block("minecraft:cobblestone"))
        for clear_y in range(y + 1, y + 4):
            editor.placeBlock((cur_x, clear_y, z1), Block("minecraft:air"))
    step_z = 1 if z2 >= z1 else -1
    path_end_z = z2 - step_z
    for cur_z in range(z1, path_end_z + step_z, step_z):
        editor.placeBlock((x2, y, cur_z), Block("minecraft:cobblestone"))
        for clear_y in range(y + 1, y + 4):
            editor.placeBlock((x2, clear_y, cur_z), Block("minecraft:air"))
    print("Connecting path built.")

def add_extra_decor(editor, x, y, z, width, depth):
    # Extra decoration: randomly add a decorative quartz column at the front center (50\% chance)
    if random.random() < 0.5:
        col_x = x + width // 2
        print("Adding decorative column at front center.")
        for y_off in range(1, 4):
            editor.placeBlock((col_x, y + y_off, z), Block("minecraft:quartz_block"))
    else:
        print("No extra decorative column added.")

def fill_underneath(editor, heightmap, min_x, min_z, start_x, base_y, start_z, width, depth):
    for xi in range(start_x, start_x + width):
        for zi in range(start_z, start_z + depth):
            local_x = xi - min_x
            local_z = zi - min_z
            terrain_height = int(heightmap[local_x][local_z])
            for fill_y in range(terrain_height + 1, base_y):
                editor.placeBlock((xi, fill_y, zi), Block("minecraft:grass_block"))
    print("Underneath gap filled with natural blocks.")

if __name__ == "__main__":
    main()
