// messageSender.js
function sendAdditionalMessages(ws, isConnected) {
    if (isConnected) {
        const messages = [
            "SUBSCRIBE\nid:sub-0\ndestination:/user/exchange/amq.direct/config\n\n ",
            "SEND\ndestination:/settings/session\n\n ",
            // "SUBSCRIBE\nid:sub-1\ndestination:/user/exchange/amq.direct/geofencing-events\n\n ",
            // "SUBSCRIBE\nid:sub-2\ndestination:/user/exchange/amq.direct/updates\n\n ",
            // "SUBSCRIBE\nid:sub-3\ndestination:/user/exchange/amq.direct/updates-collection\n\n ",
            // "SUBSCRIBE\nid:sub-4\ndestination:/user/exchange/amq.direct/user-overlays-roles\n\n ",
            // "SUBSCRIBE\nid:sub-5\ndestination:/user/exchange/amq.direct/tube\n\n ",
            // "SUBSCRIBE\nid:sub-6\ndestination:/user/exchange/amq.direct/track\n\n ",
            // "SUBSCRIBE\nid:sub-7\ndestination:/user/exchange/amq.direct/tracks\n\n ",
            "SUBSCRIBE\nid:sub-8\ndestination:/user/exchange/amq.direct/feed\n\n ",
            "SUBSCRIBE\nid:sub-9\ndestination:/user/exchange/amq.direct/feed-collection\n\n ",
            "SEND\ndestination:/settings/locale\ncontent-length:2\n\nuk "
        ];

        messages.forEach(function (message) {
            ws.send(message);
            console.log("Message sent:", message);
        });
    } else {
        console.log("Connection not established. Cannot send additional messages.");
    }
}

module.exports = {
    sendAdditionalMessages
};
