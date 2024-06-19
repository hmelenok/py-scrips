// locationUtils.js
const fs = require('fs');

const coordinatesData = fs.readFileSync('locations_coords.csv', 'utf8');
const coordinatesLines = coordinatesData.split('\n').slice(1);
const coordinatesMap = new Map();

coordinatesLines.forEach(line => {
    const [name, nw, sw, se, ne] = line.split(',');
    coordinatesMap.set(name, { nw, sw, se, ne });
});

function isPointInPolygon(point, polygon) {
    const [x, y] = point.split('|').map(parseFloat);
    const polygonPoints = [polygon.nw, polygon.sw, polygon.se, polygon.ne].map(p => p.split('|').map(parseFloat));

    let inside = false;
    for (let i = 0, j = polygonPoints.length - 1; i < polygonPoints.length; j = i++) {
        const xi = polygonPoints[i][0], yi = polygonPoints[i][1];
        const xj = polygonPoints[j][0], yj = polygonPoints[j][1];

        const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }

    return inside;
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    return distance;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function findClosestLocation(point, showByDistance) {
    let closestLocation = null;
    let minDistance = Infinity;

    coordinatesMap.forEach((polygon, name) => {
        if (isPointInPolygon(point, polygon)) {
            closestLocation = name;
            minDistance = 0;
        } else {
            const [x, y] = point.split('|').map(parseFloat);
            const [nwX, nwY] = polygon.nw.split('|').map(parseFloat);
            const [swX, swY] = polygon.sw.split('|').map(parseFloat);
            const [seX, seY] = polygon.se.split('|').map(parseFloat);
            const [neX, neY] = polygon.ne.split('|').map(parseFloat);

            const distances = [
                calculateDistance(y, x, nwY, nwX),
                calculateDistance(y, x, swY, swX),
                calculateDistance(y, x, seY, seX),
                calculateDistance(y, x, neY, neX)
            ];

            const distance = Math.min(...distances);
            if (distance < minDistance) {
                closestLocation = name;
                minDistance = distance;
            }
        }
    });

    if (minDistance > 0 && showByDistance) {
        const distanceInKm = Math.round(minDistance * 100) / 100;
        return `${closestLocation} (близько ${distanceInKm}км)`;
    }

    return closestLocation;
}

module.exports = {
    findClosestLocation
};
