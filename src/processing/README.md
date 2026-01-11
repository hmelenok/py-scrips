# Processing Scripts

Data processing scripts for OCR-based marker detection and geospatial utilities.

## Scripts

### [detect-markers.py](detect-markers.py)
OCR-based marker detection and extraction from map images.

**Purpose**: Processes map images to extract text markers and match against known locations and drone types

**Features**:
- Image preprocessing: upscaling (2x), grayscaling, CLAHE contrast enhancement
- EasyOCR with Ukrainian and English language support
- Fuzzy string matching for location and drone type detection
- Latin to Ukrainian Cyrillic transliteration
- Automatic image cleanup after processing

**Input**:
- Images from `data/raw-data/map-parts/` (.png, .jpg, .jpeg)
- Location list from `data/reference-data/locations.txt`

**Output**:
- `output/csv/extracted_data.csv`: Extracted markers with location and drone type
- Optional: `output/images/map-parts-processed/`: Processed images (if enabled)

**Usage**:
```bash
python src/processing/detect-markers.py
```

**Dependencies**:
- opencv-python: Image processing
- easyocr: Optical character recognition
- pandas: Data manipulation
- fuzzywuzzy: Fuzzy string matching
- Pillow: Image I/O

### [locationUtils.js](locationUtils.js)
Geospatial utilities for location detection.

**Purpose**: Matches coordinates to known location polygons and calculates distances

**Features**:
- Point-in-polygon detection using ray casting algorithm
- Haversine distance calculations
- Finds closest location for any longitude|latitude point
- Optional distance display in Ukrainian

**Input**:
- `data/reference-data/locations_coords.csv`: Location polygon boundaries

**Functions**:
- `findClosestLocation(point, showByDistance)`: Returns location name for given coordinates
- `isPointInPolygon(point, polygon)`: Checks if point is within polygon
- `calculateDistance(lat1, lon1, lat2, lon2)`: Haversine distance in km

**Usage**:
```javascript
const { findClosestLocation } = require('./locationUtils.js');
const location = findClosestLocation('37.123|50.456', false);
```

## Data Flow

### Image Processing Pipeline
1. Read images from `data/raw-data/map-parts/`
2. Upscale and preprocess images
3. Extract text using EasyOCR
4. Match text against known locations and drone types
5. Save results to `output/csv/extracted_data.csv`
6. Remove processed images

### Location Matching
1. Load location polygons from `data/reference-data/locations_coords.csv`
2. For each coordinate point:
   - Check if point is within any polygon
   - If not, calculate distance to nearest polygon corners
   - Return closest location name
