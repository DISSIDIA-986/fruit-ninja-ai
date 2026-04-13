/**
 * YOLO26 Fruit Ninja - Main Entry Point
 * 
 * Computer Vision Final Project
 * Using Ultralytics YOLO26 with MPS acceleration on Apple M3 Pro
 * 
 * YOLO26 Advantages over YOLO11:
 * - End-to-End inference without NMS
 * - DFL removed for simpler export
 * - ProgLoss + STAL for better small-object detection
 * - MuSGD Optimizer for stable training
 * - Up to 43% faster CPU inference
 * 
 * Modes:
 * - YOLO26 Mode: Object detection via Python backend
 * - Fallback Mode: Mouse/Touch controls
 */

import { YOLODetector, YOLOGameController } from './components/YOLODetector.js';
import { TrailRenderer } from './components/TrailRenderer.js';
import { GameScene } from './components/GameScene.js';
import { ScoreSystem } from './components/ScoreSystem.js';
import { AudioManager } from './utils/AudioManager.js';
import { SystemInfo } from './utils/SystemInfo.js';

/**
 * YOLO Fruit Ninja Game Class
 */
class YOLOFruitNinja {
    constructor() {
        // DOM 元素
        this.videoElement = document.getElementById('video-input');
        this.canvasElement = document.getElementById('game-canvas');
        this.gameContainer = document.getElementById('game-container');
        this.startScreen = document.getElementById('start-screen');
        this.pauseScreen = document.getElementById('pause-screen');
        this.gameOverScreen = document.getElementById('game-over-screen');
        this.startButton = document.getElementById('start-button');
        this.restartButton = document.getElementById('restart-button');
        this.scoreValueEl = document.getElementById('score-value');
        this.timeRemainingEl = document.getElementById('time-remaining');
        this.finalScoreValueEl = document.getElementById('final-score-value');
        this.modeToggleBtn = document.getElementById('mode-toggle');
        
        // Game components
        this.yoloDetector = null;
        this.yoloController = null;
        this.trailRenderer = null;
        this.gameScene = null;
        this.scoreSystem = null;
        this.audioManager = null;
        this.systemInfo = null;
        
        // Game state
        this.gameState = 'idle'; // idle, starting, playing, paused, gameover
        this.gameMode = 'yolo'; // 'yolo' or 'fallback'
        this.lastFrameTime = null;
        
        // Performance tracking
        this.detectionFPS = 0;
        this.renderFPS = 0;
        
        // Initialize
        this.init();
    }
    
    /**
     * Initialize game
     */
    async init() {
        console.log('🎮 YOLO Fruit Ninja: Initializing...');
        
        // Initialize system info
        this.systemInfo = new SystemInfo();
        
        // Initialize audio
        this.audioManager = new AudioManager();
        
        // Initialize score system
        this.scoreSystem = new ScoreSystem();
        this.scoreSystem.onScoreChange = (score) => this.updateScoreDisplay(score);
        this.scoreSystem.onTimeChange = (time) => this.updateTimeDisplay(time);
        this.scoreSystem.onGameOver = (data) => this.showGameOver(data);
        
        // Initialize game scene
        this.gameScene = new GameScene(
            this.canvasElement,
            (fruitType) => this.onFruitCut(fruitType),
            () => this.onBombCut()
        );
        
        // Initialize trail renderer
        this.trailRenderer = new TrailRenderer(this.canvasElement);
        
        // Initialize YOLO26 controller
        this.yoloController = new YOLOGameController(this.gameScene, this.scoreSystem);
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize camera for video background
        await this.initializeCamera();
        
        // Try to connect to YOLO26 backend
        await this.initializeYOLO();
        
        console.log('🎮 YOLO26 Fruit Ninja: Ready!');
    }
    
    /**
     * Initialize camera for video background
     */
    async initializeCamera() {
        console.log('📷 Initializing camera for video background...');
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            
            if (this.videoElement) {
                this.videoElement.srcObject = stream;
                this.videoElement.play();
                this.systemInfo.updateCameraStatus('Connected (Video Background)');
                console.log('✅ Camera connected for video background');
            }
        } catch (error) {
            console.warn('⚠️ Camera not available, using solid background');
            this.systemInfo.updateCameraStatus('Not Available');
            
            // Show solid background instead
            if (this.videoElement) {
                this.videoElement.style.display = 'none';
            }
        }
    }
    
    /**
     * Initialize YOLO26 object detection
     */
    async initializeYOLO() {
        console.log('🔍 Initializing YOLO26 detection...');
        
        this.updateStatusDisplay('Connecting to YOLO26 server...');
        
        try {
            const success = await this.yoloController.initializeYOLO({
                wsUrl: 'ws://localhost:8001/ws/detect'
            });
            
            if (success) {
                this.gameMode = 'yolo';
                this.updateModeDisplay('YOLO26 Mode');
                this.updateStatusDisplay('✅ YOLO26 Connected');
                console.log('✅ YOLO26 detection initialized');
                
                // Update system info
                if (this.systemInfo) {
                    this.systemInfo.updateDetectionStatus('YOLO26 (MPS Accelerated)');
                }
            } else {
                throw new Error('YOLO26 initialization failed');
            }
        } catch (error) {
            console.warn('⚠️ YOLO26 not available, using fallback mode');
            this.gameMode = 'fallback';
            this.updateModeDisplay('Fallback Mode');
            this.updateStatusDisplay('⚠️ Using Mouse/Touch Controls');
            
            this.setupFallbackControls();
        }
    }
    
    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Space key - pause/resume
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                this.togglePause();
            }
            
            // M key - toggle mode
            if (e.code === 'KeyM') {
                e.preventDefault();
                this.toggleMode();
            }
            
            // P key - performance monitor
            if (e.code === 'KeyP') {
                e.preventDefault();
                if (this.systemInfo && this.systemInfo.togglePerformance) {
                    this.systemInfo.togglePerformance();
                }
            }
        });
        
        // Mode toggle button
        if (this.modeToggleBtn) {
            this.modeToggleBtn.addEventListener('click', () => {
                this.toggleMode();
            });
        }
        
        // Start button
        if (this.startButton) {
            this.startButton.addEventListener('click', () => {
                this.startGame();
            });
        }
        
        // Restart button
        if (this.restartButton) {
            this.restartButton.addEventListener('click', () => {
                this.restartGame();
            });
        }
        
        // Music toggle
        const musicToggleBtn = document.getElementById('music-toggle');
        if (musicToggleBtn) {
            musicToggleBtn.addEventListener('click', () => {
                const isEnabled = this.audioManager.toggleMusic();
                musicToggleBtn.textContent = isEnabled ? '🔊' : '🔇';
            });
        }
    }
    
    /**
     * Toggle between YOLO26 and fallback mode
     */
    toggleMode() {
        if (this.gameMode === 'yolo') {
            this.gameMode = 'fallback';
            this.yoloController.stopDetection();
            this.setupFallbackControls();
            this.updateModeDisplay('Fallback Mode');
            this.updateStatusDisplay('🖱️ Mouse/Touch Controls');
        } else {
            this.gameMode = 'yolo';
            this.yoloController.startDetection();
            this.updateModeDisplay('YOLO26 Mode');
            this.updateStatusDisplay('🤖 YOLO26 Detection');
        }
    }
    
    /**
     * Setup fallback mouse/touch controls
     */
    setupFallbackControls() {
        let isMouseDown = false;
        let mouseTrail = [];
        const maxTrailLength = 25;
        
        const addMousePoint = (x, y) => {
            mouseTrail.push({ x, y, timestamp: Date.now() });
            if (mouseTrail.length > maxTrailLength) {
                mouseTrail.shift();
            }
            
            if (mouseTrail.length >= 2) {
                this.gameScene.updateCuttingPaths([{
                    points: mouseTrail.map(p => ({ x: p.x, y: p.y })),
                    hand: 'mouse'
                }]);
            }
        };
        
        const clearMouseTrail = () => {
            mouseTrail = [];
            this.gameScene.updateCuttingPaths([]);
        };
        
        // Mouse events
        this.canvasElement.addEventListener('mousedown', (e) => {
            isMouseDown = true;
            const rect = this.canvasElement.getBoundingClientRect();
            addMousePoint(e.clientX - rect.left, e.clientY - rect.top);
        });
        
        this.canvasElement.addEventListener('mousemove', (e) => {
            if (isMouseDown) {
                const rect = this.canvasElement.getBoundingClientRect();
                addMousePoint(e.clientX - rect.left, e.clientY - rect.top);
            }
        });
        
        this.canvasElement.addEventListener('mouseup', () => {
            isMouseDown = false;
            setTimeout(clearMouseTrail, 300);
        });
        
        // Touch events
        this.canvasElement.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const rect = this.canvasElement.getBoundingClientRect();
            const touch = e.touches[0];
            addMousePoint(touch.clientX - rect.left, touch.clientY - rect.top);
        });
        
        this.canvasElement.addEventListener('touchmove', (e) => {
            e.preventDefault();
            const rect = this.canvasElement.getBoundingClientRect();
            const touch = e.touches[0];
            addMousePoint(touch.clientX - rect.left, touch.clientY - rect.top);
        });
        
        this.canvasElement.addEventListener('touchend', (e) => {
            e.preventDefault();
            setTimeout(clearMouseTrail, 300);
        });
        
        console.log('🖱️ Fallback controls enabled');
    }
    
    /**
     * Start game
     */
    startGame() {
        this.gameState = 'playing';
        this.startScreen.classList.add('hidden');
        this.pauseScreen.classList.add('hidden');
        this.gameOverScreen.classList.add('hidden');
        
        this.scoreSystem.start();
        this.gameScene.reset();
        this.gameScene.setPaused(false);
        
        // Start YOLO detection
        if (this.gameMode === 'yolo') {
            this.yoloController.startDetection();
        }
        
        this.lastFrameTime = null;
        this.gameLoop();
    }
    
    /**
     * Game loop
     */
    gameLoop() {
        if (this.gameState !== 'playing') return;
        
        const now = performance.now();
        if (!this.lastFrameTime) {
            this.lastFrameTime = now;
        }
        const deltaTime = (now - this.lastFrameTime) / 1000;
        this.lastFrameTime = now;
        
        // Update score system
        this.scoreSystem.update(deltaTime);
        
        // Update trail renderer
        this.trailRenderer.drawTrails([]);
        
        // Update FPS
        this.renderFPS = Math.round(1 / deltaTime);
        this.updateFPSDisplay();
        
        requestAnimationFrame(() => this.gameLoop());
    }
    
    /**
     * Toggle pause
     */
    togglePause() {
        if (this.gameState === 'playing') {
            this.gameState = 'paused';
            this.pauseScreen.classList.remove('hidden');
            this.gameScene.setPaused(true);
            this.yoloController.stopDetection();
        } else if (this.gameState === 'paused') {
            this.gameState = 'playing';
            this.pauseScreen.classList.add('hidden');
            this.gameScene.setPaused(false);
            if (this.gameMode === 'yolo') {
                this.yoloController.startDetection();
            }
            this.lastFrameTime = null;
            this.gameLoop();
        }
    }
    
    /**
     * Restart game
     */
    restartGame() {
        this.gameState = 'idle';
        this.scoreSystem.reset();
        this.gameScene.reset();
        this.startScreen.classList.remove('hidden');
        this.gameOverScreen.classList.add('hidden');
    }
    
    /**
     * Fruit cut callback
     */
    onFruitCut(fruitType) {
        this.scoreSystem.cutFruit(fruitType);
        this.audioManager.playCutSound();
    }
    
    /**
     * Bomb cut callback
     */
    onBombCut() {
        this.scoreSystem.cutBomb();
        this.audioManager.playExplosionSound();
        this.shakeScreen();
    }
    
    /**
     * Screen shake effect
     */
    shakeScreen() {
        this.gameContainer.style.animation = 'shake 0.5s';
        setTimeout(() => {
            this.gameContainer.style.animation = '';
        }, 500);
    }
    
    /**
     * Show game over
     */
    showGameOver(data) {
        this.gameState = 'gameover';
        this.gameOverScreen.classList.remove('hidden');
        this.yoloController.stopDetection();
        
        if (this.finalScoreValueEl) {
            this.finalScoreValueEl.textContent = data.score;
        }
    }
    
    /**
     * Update score display
     */
    updateScoreDisplay(score) {
        if (this.scoreValueEl) {
            this.scoreValueEl.textContent = score;
        }
    }
    
    /**
     * Update time display
     */
    updateTimeDisplay(time) {
        if (this.timeRemainingEl) {
            this.timeRemainingEl.textContent = Math.ceil(time);
        }
    }
    
    /**
     * Update FPS display
     */
    updateFPSDisplay() {
        const fpsEl = document.getElementById('fps-value');
        if (fpsEl) {
            fpsEl.textContent = this.renderFPS;
        }
    }
    
    /**
     * Update status display
     */
    updateStatusDisplay(status) {
        const statusEl = document.getElementById('connection-status');
        if (statusEl) {
            statusEl.textContent = status;
        }
    }
    
    /**
     * Update mode display
     */
    updateModeDisplay(mode) {
        if (this.modeToggleBtn) {
            this.modeToggleBtn.textContent = mode;
        }
    }
    
    /**
     * Cleanup
     */
    dispose() {
        this.yoloController.dispose();
        this.scoreSystem.dispose();
        this.gameScene.dispose();
        
        if (this.videoElement && this.videoElement.srcObject) {
            this.videoElement.srcObject.getTracks().forEach(track => track.stop());
        }
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new YOLOFruitNinja();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.game) {
        window.game.dispose();
    }
});
