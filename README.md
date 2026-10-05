# Procedural Farmhouse Generator for Minecraft

A procedural content generation project that builds randomized farmhouses in Minecraft Java Edition using Python and GDPC.

The generator analyzes terrain, selects a building location, and constructs a furnished farmhouse with a glass roof, outdoor decorations, and a separate washroom connected by a cobblestone path.

![Generated farmhouse](Front%20%281%29.png)

## Features

- **Terrain analysis:** Searches for suitable ground using heightmaps and allowed terrain blocks.
- **Randomized architecture:** Varies house dimensions, foundation materials, and wall materials.
- **Glass roof:** Provides an open view of the sky with sea-lantern lighting.
- **Furnished interior:** Includes bed blocks, bookshelves, a crafting table, a chest, and decorative features.
- **Pressure-plate entrances:** Adds doors with pressure plates.
- **Separate washroom:** Randomly places a washroom on the left or right of the house.
- **Outdoor details:** Generates a flower garden, exterior lighting, and a connecting path.
- **Buffered construction:** Batches block placement through GDPC.

## How It Works

1. Retrieve the configured Minecraft build area.
2. Load a world slice and its `MOTION_BLOCKING_NO_LEAVES` heightmap.
3. Select randomized dimensions and materials.
4. Search candidate locations for suitable ground and low height variation.
5. Prepare the footprint and construct the house.
6. Add furnishings, garden decorations, and lighting.
7. Build the washroom and connecting path.
8. Flush buffered changes to the Minecraft world.

If no suitable location is found, the script falls back to the build area's origin.

## Generation Settings

| Parameter | Current setting |
|-----------|-----------------|
| House width | 10–20 blocks |
| House depth | 8–16 blocks |
| Wall height | 4–8 blocks |
| Roof | Glass |
| Foundation and walls | Randomly selected material palettes |
| Washroom footprint | 5 × 4 blocks |
| Washroom position | Left or right |
| Garden depth | 4 blocks |
| Connecting path | Cobblestone |

## Screenshots

### Interior

![Farmhouse interior](inside%20%281%29.png)

### Overhead View

![Overhead view](top%20%281%29.png)

Additional screenshots show exterior, rear, and interior views.

## Requirements

- Minecraft Java Edition.
- A compatible GDMC HTTP Interface mod.
- Python and a compatible GDPC release.
- A running Minecraft world with a configured build area.

Refer to the official setup documentation:

- [GDPC installation](https://gdpc.readthedocs.io/en/stable/getting-started/installation.html)
- [GDMC HTTP Interface](https://github.com/Niels-NTG/gdmc_http_interface)

## Installation

```bash
git clone https://github.com/Praneeth-496/Procedural-Farmhouse-Generator-for-Minecraft.git
cd Procedural-Farmhouse-Generator-for-Minecraft
python -m pip install gdpc
```

## Usage

1. Launch Minecraft with the compatible interface mod.
2. Open a test world or a backup copy.
3. Configure the build area using your installed mod's build-area command.
4. Allow space for the house, washroom, garden, and path.
5. Run:

```bash
python mypcg.py
```

The script prints the selected dimensions, materials, location, and construction progress.

**The generator clears and replaces blocks in the world.**

## Customization

Edit `mypcg.py` to adjust:

| Setting | Location |
|---------|----------|
| House dimensions | `main()` |
| Foundation and wall palettes | `FOUNDATION_OPTIONS`, `WALL_OPTIONS` |
| Allowed terrain blocks | `find_flattest_spot()` |
| Interior layout | `furnish_interior()` |
| Washroom placement and dimensions | `build_washroom()` |
| Garden flowers | `add_flower_garden()` |
| Connecting path | `build_path()` |

For repeatable random choices, add the following before generation:

```python
random.seed(42)
```

Matching the complete output also requires the same initial terrain and build area.

## Repository Contents

| File | Description |
|------|-------------|
| `mypcg.py` | Terrain analysis and structure generation |
| `Praneeth__s4174089_Modern_AI_1_Report.pdf` | Project report |
| PNG screenshots | Examples of generated structures |
| `README.md` | Project documentation |

## Current Limitations

- Placement checks cover the main house footprint; the washroom, garden, and path may extend beyond the build area.
- Terrain adaptation uses heuristics, and the fallback location is not validated.
- Clearing height is fixed at six blocks even when taller walls are selected.
- Some block identifiers and multi-block object states require validation against the chosen Minecraft version.
- The TV, sink, and toilet are decorative block arrangements.
- Dependency and Minecraft versions are not pinned.

## Future Improvements

- Validate the entire compound footprint before construction.
- Improve terrain support and boundary handling.
- Add configurable seeds and architectural themes.
- Introduce alternative roofs, room layouts, and landscaping.
- Validate block identifiers and placement states automatically.

## Author

[Praneeth Dathu](https://github.com/Praneeth-496)

Developed for the Modern Game AI course at Leiden University.

## Acknowledgments

- GDPC contributors.
- GDMC HTTP Interface contributors.
