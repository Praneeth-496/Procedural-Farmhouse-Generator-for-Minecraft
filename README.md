# Procedural Farmhouse Generator for Minecraft

A Python-based procedural content generation system that creates unique, nature-integrated farmhouses in Minecraft using the GDPC package.

## Project Overview

This project implements a procedural generation system that creates farmhouses in Minecraft with the following features:
- Terrain analysis to find suitable building locations
- Randomized dimensions and materials for unique structures
- Transparent mirror surfaces on roofs and walls for sky viewing
- Integrated washroom with automated doors
- L-shaped connecting path between main house and washroom
- Interior furnishings including beds, crafting table, chest, bookshelves, TV, and heater
- Exterior decorations including flower gardens and lighting

## Features

### Terrain Analysis
- Evaluates build areas (typically 100x100 blocks) using GDPC's MOTION_BLOCKING_NO_LEAVES heightmap
- Identifies flat regions with natural blocks (grass, dirt, stone)
- Calculates height differences to ensure suitable building locations

### Randomization and Variation
- Randomized dimensions (width: 10-20 blocks, depth: 8-16 blocks, wall height: 4-8 blocks)
- Random material selection for foundations and walls
- Transparent glass roofs for mirror-like effects
- Random washroom placement (left or right side)

### Integration with Environment
- Selective clearing that preserves the natural landscape
- Foundation filling to ensure structure stability
- Interior and exterior decorations for a believable living space

## Implementation

The system is built using:
- Python
- GDPC (Generative Design in Minecraft Python Client)
- Minecraft Java Edition

## Results

Each execution produces a unique farmhouse that:
- Adapts to the natural terrain
- Features randomized dimensions and materials
- Includes transparent surfaces for sky viewing
- Contains an attached washroom with automated doors
- Provides interior furnishings and exterior decorations

## Installation

1. Install Python 3.7 or higher
2. Install Minecraft Java Edition
3. Install the GDPC package:
   ```
   pip install gdpc
   ```
4. Clone this repository:
   ```
   git clone https://github.com/yourusername/procedural-farmhouse-generator.git
   ```

## Usage

1. Start Minecraft with the GDPC interface mod
2. Run the generator script:
   ```
   python farmhouse_generator.py
   ```
3. The script will analyze the terrain, select a suitable location, and generate a unique farmhouse

## Configuration

You can modify the following parameters in the script:
- Build area size (default: 100x100 blocks)
- Dimension ranges for width, depth, and height
- Material selection pools for foundations and walls
- Interior and exterior decoration options

## Screenshots

The repository includes several screenshots showing:
- Front view of generated farmhouses
- Interior views showing furnishings
- Back views showing garden areas
- Top views demonstrating roof transparency

## Author

Praneeth Dathu

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Modern Game AI course at Leiden University
- GDPC development team for their Minecraft interface tools

