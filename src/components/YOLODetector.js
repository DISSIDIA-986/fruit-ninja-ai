/**
 * YOLO26Detector - WebSocket-based YOLO26 Object Detection
 * 
 * Connects to Python backend server for real-time object detection
 * using YOLO26 with MPS acceleration on Apple M3 Pro.
 * 
 * YOLO26 Advantages:
 * - End-to-End inference without NMS (faster, cleaner)
 * - DFL (Distribution Focal Loss) removed (simpler export)
 * - ProgLoss + STAL for better small-object detection
 * - MuSGD Optimizer for stable training
 * - Up to 43% faster CPU inference vs YOLO11
 * 
 * @example
 * const detector = new YOLO26Detector();
 * await detector.connect();
 * detector.onDetections = (data) => { console.log(data); };
 * detector.start();
 */
export class YOLODetector {
    constructor(options = {}) {
        this.wsUrl = options.wsUrl || 'ws://localhost:8001/ws/detect';
        this.ws = null;
        this.isConnected = false;
        this.isRunning = false;
        this.onDetections = null;  // Callback for detection results
        this.onError = null;       // Callback for errors
        this.onStatusChange = null; // Callback for connection status
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // Detection state
        this.lastDetections = {
            fruits: [],
            bombs: [],
            hands: [],
            fps: 0,
            timestamp: null
        };
        
        // Performance tracking
        this.frameCount = 0;
        this.lastFpsUpdate = Date.now();
    }
    
    /**
     * Connect to YOLO detection server via WebSocket
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(this.wsUrl);
                
                this.ws.onopen = () => {
                    console.log('🔌 YOLO Detector: Connected to server');
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    this._notifyStatus('connected');
                    resolve(true);
                };
                
                this.ws.onclose = (event) => {
                    console.log('🔌 YOLO Detector: Disconnected', event.code, event.reason);
                    this.isConnected = false;
                    this.isRunning = false;
                    this._notifyStatus('disconnected');
                    
                    // Attempt reconnection
                    if (this.reconnectAttempts < this.maxReconnectAttempts) {
                        this._reconnect();
                    }
                };
                
                this.ws.onerror = (error) => {
                    console.error('🔌 YOLO Detector: WebSocket error', error);
                    this._notifyError('WebSocket connection error');
                    reject(error);
                };
                
                this.ws.onmessage = (event) => {
                    this._handleMessage(event.data);
                };
                
            } catch (error) {
                console.error('🔌 YOLO Detector: Failed to create WebSocket', error);
                reject(error);
            }
        });
    }
    
    /**
     * Handle incoming WebSocket messages
     */
    _handleMessage(data) {
        try {
            const message = JSON.parse(data);
            
            // Check for error messages
            if (message.error) {
                this._notifyError(message.error);
                return;
            }
            
            // Update detection state
            this.lastDetections = message;
            this.frameCount++;
            
            // Calculate FPS every second
            const now = Date.now();
            if (now - this.lastFpsUpdate >= 1000) {
                this.lastDetections.fps = Math.round(
                    (this.frameCount * 1000) / (now - this.lastFpsUpdate)
                );
                this.frameCount = 0;
                this.lastFpsUpdate = now;
            }
            
            // Call detection callback
            if (this.onDetections) {
                this.onDetections(this.lastDetections);
            }
            
        } catch (error) {
            console.error('🔌 YOLO Detector: Failed to parse message', error);
        }
    }
    
    /**
     * Reconnect to server with exponential backoff
     */
    _reconnect() {
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
        
        console.log(`🔌 YOLO Detector: Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
        this._notifyStatus('reconnecting');
        
        setTimeout(() => {
            this.connect().catch(console.error);
        }, delay);
    }
    
    /**
     * Start detection stream
     */
    start() {
        if (!this.isConnected) {
            console.warn('🔌 YOLO Detector: Cannot start - not connected');
            return false;
        }
        
        this.isRunning = true;
        console.log('🔌 YOLO Detector: Detection started');
        return true;
    }
    
    /**
     * Stop detection stream
     */
    stop() {
        this.isRunning = false;
        
        if (this.ws && this.isConnected) {
            try {
                this.ws.send(JSON.stringify({ type: 'stop' }));
            } catch (error) {
                console.error('🔌 YOLO Detector: Failed to send stop message', error);
            }
        }
        
        console.log('🔌 YOLO Detector: Detection stopped');
    }
    
    /**
     * Disconnect from server
     */
    disconnect() {
        this.stop();
        
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        
        this.isConnected = false;
        this._notifyStatus('disconnected');
    }
    
    /**
     * Get current detection state
     */
    getDetections() {
        return { ...this.lastDetections };
    }
    
    /**
     * Check if a point is inside any detected fruit bounding box
     */
    isPointInFruit(x, y) {
        for (const fruit of this.lastDetections.fruits) {
            const [fx, fy, fw, fh] = fruit.bbox;
            if (x >= fx && x <= fx + fw && y >= fy && y <= fy + fh) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Get fruits near a point (for cutting detection)
     */
    getFruitsNearPoint(x, y, threshold = 50) {
        return this.lastDetections.fruits.filter(fruit => {
            const [fx, fy, fw, fh] = fruit.bbox;
            const centerX = fx + fw / 2;
            const centerY = fy + fh / 2;
            const distance = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2);
            return distance < threshold;
        });
    }
    
    /**
     * Notify status change
     */
    _notifyStatus(status) {
        if (this.onStatusChange) {
            this.onStatusChange(status);
        }
    }
    
    /**
     * Notify error
     */
    _notifyError(error) {
        if (this.onError) {
            this.onError(error);
        }
    }
}

/**
 * YOLO-based Game Controller
 * Integrates YOLO detection with game logic
 */
export class YOLOGameController {
    constructor(gameScene, scoreSystem) {
        this.gameScene = gameScene;
        this.scoreSystem = scoreSystem;
        this.detector = null;
        this.previousFruitPositions = new Map();
        this.cutCooldowns = new Map();
        this.isUsingYOLO = false;
    }
    
    /**
     * Initialize YOLO detector
     */
    async initializeYOLO(options = {}) {
        this.detector = new YOLODetector(options);
        
        this.detector.onDetections = (detections) => {
            this._handleDetections(detections);
        };
        
        this.detector.onStatusChange = (status) => {
            console.log(`🎮 YOLO Game: Status changed to ${status}`);
        };
        
        this.detector.onError = (error) => {
            console.error(`🎮 YOLO Game: Error - ${error}`);
        };
        
        try {
            await this.detector.connect();
            this.isUsingYOLO = true;
            console.log('🎮 YOLO Game: YOLO detector initialized');
            return true;
        } catch (error) {
            console.error('🎮 YOLO Game: Failed to initialize YOLO', error);
            this.isUsingYOLO = false;
            return false;
        }
    }
    
    /**
     * Handle incoming detections
     */
    _handleDetections(detections) {
        if (!this.gameScene || this.gameScene.isPaused) return;
        
        // Update fruit positions based on YOLO detections
        const currentFruitPositions = new Map();
        
        detections.fruits.forEach((fruit, index) => {
            const fruitId = `fruit_${index}`;
            const [x, y, w, h] = fruit.bbox;
            const centerX = x + w / 2;
            const centerY = y + h / 2;
            
            currentFruitPositions.set(fruitId, { x: centerX, y: centerY });
            
            // Check if fruit was "cut" (rapid position change or hand proximity)
            if (this.previousFruitPositions.has(fruitId)) {
                const prevPos = this.previousFruitPositions.get(fruitId);
                const distance = Math.sqrt(
                    (centerX - prevPos.x) ** 2 + (centerY - prevPos.y) ** 2
                );
                
                // If fruit moved significantly, consider it "cut"
                if (distance > 30 && !this.cutCooldowns.has(fruitId)) {
                    this._onFruitCut(fruit);
                    this.cutCooldowns.set(fruitId, Date.now());
                    
                    // Remove cooldown after 500ms
                    setTimeout(() => {
                        this.cutCooldowns.delete(fruitId);
                    }, 500);
                }
            }
        });
        
        this.previousFruitPositions = currentFruitPositions;
        
        // Update game scene with detection overlay
        if (this.gameScene.updateYOLODetections) {
            this.gameScene.updateYOLODetections(detections);
        }
    }
    
    /**
     * Handle fruit cut event
     */
    _onFruitCut(fruit) {
        console.log('🎮 YOLO Game: Fruit cut!', fruit);
        
        if (this.scoreSystem) {
            this.scoreSystem.cutFruit(fruit.class_id || 'unknown');
        }
    }
    
    /**
     * Start YOLO detection
     */
    startDetection() {
        if (this.detector) {
            this.detector.start();
        }
    }
    
    /**
     * Stop YOLO detection
     */
    stopDetection() {
        if (this.detector) {
            this.detector.stop();
        }
    }
    
    /**
     * Cleanup
     */
    dispose() {
        if (this.detector) {
            this.detector.disconnect();
            this.detector = null;
        }
        this.isUsingYOLO = false;
    }
}
