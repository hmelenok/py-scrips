# Drone Tracking System

A comprehensive system for real-time drone tracking via WebSocket and map marker detection using OCR, with geospatial location matching capabilities.

## Features

- **Real-time Drone Tracking**: WebSocket client that monitors unmanned aircraft positions via configurable endpoint
- **Image Processing**: OCR-based marker detection and extraction from map images
- **Geospatial Analysis**: Point-in-polygon detection and distance calculations for location matching
- **Data Visualization**: Plotting tools for geographic coordinate visualization

## Directory Structure

```
py-scrips/
├── src/                    # Source code
│   ├── tracking/           # Real-time drone tracking scripts
│   ├── processing/         # Data processing and OCR
│   ├── analysis/           # Visualization and analysis
│   ├── utils/              # Utility scripts
│   └── lib/                # Shared libraries (Python & Node.js)
├── data/                   # Data files
│   ├── config/             # Configuration files
│   ├── reference-data/     # Reference data (locations, coordinates)
│   └── raw-data/           # Raw input data for processing
├── output/                 # All output artifacts
│   ├── csv/                # CSV outputs
│   ├── images/             # Processed images
│   ├── logs/               # Application logs
│   └── text/               # Text outputs
├── templates/              # Script templates for development
└── docs/                   # Documentation
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- pip and npm

### Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Configure environment (for tracking):
   ```bash
   cp data/config/.env.example data/config/.env
   # Edit .env and add your authentication credentials
   ```

### Running Scripts

**Real-time Tracking:**
```bash
npm start
# or
node src/tracking/ws-client.js
```

**Image Processing (OCR):**
```bash
python src/processing/detect-markers.py
```

**Visualization:**
```bash
python src/analysis/plot.py
```

**Utility Scripts:**
```bash
python src/utils/uniq-chars.py
python src/utils/rename.py
```

## Scripts Overview

### Tracking Scripts ([src/tracking/](src/tracking/))
- **ws-client.js**: Main WebSocket client for connecting to drone tracking system
- **messageProcessor.js**: Processes incoming STOMP messages and extracts drone data
- **messageSender.js**: Sends subscription and configuration messages

### Processing Scripts ([src/processing/](src/processing/))
- **detect-markers.py**: OCR-based marker detection from map images
- **locationUtils.js**: Geospatial utilities for location detection

### Analysis Scripts ([src/analysis/](src/analysis/))
- **plot.py**: Visualizes geographic polygon coordinates

### Utility Scripts ([src/utils/](src/utils/))
- **rename.py**: Batch file extension renaming
- **uniq-chars.py**: Character set extraction from text files

## Output Files

- **output/csv/data.csv**: Real-time drone tracking data (last 50 entries)
- **output/csv/extracted_data.csv**: OCR-extracted markers from images
- **output/text/simple.txt**: Simplified drone sightings (location - drone type)
- **output/logs/**: Application logs when enabled

## Development

### Adding New Scripts

See [docs/ADDING_NEW_SCRIPTS.md](docs/ADDING_NEW_SCRIPTS.md) for detailed instructions on extending the system with new scripts.

Templates are available in the [templates/](templates/) directory for both Python and Node.js scripts.

### Shared Libraries

All scripts have access to shared utilities:

**Python** ([src/lib/python/](src/lib/python/)):
- `file_utils.py`: Path management functions
- `config_loader.py`: Environment configuration loading
- `logger.py`: Standardized logging

**Node.js** ([src/lib/nodejs/](src/lib/nodejs/)):
- `fileUtils.js`: Path management functions
- `configLoader.js`: Environment configuration loading
- `logger.js`: Standardized logging

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Adding New Scripts](docs/ADDING_NEW_SCRIPTS.md)
- [Data Flows](docs/DATA_FLOWS.md)

## License

This project is for educational and monitoring purposes.
