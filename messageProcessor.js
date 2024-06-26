// messageProcessor.js
const fs = require('fs');

function processMessage(message, findClosestLocation, showByDistance) {
    if (message.includes("subscription:sub-9") && message.includes("destination:/user/exchange/amq.direct/feed-collection")) {
        const jsonData = message.split('\n\n')[1].trim().replace(' ', '');
        const jsonArray = JSON.parse(jsonData);

        const filteredData = jsonArray.filter(item =>
            item.source.name === "GRAPHITE" &&
            item.action === "UPDATED" &&
            item.typeName.includes("Безпілотний літак")
        );

        const csvRows = [];
        const simpleTextLines = [];
        const uniqueMarkers = {};

        filteredData.forEach(item => {
            const latitude = item.geometry.absolutePointLatitudeCoordinate.latitudeCoordinateCoordinate;
            const longitude = item.geometry.absolutePointLongitudeCoordinate.longitudeCoordinateCoordinate;
            const point = `${longitude}|${latitude}`;
            const location = findClosestLocation(point, showByDistance);

            const creatingDateTime = new Date(item.creatingDateTime).toLocaleTimeString('en-US', { hour12: false });
            const observationDateTime = item.observationDateTime !== -1 ? new Date(item.observationDateTime).toLocaleTimeString('en-US', { hour12: false }) : '';
            const reportingDateTime = new Date(item.reportingDateTime).toLocaleTimeString('en-US', { hour12: false });

            if (uniqueMarkers[item.id]) {
                uniqueMarkers[item.id] = `${item.id},${latitude},${longitude},${item.name},${creatingDateTime},${observationDateTime},${reportingDateTime},${location}`;
            } else {
                uniqueMarkers[item.id] = `${item.id},${latitude},${longitude},${item.name},${creatingDateTime},${observationDateTime},${reportingDateTime},${location}`;
            }

            simpleTextLines.push(`${location} - ${item.name.split(' ')[0]}`);
        });

        const updatedData = Object.values(uniqueMarkers);

        let existingData = [];
        if (fs.existsSync('data.csv')) {
            const fileData = fs.readFileSync('data.csv', 'utf8');
            existingData = fileData.split('\n').filter(row => row.trim() !== '');
        }

        const mergedData = {};
        [...existingData, ...updatedData].forEach(row => {
            const [id] = row.split(',');
            mergedData[id] = row;
        });

        const finalData = Object.values(mergedData);

        const lastEntries = finalData.slice(-50);

        fs.writeFileSync('data.csv', lastEntries.join('\n'));

        let existingSimpleData = [];
        if (fs.existsSync('simple.txt')) {
            const simpleFileData = fs.readFileSync('simple.txt', 'utf8');
            existingSimpleData = simpleFileData.split('\n').filter(line => line.trim() !== '');
        }

        const updatedSimpleData = [...existingSimpleData, ...simpleTextLines];

        const uniqueSimpleEntries = [...new Set(updatedSimpleData)];
        const lastSimpleEntries = uniqueSimpleEntries.slice(-50);

        fs.writeFileSync('simple.txt', lastSimpleEntries.join('\n'));
    }
}

module.exports = {
    processMessage
};
