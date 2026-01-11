# Utility Scripts

General-purpose utility scripts for file operations and text processing.

## Scripts

### [rename.py](rename.py)
Batch file extension renaming utility.

**Purpose**: Renames file extensions in bulk within a directory

**Usage**:
Modify the script to specify:
- Target directory
- Old extension
- New extension

```bash
python src/utils/rename.py
```

**Use Cases**:
- Converting annotation file formats
- Bulk file type changes
- Organizing training data

### [uniq-chars.py](uniq-chars.py)
Character set extraction from text files.

**Purpose**: Extracts all unique characters from text files in a directory

**Features**:
- Scans all .txt files in specified directory
- Extracts unique characters
- Sorts characters
- UTF-8 encoding support

**Input**:
- Text files in `training-annotations/` directory (or as configured)

**Output**:
- `output/text/unique_chars.txt`: Sorted unique character set

**Usage**:
```bash
python src/utils/uniq-chars.py
```

**Use Cases**:
- Character set analysis for OCR training
- Text corpus analysis
- Font coverage verification

## Configuration

Both scripts use hardcoded paths that can be modified:

**rename.py**:
```python
directory = 'path/to/directory'
old_ext = '.png'
new_ext = '.txt'
```

**uniq-chars.py**:
```python
directory_path = 'training-annotations'
output_file_path = '../../output/text/unique_chars.txt'
```
