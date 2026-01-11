# Tracking Scripts

Real-time drone tracking via WebSocket connection to Ukrainian military tracking system.

## Scripts

### [ws-client.js](ws-client.js)
Main WebSocket client entry point.

**Purpose**: Establishes and maintains WebSocket connection to `wss://delta.mil.gov.ua/updates/events/websocket`

**Features**:
- STOMP protocol support (v12, v11, v10)
- Session-based authentication
- Keep-alive heartbeat mechanism (6-second intervals)
- Orchestrates message processing and sending

**Environment Variables**:
- `AUTH_SESSIONID`: Authentication session ID cookie
- `SESSION`: Session cookie

**Usage**:
```bash
node src/tracking/ws-client.js
```

### [messageProcessor.js](messageProcessor.js)
Processes incoming WebSocket messages.

**Purpose**: Extracts and stores drone position data from STOMP messages

**Features**:
- Filters for subscription "sub-9" (feed-collection)
- Parses JSON data for unmanned aircraft ("Безпілотний літак")
- Extracts coordinates, timestamps, and metadata
- Uses locationUtils to match positions to known locations
- Maintains rolling window of last 50 unique entries
- Deduplicates by ID
- Outputs to CSV and simplified text format

**Outputs**:
- `output/csv/data.csv`: Full tracking data
- `output/text/simple.txt`: Simplified format (location - drone type)

### [messageSender.js](messageSender.js)
Sends STOMP subscription and configuration messages.

**Purpose**: Configures WebSocket subscriptions and settings

**Features**:
- Subscribes to required STOMP channels
- Sets locale to Ukrainian
- Manages message timing after connection established

## Data Flow

1. **ws-client.js** establishes WebSocket connection
2. On connection, **messageSender.js** sends subscription messages
3. Incoming messages are processed by **messageProcessor.js**
4. Drone positions are matched to locations using **locationUtils.js** from processing/
5. Results are written to output/csv/ and output/text/

## Dependencies

- `ws@^8.17.1`: WebSocket client library

## Running

Make sure environment variables are set:
```bash
export AUTH_SESSIONID="your_session_id"
export SESSION="your_session_cookie"
node src/tracking/ws-client.js
```

Or use the .env file in data/config/
