# Data Flows

This document describes the data pipelines and transformations in the system.

## Overview

The system has two main data pipelines:
1. **Real-time Tracking Pipeline**: Ingests live drone position data via WebSocket
2. **Image Processing Pipeline**: Extracts markers from map images using OCR

## Real-time Tracking Pipeline

### Flow Diagram

```
┌─────────────────────────────────────────────────┐
│ WebSocket Server                                │
│ wss://delta.mil.gov.ua/updates/events/websocket│
└──────────────────┬──────────────────────────────┘
                   │ STOMP over WebSocket
                   ▼
┌─────────────────────────────────────────────────┐
│ ws-client.js                                    │
│ - Establishes connection                        │
│ - Handles authentication                        │
│ - Maintains keep-alive                          │
└──────────────────┬──────────────────────────────┘
                   │ Connection established
                   ▼
┌─────────────────────────────────────────────────┐
│ messageSender.js                                │
│ - Sends subscription messages                   │
│ - Configures locale (Ukrainian)                 │
│ - Subscribes to feed-collection (sub-9)         │
└──────────────────┬──────────────────────────────┘
                   │ Subscriptions active
                   ▼
┌─────────────────────────────────────────────────┐
│ Incoming STOMP Messages                         │
│ subscription: sub-9                             │
│ destination: /user/exchange/amq.direct/feed-... │
└──────────────────┬──────────────────────────────┘
                   │ JSON payload
                   ▼
┌─────────────────────────────────────────────────┐
│ messageProcessor.js                             │
│ - Parses STOMP frame                            │
│ - Extracts JSON array                           │
│ - Filters for:                                  │
│   * source.name = "GRAPHITE"                    │
│   * action = "UPDATED"                          │
│   * typeName contains "Безпілотний літак"       │
└──────────────────┬──────────────────────────────┘
                   │ Filtered drone data
                   ▼
┌─────────────────────────────────────────────────┐
│ Extract Fields                                  │
│ - id                                            │
│ - latitude, longitude                           │
│ - name (drone type)                             │
│ - creatingDateTime                              │
│ - observationDateTime                           │
│ - reportingDateTime                             │
└──────────────────┬──────────────────────────────┘
                   │ longitude|latitude
                   ▼
┌─────────────────────────────────────────────────┐
│ locationUtils.js (from processing/)             │
│ - findClosestLocation()                         │
│ - Point-in-polygon detection                    │
│ - Distance calculations                         │
└──────────────────┬──────────────────────────────┘
                   │ Location name
                   ▼
┌─────────────────────────────────────────────────┐
│ Data Persistence                                │
│ - Merge with existing data                      │
│ - Deduplicate by ID                             │
│ - Keep last 50 entries                          │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌────────────────┐    ┌────────────────┐
│ output/csv/    │    │ output/text/   │
│ data.csv       │    │ simple.txt     │
│                │    │                │
│ Full details   │    │ Location -     │
│ CSV format     │    │ DroneType      │
└────────────────┘    └────────────────┘
```

### Data Transformations

#### Input Format (STOMP Message)
```
STOMP frame header...

[{
  "id": "abc123",
  "source": {"name": "GRAPHITE"},
  "action": "UPDATED",
  "typeName": "Безпілотний літак: Орлан-10",
  "name": "Орлан-10",
  "geometry": {
    "absolutePointLatitudeCoordinate": {
      "latitudeCoordinateCoordinate": 50.123
    },
    "absolutePointLongitudeCoordinate": {
      "longitudeCoordinateCoordinate": 37.456
    }
  },
  "creatingDateTime": 1234567890000,
  "observationDateTime": 1234567891000,
  "reportingDateTime": 1234567892000
}, ...]
```

#### Intermediate Format (Processed)
```javascript
{
  id: "abc123",
  latitude: 50.123,
  longitude: 37.456,
  name: "Орлан-10",
  creatingDateTime: "12:34:56",
  observationDateTime: "12:35:01",
  reportingDateTime: "12:35:02",
  location: "Вовчанськ"
}
```

#### Output Format (data.csv)
```
abc123,50.123,37.456,Орлан-10,12:34:56,12:35:01,12:35:02,Вовчанськ
```

#### Output Format (simple.txt)
```
Вовчанськ - Орлан-10
```

### Location Matching Logic

**Reference Data** (data/reference-data/locations_coords.csv):
```
Name,NW_coords,SW_coords,SE_coords,NE_coords
Вовчанськ,36.9|50.3,36.9|50.2,37.0|50.2,37.0|50.3
```

**Algorithm**:
1. For given point (longitude|latitude)
2. Check if point is inside any location polygon (ray casting algorithm)
3. If inside, return location name
4. If outside all polygons, calculate distance to nearest polygon corners (Haversine)
5. Return name of closest location

**Distance Calculation** (Haversine Formula):
```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1−a))
distance = R × c  (where R = 6371 km)
```

### Rolling Window Logic

**Purpose**: Prevent unbounded data growth

**Implementation**:
1. Read existing data from file
2. Merge with new data
3. Deduplicate by ID (keeping latest entry)
4. Slice to last 50 entries
5. Write back to file

```javascript
const mergedData = {};
[...existingData, ...newData].forEach(row => {
    const [id] = row.split(',');
    mergedData[id] = row;  // Latest entry wins
});

const finalData = Object.values(mergedData).slice(-50);
```

## Image Processing Pipeline

### Flow Diagram

```
┌─────────────────────────────────────────────────┐
│ Input Images                                    │
│ data/raw-data/map-parts/*.{png,jpg,jpeg}       │
└──────────────────┬──────────────────────────────┘
                   │ For each image
                   ▼
┌─────────────────────────────────────────────────┐
│ Image Preprocessing                             │
│ - Load image (PIL)                              │
│ - Upscale 2x (BICUBIC interpolation)           │
│ - Convert to grayscale                          │
│ - CLAHE contrast enhancement                    │
└──────────────────┬──────────────────────────────┘
                   │ Preprocessed numpy array
                   ▼
┌─────────────────────────────────────────────────┐
│ EasyOCR                                         │
│ - Languages: Ukrainian, English                 │
│ - Extract text regions and confidence           │
│ - Concatenate all text                          │
└──────────────────┬──────────────────────────────┘
                   │ Extracted text
                   ▼
┌─────────────────────────────────────────────────┐
│ Text Parsing & Matching                         │
│ - Split text into words                         │
│ - Fuzzy match against known locations (60%)     │
│ - Fuzzy match against known drones (90%)        │
│ - Select best matches                           │
└──────────────────┬──────────────────────────────┘
                   │ Matched entities
                   ▼
┌─────────────────────────────────────────────────┐
│ Transliteration                                 │
│ - Convert Latin to Ukrainian Cyrillic           │
│ - Capitalize drone type                         │
└──────────────────┬──────────────────────────────┘
                   │ Normalized data
                   ▼
┌─────────────────────────────────────────────────┐
│ Data Accumulation                               │
│ - Append to results list                        │
│ - Convert to pandas DataFrame                   │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌────────────────┐    ┌────────────────┐
│ output/csv/    │    │ File Cleanup   │
│ extracted_     │    │ Remove         │
│ data.csv       │    │ processed      │
│                │    │ images         │
└────────────────┘    └────────────────┘
```

### Data Transformations

#### Input (Image File)
- Format: PNG, JPG, JPEG
- Location: `data/raw-data/map-parts/image001.png`
- Content: Map with text markers

#### Preprocessing
1. **Upscaling**: 2x size using BICUBIC interpolation (improves OCR accuracy)
2. **Grayscale**: Convert to single channel (reduces complexity)
3. **CLAHE**: Contrast Limited Adaptive Histogram Equalization (enhances text visibility)

#### OCR Output
```python
[
  (bbox, "Вовчанськ", confidence),
  (bbox, "ORLAN", confidence),
  ...
]
```

Concatenated: `"Вовчанськ ORLAN ..."`

#### Fuzzy Matching

**Known Locations** (from data/reference-data/locations.txt):
```
Вовчанськ
Лиман
Покаляне
...
```

**Known Drones**:
```python
["ORLAN", "SUPERCAM", "ZALA", "Орлан", "зала", "Зала", "Суперкам"]
```

**Fuzzy Match**:
- Extract best match above threshold
- Locations: 60% similarity required
- Drones: 90% similarity required

#### Transliteration Map
```python
{
  'O': 'О', 'R': 'Р', 'L': 'Л', 'A': 'А', 'N': 'Н',
  # ... (full map in detect-markers.py)
}
```

"ORLAN" → "Орлан" (capitalized)

#### Output Format (extracted_data.csv)
```
location,drone_type
Вовчанськ,Орлан
Лиман,Зала
```

### Image Cleanup

After processing, all images in `data/raw-data/map-parts/` are removed to:
- Save disk space
- Prevent reprocessing
- Keep input directory clean

Optional: Save processed images to `output/images/map-parts-processed/` (disabled by default)

## Reference Data

### locations.txt
**Purpose**: List of known location names for fuzzy matching

**Format**: One location per line
```
Бочкове
Покаляне
Юрченкове
Вовчанськ
Лиман
...
```

**Usage**: Loaded by detect-markers.py for fuzzy matching

### locations_coords.csv
**Purpose**: Geographic boundaries for location detection

**Format**: CSV with 5 columns
```
Name,NW_coords,SW_coords,SE_coords,NE_coords
LocationName,lon|lat,lon|lat,lon|lat,lon|lat
```

**Coordinate System**: WGS84 (longitude|latitude)

**Usage**:
- Loaded by locationUtils.js for point-in-polygon detection
- Loaded by plot.py for visualization

**Example**:
```
Вовчанськ,36.9|50.3,36.9|50.2,37.0|50.2,37.0|50.3
```
Defines a rectangular polygon with four corners (NW, SW, SE, NE)

## Output Files

### data.csv (output/csv/)
**Format**: CSV without header
**Columns**: id, latitude, longitude, name, creatingDateTime, observationDateTime, reportingDateTime, location
**Size**: Rolling window of last 50 unique entries
**Deduplication**: By ID
**Update Frequency**: Real-time (whenever new data arrives)

### simple.txt (output/text/)
**Format**: Plain text
**Pattern**: `Location - DroneTypeCode`
**Size**: Last 50 unique entries
**Deduplication**: Exact match
**Update Frequency**: Real-time

### extracted_data.csv (output/csv/)
**Format**: CSV with header
**Columns**: location, drone_type
**Size**: All extractions from current batch
**Update Frequency**: After each batch of images processed

### unique_chars.txt (output/text/)
**Format**: Plain text, sorted characters
**Purpose**: Character set analysis for OCR training
**Update Frequency**: Manual (run uniq-chars.py)

## Performance Characteristics

### Real-time Tracking
- **Latency**: Sub-second from WebSocket message to file write
- **Throughput**: Depends on incoming message rate
- **Memory**: O(1) - fixed size rolling window
- **Disk**: O(1) - fixed size files (last 50 entries)

### Image Processing
- **Speed**: ~2-10 seconds per image (depends on size and content)
- **Bottleneck**: OCR processing
- **Memory**: Single image in memory at a time
- **Disk**: Input images deleted after processing

## Error Handling

### Real-time Tracking
- **Connection Loss**: Auto-reconnect handled by ws library
- **Parse Errors**: Logged but don't crash the process
- **File Write Errors**: Logged as errors

### Image Processing
- **OCR Failures**: Logged, script continues to next image
- **Invalid Images**: Skipped
- **No Matches**: Empty entries in output (still logged)

## Data Retention

- **Tracking Data**: Last 50 entries only (rolling window)
- **Extracted Data**: Cumulative per batch, then replaced
- **Processed Images**: Deleted immediately
- **Logs**: Retained indefinitely (manual cleanup required)

## Integration Points

### Shared Data
- Location coordinates used by both tracking and analysis
- Location names used by both processing and tracking

### Cross-Pipeline Dependencies
- locationUtils.js used by tracking pipeline for real-time matching
- Reference data (locations.txt, locations_coords.csv) used by multiple pipelines
