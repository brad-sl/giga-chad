/**
 * WebSocket Client Handler for Dashboard Real-time Updates
 * Connects to Flask-SocketIO server and handles event streaming
 */

class DashboardWebSocketClient {
    /**
     * Initialize WebSocket client
     * @param {string} serverUrl - WebSocket server URL (default: ws://localhost:5000)
     * @param {Object} handlers - Event handler callbacks
     */
    constructor(serverUrl = 'http://localhost:5000', handlers = {}) {
        this.serverUrl = serverUrl;
        this.handlers = handlers;
        this.socket = null;
        this.connected = false;
        this.subscriptions = new Set();
        this.eventQueue = [];
        
        // Default handlers
        this.defaultHandlers = {
            onConnect: () => console.log('Connected to dashboard'),
            onDisconnect: () => console.log('Disconnected from dashboard'),
            onRunStatusUpdate: (event) => console.log('Run status:', event),
            onProposal: (event) => console.log('New proposal:', event),
            onLog: (event) => console.log('Log:', event),
            onExecution: (event) => console.log('Execution:', event),
            onError: (error) => console.error('WebSocket error:', error),
            onEvent: (event) => console.log('Event received:', event)
        };
        
        // Merge provided handlers with defaults
        this.handlers = { ...this.defaultHandlers, ...handlers };
    }
    
    /**
     * Connect to WebSocket server
     * Uses Socket.IO client library (must be loaded separately)
     */
    connect() {
        if (!window.io) {
            console.error('Socket.IO client library not loaded. Include <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>');
            return;
        }
        
        this.socket = io(this.serverUrl, {
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: 5
        });
        
        // Register Socket.IO event handlers
        this.registerSocketHandlers();
    }
    
    /**
     * Register Socket.IO event handlers
     * @private
     */
    registerSocketHandlers() {
        // Connection events
        this.socket.on('connect', () => {
            console.log('WebSocket connected');
            this.connected = true;
            this.handlers.onConnect();
            
            // Resubscribe to previous subscriptions after reconnect
            this.subscriptions.forEach(runId => {
                this.subscribe(runId);
            });
            
            // Flush queued events
            this.flushEventQueue();
        });
        
        this.socket.on('disconnect', () => {
            console.log('WebSocket disconnected');
            this.connected = false;
            this.handlers.onDisconnect();
        });
        
        // Connection response
        this.socket.on('connection_response', (data) => {
            console.log('Connection response:', data);
        });
        
        // Subscription response
        this.socket.on('subscription_response', (data) => {
            console.log('Subscription response:', data);
        });
        
        // Unsubscription response
        this.socket.on('unsubscription_response', (data) => {
            console.log('Unsubscription response:', data);
        });
        
        // Heartbeat response
        this.socket.on('heartbeat_response', (data) => {
            console.log('Heartbeat response:', data);
        });
        
        // Main event handler - dispatches to specific handlers
        this.socket.on('event', (event) => {
            console.log('Event received:', event);
            
            // Call generic event handler
            this.handlers.onEvent(event);
            
            // Dispatch to specific handler based on event type
            switch (event.type) {
                case 'run_status':
                    this.handlers.onRunStatusUpdate(event);
                    break;
                case 'proposal':
                    this.handlers.onProposal(event);
                    break;
                case 'log':
                    this.handlers.onLog(event);
                    break;
                case 'execution':
                    this.handlers.onExecution(event);
                    break;
                default:
                    console.warn('Unknown event type:', event.type);
            }
        });
        
        // Error handler
        this.socket.on('error', (error) => {
            console.error('WebSocket error:', error);
            this.handlers.onError(error);
        });
    }
    
    /**
     * Subscribe to a specific run's events
     * @param {string} runId - The run ID to subscribe to
     */
    subscribe(runId) {
        if (!this.socket) {
            console.error('Not connected. Call connect() first.');
            return;
        }
        
        this.subscriptions.add(runId);
        this.socket.emit('subscribe', { run_id: runId });
        console.log(`Subscribed to run: ${runId}`);
    }
    
    /**
     * Unsubscribe from a specific run's events
     * @param {string} runId - The run ID to unsubscribe from
     */
    unsubscribe(runId) {
        if (!this.socket) {
            console.error('Not connected. Call connect() first.');
            return;
        }
        
        this.subscriptions.delete(runId);
        this.socket.emit('unsubscribe', { run_id: runId });
        console.log(`Unsubscribed from run: ${runId}`);
    }
    
    /**
     * Send a heartbeat to keep connection alive
     */
    heartbeat() {
        if (!this.socket) {
            console.error('Not connected. Call connect() first.');
            return;
        }
        
        this.socket.emit('heartbeat');
    }
    
    /**
     * Queue an event if not connected
     * @private
     */
    queueEvent(event) {
        this.eventQueue.push(event);
    }
    
    /**
     * Flush queued events
     * @private
     */
    flushEventQueue() {
        if (this.eventQueue.length === 0) return;
        
        console.log(`Flushing ${this.eventQueue.length} queued events`);
        while (this.eventQueue.length > 0) {
            const event = this.eventQueue.shift();
            // Process queued events
            this.handlers.onEvent(event);
            switch (event.type) {
                case 'run_status':
                    this.handlers.onRunStatusUpdate(event);
                    break;
                case 'proposal':
                    this.handlers.onProposal(event);
                    break;
                case 'log':
                    this.handlers.onLog(event);
                    break;
                case 'execution':
                    this.handlers.onExecution(event);
                    break;
            }
        }
    }
    
    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.connected = false;
        }
    }
    
    /**
     * Get connection status
     * @returns {boolean} Connection status
     */
    isConnected() {
        return this.connected;
    }
    
    /**
     * Get current subscriptions
     * @returns {Array} Array of subscribed run IDs
     */
    getSubscriptions() {
        return Array.from(this.subscriptions);
    }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DashboardWebSocketClient;
}
