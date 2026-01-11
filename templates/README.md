# Script Templates

This directory contains templates for creating new scripts in the project.

## Available Templates

### Python Template (`python_script_template.py`)

Template for creating new Python scripts with:
- Standardized imports and setup
- Logging configuration
- Path utilities for accessing data and output directories
- Error handling structure

**Usage:**

1. Copy the template:
   ```bash
   cp templates/python_script_template.py src/<category>/your_script.py
   ```

2. Update the template placeholders:
   - `[SCRIPT_NAME]` - Name of your script
   - `[DESCRIPTION]` - Brief description of what the script does
   - `[AUTHOR]` - Your name
   - `[DATE]` - Current date

3. Replace `script_name.log` with an appropriate log file name

4. Implement your logic in the `main()` function

### Node.js Template (`nodejs_script_template.js`)

Template for creating new Node.js scripts with:
- Standardized imports and setup
- Logging configuration
- Path utilities for accessing data and output directories
- Error handling structure

**Usage:**

1. Copy the template:
   ```bash
   cp templates/nodejs_script_template.js src/<category>/your_script.js
   ```

2. Update the template placeholders:
   - `[SCRIPT_NAME]` - Name of your script
   - `[DESCRIPTION]` - Brief description of what the script does
   - `[AUTHOR]` - Your name
   - `[DATE]` - Current date

3. Replace `'ScriptName'` and `'script_name.log'` with appropriate names

4. Implement your logic in the `main()` function

## Best Practices

1. **Use Shared Libraries**: Always import and use the shared utilities from `src/lib/`
2. **Logging**: Enable file logging for production scripts to track execution
3. **Error Handling**: Keep the try-catch structure for proper error reporting
4. **Path Management**: Use `getDataPath()` and `getOutputPath()` instead of hardcoded paths
5. **Configuration**: Load environment variables using `loadConfig()` when needed
6. **Documentation**: Update the docstring/comments with accurate information

## Example

After customization, your script header should look like:

```python
"""
Script Name: Analyze User Metrics
Description: Analyzes user activity metrics and generates reports
Author: John Doe
Date: 2024-01-15
"""
```

For more information on adding new scripts, see [docs/ADDING_NEW_SCRIPTS.md](../docs/ADDING_NEW_SCRIPTS.md).
