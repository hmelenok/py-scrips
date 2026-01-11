/**
 * Logging utilities for standardized logging across scripts.
 */

const fs = require('fs');
const path = require('path');

/**
 * Logger class for standardized logging.
 */
class Logger {
    /**
     * Create a logger instance.
     * @param {string} name - Logger name
     * @param {string|null} logFile - Optional log file name (will be created in output/logs/)
     */
    constructor(name, logFile = null) {
        this.name = name;
        this.logFile = logFile;

        if (logFile) {
            const logDir = path.join(__dirname, '..', '..', '..', 'output', 'logs');
            if (!fs.existsSync(logDir)) {
                fs.mkdirSync(logDir, { recursive: true });
            }
            this.logPath = path.join(logDir, logFile);
        }
    }

    /**
     * Log a message with specified level.
     * @param {string} level - Log level (INFO, ERROR, DEBUG, etc.)
     * @param {string} message - Message to log
     */
    log(level, message) {
        const timestamp = new Date().toISOString();
        const logMessage = `${timestamp} - ${this.name} - ${level} - ${message}`;

        console.log(logMessage);

        if (this.logFile) {
            fs.appendFileSync(this.logPath, logMessage + '\n');
        }
    }

    /**
     * Log info message.
     * @param {string} message - Message to log
     */
    info(message) {
        this.log('INFO', message);
    }

    /**
     * Log error message.
     * @param {string} message - Message to log
     */
    error(message) {
        this.log('ERROR', message);
    }

    /**
     * Log debug message.
     * @param {string} message - Message to log
     */
    debug(message) {
        this.log('DEBUG', message);
    }
}

module.exports = { Logger };
