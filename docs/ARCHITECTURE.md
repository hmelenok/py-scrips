# Architecture Overview

## System Components

The drone tracking system consists of four main functional categories:

### 1. Tracking (Real-time Data Ingestion)
- **Technology**: Node.js with WebSocket (ws library)
- **Purpose**: Real-time monitoring of unmanned aircraft positions
- **Protocol**: STOMP over WebSocket
- **Source**: Configurable WebSocket endpoint (via environment variables)

**Components**:
- WebSocket client with authentication
- STOMP message parser
- Data processor and filter
- Location matcher (uses geospatial processing)

### 2. Processing (Data Transformation)
- **Technologies**: Python (OpenCV, EasyOCR) and Node.js
- **Purpose**: Image OCR and geospatial calculations

**Components**:
- Image preprocessing pipeline (upscaling, grayscaling, contrast enhancement)
- OCR engine (EasyOCR with UK/EN support)
- Fuzzy string matching for entity recognition
- Point-in-polygon detection
- Distance calculations (Haversine formula)

### 3. Analysis (Visualization)
- **Technology**: Python (matplotlib)
- **Purpose**: Geographic data visualization

**Components**:
- Polygon plotting
- Coordinate visualization
- Multi-location comparison

### 4. Utilities (Supporting Tools)
- **Technology**: Python
- **Purpose**: File operations and text processing

**Components**:
- Batch file operations
- Character set analysis

## Data Flow Diagrams

### Real-time Tracking Pipeline

```
WebSocket Connection (configured server)
    |
    v
ws-client.js (STOMP protocol handling)
    |
    v
messageSender.js (subscription setup)
    |
    v
messageProcessor.js (data extraction)
    |
    v
locationUtils.js (geospatial matching)
    |
    v
Output Files (CSV + Text)
```

### Image Processing Pipeline

```
Raw Images (data/raw-data/map-parts/)
    |
    v
Image Preprocessing (upscale, grayscale, CLAHE)
    |
    v
OCR Extraction (EasyOCR: UK + EN)
    |
    v
Text Parsing & Fuzzy Matching
    |
    v
Entity Recognition (locations + drone types)
    |
    v
Transliteration (Latin to Cyrillic)
    |
    v
Output (output/csv/extracted_data.csv)
    |
    v
Cleanup (remove processed images)
```

## Technology Stack

### Node.js Components
- **Runtime**: Node.js 14+
- **WebSocket**: ws@^8.17.1
- **Protocol**: STOMP (v12, v11, v10)

### Python Components
- **Runtime**: Python 3.8+
- **Image Processing**: OpenCV, Pillow
- **OCR**: EasyOCR
- **Data**: pandas, numpy
- **Visualization**: matplotlib
- **Text Matching**: fuzzywuzzy

## Integration Points

### 1. WebSocket API
- **Endpoint**: Configurable via WEBSOCKET_URL environment variable
- **Authentication**: Cookie-based (AUTH_SESSIONID, SESSION)
- **Protocol**: STOMP over WebSocket
- **Data Format**: JSON within STOMP frames

### 2. File System
- **Configuration**: data/config/.env
- **Reference Data**: data/reference-data/ (locations, coordinates)
- **Input**: data/raw-data/ (images to process)
- **Output**: output/ (CSV, text, images, logs)

### 3. Shared Libraries
- **Python**: src/lib/python/ (file_utils, config_loader, logger)
- **Node.js**: src/lib/nodejs/ (fileUtils, configLoader, logger)

## Data Models

### Tracking Data (output/csv/data.csv)
```
id, latitude, longitude, name, creatingDateTime, observationDateTime, reportingDateTime, location
```

### Extracted Markers (output/csv/extracted_data.csv)
```
location, drone_type
```

### Location Coordinates (data/reference-data/locations_coords.csv)
```
Name, NW_coords, SW_coords, SE_coords, NE_coords
```
Format: `longitude|latitude` for each corner

### Simple Output (output/text/simple.txt)
```
Location - DroneTypeCode
```

## Security Considerations

### Authentication
- WebSocket requires valid session cookies
- Credentials stored in .env file (not committed to git)
- Environment variables loaded at runtime

### Data Privacy
- Output files git-ignored by default
- Logs excluded from version control
- No sensitive data hardcoded in scripts

## Performance Characteristics

### Real-time Tracking
- **Connection**: Persistent WebSocket with keep-alive (6s)
- **Data Rate**: Variable based on drone activity
- **Storage**: Rolling window of last 50 entries (prevents unbounded growth)
- **Deduplication**: By ID to avoid duplicates

### Image Processing
- **Batch Processing**: Sequential (one image at a time)
- **Image Size**: 2x upscaling increases processing time
- **OCR**: GPU-accelerated if available (EasyOCR)
- **Cleanup**: Automatic removal after processing

## Extensibility Points

### Adding New Scripts
1. Copy template from templates/
2. Place in appropriate category (tracking, processing, analysis, utils)
3. Import shared libraries
4. Follow established patterns

### Adding New Data Sources
1. Add new scripts to src/
2. Use shared libraries for paths
3. Write outputs to output/ subdirectories
4. Update documentation

### Adding New Output Formats
1. Extend messageProcessor.js or create new processor
2. Write to appropriate output/ subdirectory
3. Update .gitignore if needed

## Directory Structure Rationale

```
src/          - Source code by functionality
data/         - Input data by type (config, reference, raw)
output/       - Output artifacts by type (csv, images, logs, text)
templates/    - Development templates
docs/         - Documentation
```

**Benefits**:
- Clear separation of concerns
- Easy to find related functionality
- Scalable structure
- Git-friendly (outputs ignored, structure preserved)
