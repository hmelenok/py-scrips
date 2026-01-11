/**
 * Configuration loader for environment variables.
 */

const fs = require('fs');
const path = require('path');

/**
 * Load environment configuration from .env file.
 * @returns {object} process.env with loaded variables
 */
function loadConfig() {
    const configPath = path.join(__dirname, '..', '..', '..', 'data', 'config', '.env');

    if (fs.existsSync(configPath)) {
        const content = fs.readFileSync(configPath, 'utf-8');
        content.split('\n').forEach(line => {
            line = line.trim();
            if (line && !line.startsWith('#') && line.includes('=')) {
                const [key, ...valueParts] = line.split('=');
                const value = valueParts.join('='); // Handle values with '='
                if (key && value) {
                    process.env[key.trim()] = value.trim();
                }
            }
        });
    }

    return process.env;
}

module.exports = { loadConfig };
