# Adding New Scripts

This guide explains how to extend the system with new scripts following the established patterns and conventions.

## Step-by-Step Guide

### 1. Choose the Right Category

Place your script in the appropriate directory based on its functionality:

- **src/tracking/**: Real-time data ingestion, WebSocket connections, streaming data
- **src/processing/**: Data transformation, OCR, geospatial calculations, batch processing
- **src/analysis/**: Visualization, reporting, data analysis
- **src/utils/**: General utilities, file operations, helper scripts

### 2. Copy the Template

Choose the appropriate template based on your language:

**Python**:
```bash
cp templates/python_script_template.py src/<category>/your_script.py
```

**Node.js**:
```bash
cp templates/nodejs_script_template.js src/<category>/your_script.js
```

### 3. Update Script Metadata

Replace the placeholders in your new script:

```python
# Python example
"""
Script Name: Drone Activity Analyzer
Description: Analyzes drone activity patterns and generates summary reports
Author: Your Name
Date: 2024-01-15
"""
```

```javascript
// Node.js example
/**
 * Script Name: WebSocket Monitor
 * Description: Monitors WebSocket connection health and logs statistics
 * Author: Your Name
 * Date: 2024-01-15
 */
```

### 4. Use Shared Libraries

Import and use the shared utilities for consistent path handling:

**Python**:
```python
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib" / "python"))

from file_utils import get_data_path, get_output_path, ensure_dir
from config_loader import load_config
from logger import setup_logger

# Get path to input file
input_file = get_data_path("reference-data", "locations.txt")

# Get path to output file
output_file = get_output_path("csv", "analysis_results.csv")

# Ensure output directory exists
ensure_dir(output_file.parent)
```

**Node.js**:
```javascript
const { getDataPath, getOutputPath, ensureDir } = require('../lib/nodejs/fileUtils');
const { loadConfig } = require('../lib/nodejs/configLoader');
const { Logger } = require('../lib/nodejs/logger');

// Get path to input file
const inputFile = getDataPath('reference-data', 'locations.txt');

// Get path to output file
const outputFile = getOutputPath('csv', 'analysis_results.csv');

// Ensure output directory exists
ensureDir(path.dirname(outputFile));
```

### 5. Implement Your Logic

Add your script's functionality in the main function:

**Python**:
```python
def main():
    """Main function."""
    logger.info("Script started")

    try:
        # Load configuration if needed
        config = load_config()

        # Your code here
        # ...

        logger.info("Processing completed successfully")

    except Exception as e:
        logger.error(f"Error: {e}")
        raise

    logger.info("Script completed")
```

**Node.js**:
```javascript
async function main() {
    logger.info('Script started');

    try {
        // Load configuration if needed
        const config = loadConfig();

        // Your code here
        // ...

        logger.info('Processing completed successfully');

    } catch (error) {
        logger.error(`Error: ${error.message}`);
        throw error;
    }

    logger.info('Script completed');
}
```

### 6. Enable Logging (Optional but Recommended)

Use the logger for production scripts:

**Python**:
```python
logger = setup_logger(__name__, "your_script.log")
```

**Node.js**:
```javascript
const logger = new Logger('YourScript', 'your_script.log');
```

Logs will be saved to `output/logs/your_script.log`

### 7. Test Your Script

Run your script to ensure it works correctly:

```bash
# Python
python src/<category>/your_script.py

# Node.js
node src/<category>/your_script.js
```

### 8. Add to package.json (Optional)

For frequently used scripts, add npm scripts:

```json
{
  "scripts": {
    "your-command": "node src/<category>/your_script.js"
  }
}
```

Then run with: `npm run your-command`

### 9. Document Your Script

Create or update the README.md in your category directory:

```markdown
### [your_script.py](your_script.py)
Brief description of what the script does.

**Purpose**: Detailed explanation

**Features**:
- Feature 1
- Feature 2

**Input**:
- Input files and their locations

**Output**:
- Output files and their locations

**Usage**:
\`\`\`bash
python src/<category>/your_script.py
\`\`\`

**Dependencies**:
- List of special dependencies
```

## Best Practices

### Path Management
- **DO** use `get_data_path()` and `get_output_path()` for all file access
- **DON'T** use hardcoded relative or absolute paths
- **DO** use `ensure_dir()` to create directories as needed

### Configuration
- **DO** use environment variables for sensitive data
- **DO** load config using `load_config()`
- **DON'T** hardcode credentials or API keys

### Error Handling
- **DO** use try-catch blocks for error handling
- **DO** log errors before re-raising
- **DO** provide meaningful error messages

### Logging
- **DO** enable file logging for production scripts
- **DO** log important events (start, completion, errors)
- **DON'T** log sensitive information

### Code Organization
- **DO** keep functions focused and single-purpose
- **DO** add docstrings/comments for complex logic
- **DON'T** create monolithic functions

### Dependencies
- **DO** add new dependencies to requirements.txt (Python) or package.json (Node.js)
- **DO** specify version ranges
- **DO** document special dependencies in your script's README

## Examples

### Example 1: Data Processing Script

```python
#!/usr/bin/env python3
"""
Script Name: Activity Aggregator
Description: Aggregates drone activity data by location and time period
Author: Your Name
Date: 2024-01-15
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "lib" / "python"))

from file_utils import get_data_path, get_output_path, ensure_dir
from logger import setup_logger

logger = setup_logger(__name__, "activity_aggregator.log")


def aggregate_by_location(df):
    """Aggregate data by location."""
    return df.groupby('location').size().reset_index(name='count')


def main():
    logger.info("Activity aggregation started")

    try:
        # Read input data
        input_file = get_output_path("csv", "data.csv")
        df = pd.read_csv(input_file, header=None,
                        names=['id', 'latitude', 'longitude', 'name',
                               'creatingDateTime', 'observationDateTime',
                               'reportingDateTime', 'location'])

        # Aggregate
        aggregated = aggregate_by_location(df)

        # Save results
        output_file = get_output_path("csv", "activity_summary.csv")
        ensure_dir(output_file.parent)
        aggregated.to_csv(output_file, index=False)

        logger.info(f"Results saved to {output_file}")

    except Exception as e:
        logger.error(f"Error: {e}")
        raise

    logger.info("Activity aggregation completed")


if __name__ == "__main__":
    main()
```

### Example 2: Monitoring Script

```javascript
/**
 * Script Name: Connection Monitor
 * Description: Monitors WebSocket connection and logs statistics
 * Author: Your Name
 * Date: 2024-01-15
 */

const { Logger } = require('../lib/nodejs/logger');
const { getOutputPath } = require('../lib/nodejs/fileUtils');
const fs = require('fs');

const logger = new Logger('ConnectionMonitor', 'connection_monitor.log');

class ConnectionMonitor {
    constructor() {
        this.stats = {
            messagesReceived: 0,
            errors: 0,
            startTime: Date.now()
        };
    }

    logStats() {
        const runtime = (Date.now() - this.stats.startTime) / 1000;
        const rate = this.stats.messagesReceived / runtime;

        logger.info(`Stats: ${this.stats.messagesReceived} messages in ${runtime}s (${rate.toFixed(2)} msg/s)`);

        // Save to file
        const outputFile = getOutputPath('text', 'connection_stats.txt');
        fs.writeFileSync(outputFile, JSON.stringify(this.stats, null, 2));
    }

    incrementMessages() {
        this.stats.messagesReceived++;
    }

    incrementErrors() {
        this.stats.errors++;
    }
}

async function main() {
    logger.info('Connection monitor started');

    const monitor = new ConnectionMonitor();

    // Set up periodic stats logging
    setInterval(() => {
        monitor.logStats();
    }, 60000); // Every minute

    // Your monitoring logic here
    // ...
}

main().catch(error => {
    logger.error(`Fatal error: ${error.message}`);
    process.exit(1);
});
```

## Common Patterns

### Reading CSV Files

**Python**:
```python
import pandas as pd
input_file = get_data_path("reference-data", "locations_coords.csv")
df = pd.read_csv(input_file)
```

**Node.js**:
```javascript
const fs = require('fs');
const inputFile = getDataPath('reference-data', 'locations_coords.csv');
const data = fs.readFileSync(inputFile, 'utf8');
const lines = data.split('\n');
```

### Writing Output Files

**Python**:
```python
output_file = get_output_path("csv", "results.csv")
ensure_dir(output_file.parent)
df.to_csv(output_file, index=False)
```

**Node.js**:
```javascript
const outputFile = getOutputPath('csv', 'results.csv');
ensureDir(path.dirname(outputFile));
fs.writeFileSync(outputFile, csvData);
```

### Environment Configuration

**Python**:
```python
config = load_config()
api_key = os.getenv('API_KEY')
```

**Node.js**:
```javascript
const config = loadConfig();
const apiKey = process.env.API_KEY;
```

## Troubleshooting

### Import Errors (Python)
If you get import errors, ensure the path to lib is correct:
```python
sys.path.insert(0, str(Path(__file__).parent.parent / "lib" / "python"))
```

### Module Not Found (Node.js)
Ensure relative paths are correct based on your script location:
```javascript
require('../lib/nodejs/fileUtils')  // from src/<category>/
require('../../lib/nodejs/fileUtils')  // from deeper nesting
```

### Output Directory Doesn't Exist
Always use `ensure_dir()` before writing files:
```python
ensure_dir(output_file.parent)  # Python
```
```javascript
ensureDir(path.dirname(outputFile));  // Node.js
```

## Getting Help

- Review existing scripts in the same category
- Check the templates/ directory for examples
- Read the [Architecture Overview](ARCHITECTURE.md)
- Review shared library implementations in src/lib/
