// app.js
const WebSocket = require('ws');
const { findClosestLocation } = require('./locationUtils.js');
const { processMessage } = require('./messageProcessor.js');
const { sendAdditionalMessages } = require('./messageSender.js');

const showByDistance = false;
const url = "wss://delta.mil.gov.ua/updates/events/websocket";
const headers = {
    "Host": "delta.mil.gov.ua",
    "Origin": "https://delta.mil.gov.ua",
    "Cookie": `AUTH_SESSIONID=${process.env.AUTH_SESSIONID}; SESSION=${process.env.SESSION} `,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Sec-WebSocket-Version": "13",
};
const protocolValue = ["v12.stomp", "v11.stomp", "v10.stomp"];

let isConnected = false;

const ws = new WebSocket(url, protocolValue, { headers: headers });

ws.on('open', function () {
    console.log("WebSocket connection opened");

    const initialMessage = "CONNECT\ndestination:monitor\naccept-version:1.2,1.1,1.0\nheart-beat:60000,60000\n\n ";
    ws.send(initialMessage);
    console.log("Initial message sent");

    setInterval(function () {
        if (isConnected) {
            ws.send("\n\n");
            console.log("Keep-alive message sent");
        }
    }, 6000);
});

ws.on('message', function (data) {
    const message = data.toString();
    console.log("Received message:", message);

    if (message.indexOf("CONNECTED") > -1) {
        isConnected = true;
        sendAdditionalMessages(ws, isConnected);
    }

    processMessage(message, findClosestLocation, showByDistance);
});

ws.on('close', function (code, reason) {
    console.log("WebSocket connection closed:", code, reason);
});

ws.on('error', function (error) {
    console.error("WebSocket error:", error);
});
