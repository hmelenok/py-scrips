# Analysis Scripts

Visualization and analysis tools for geographic data.

## Scripts

### [plot.py](plot.py)
Visualizes geographic polygon coordinates.

**Purpose**: Creates matplotlib plots showing location boundaries as polygons

**Features**:
- Reads location coordinate data from CSV
- Plots each location as a closed polygon
- Supports multiple coordinate formats (pipe-delimited, comma-separated)
- Displays all locations with legend

**Input**:
- `data/reference-data/locations_coords.csv`: Location coordinates (NW, SW, SE, NE corners)

**Output**:
- Interactive matplotlib plot window

**Usage**:
```bash
python src/analysis/plot.py
```

**Dependencies**:
- matplotlib: Plotting library

## Coordinate Format

The script expects CSV with the following format:
```
Name,NW_coords,SW_coords,SE_coords,NE_coords
LocationName,lon|lat,lon|lat,lon|lat,lon|lat
```

Example:
```
Вовчанськ,36.9|50.3,36.9|50.2,37.0|50.2,37.0|50.3
```

## Visualization

- Each location is plotted as a connected polygon
- Markers at each corner point
- Color-coded by location
- Legend shows all location names
- Axes labeled with Longitude/Latitude
