/**
 * File utilities for handling project paths.
 */

const path = require('path');
const fs = require('fs');

/**
 * Get the project root directory.
 * @returns {string} Project root path
 */
function getProjectRoot() {
    return path.join(__dirname, '..', '..', '..');
}

/**
 * Get path to data file.
 * @param {string} subdir - Subdirectory under data/ (e.g., 'config', 'reference-data', 'raw-data')
 * @param {string} filename - Name of the file
 * @returns {string} Full path to the data file
 */
function getDataPath(subdir, filename) {
    return path.join(getProjectRoot(), 'data', subdir, filename);
}

/**
 * Get path to output file.
 * @param {string} subdir - Subdirectory under output/ (e.g., 'csv', 'images', 'logs', 'text')
 * @param {string} filename - Name of the file
 * @returns {string} Full path to the output file
 */
function getOutputPath(subdir, filename) {
    return path.join(getProjectRoot(), 'output', subdir, filename);
}

/**
 * Ensure directory exists.
 * @param {string} dirPath - Path to directory
 */
function ensureDir(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
}

module.exports = { getProjectRoot, getDataPath, getOutputPath, ensureDir };
