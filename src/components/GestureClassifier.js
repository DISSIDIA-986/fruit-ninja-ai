/**
 * GestureClassifier - Browser-side MLP inference for hand gesture recognition
 *
 * Loads exported PyTorch weights (JSON) and runs forward pass in pure JavaScript.
 * No Python server needed. Classifies MediaPipe hand landmarks into:
 * slash, idle, grab, open_palm
 */

import modelData from '../config/gesture_model.json';

export class GestureClassifier {
    constructor() {
        this.classNames = modelData.class_names;
        this.weights = modelData.weights;
        this.scalerMean = modelData.scaler.mean;
        this.scalerScale = modelData.scaler.scale;
        this.prevLandmarks = null;
        this.prevTime = null;
        this.ready = true;
        console.log(`GestureClassifier loaded. Classes: ${this.classNames}, Accuracy: ${(modelData.test_accuracy * 100).toFixed(1)}%`);
    }

    /**
     * Extract 126 features (63 position + 63 velocity) from hand landmarks.
     * Landmarks should be an array of {x, y, z} objects (21 points).
     */
    extractFeatures(landmarks) {
        const wrist = landmarks[0];
        const positions = [];
        for (const lm of landmarks) {
            positions.push(lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z);
        }

        const now = performance.now() / 1000;
        let velocity;
        const stale = this.prevTime !== null && (now - this.prevTime) > 0.2;

        if (this.prevLandmarks && this.prevTime !== null && !stale) {
            const dt = now - this.prevTime;
            if (dt > 0) {
                velocity = positions.map((p, i) => (p - this.prevLandmarks[i]) / dt);
            } else {
                velocity = new Array(positions.length).fill(0);
            }
        } else {
            velocity = new Array(positions.length).fill(0);
        }

        this.prevLandmarks = positions;
        this.prevTime = now;

        return positions.concat(velocity);
    }

    /**
     * Standardize features using the saved scaler parameters.
     */
    standardize(features) {
        return features.map((val, i) => (val - this.scalerMean[i]) / this.scalerScale[i]);
    }

    /**
     * ReLU activation function.
     */
    relu(arr) {
        return arr.map(v => Math.max(0, v));
    }

    /**
     * Matrix multiply: input (1D array) × weight matrix + bias.
     * weight shape: [out_features, in_features]
     */
    linear(input, weightKey, biasKey) {
        const weight = this.weights[weightKey];
        const bias = this.weights[biasKey];
        const output = new Array(weight.length);
        for (let i = 0; i < weight.length; i++) {
            let sum = bias[i];
            for (let j = 0; j < input.length; j++) {
                sum += weight[i][j] * input[j];
            }
            output[i] = sum;
        }
        return output;
    }

    /**
     * Softmax function.
     */
    softmax(arr) {
        const max = Math.max(...arr);
        const exps = arr.map(v => Math.exp(v - max));
        const sum = exps.reduce((a, b) => a + b, 0);
        return exps.map(v => v / sum);
    }

    /**
     * Run MLP forward pass.
     * Network: Linear(126,128) → ReLU → Linear(128,64) → ReLU → Linear(64,32) → ReLU → Linear(32,4)
     * Dropout layers are skipped during inference.
     */
    forward(features) {
        let x = this.linear(features, 'network.0.weight', 'network.0.bias');
        x = this.relu(x);
        // Skip dropout (network.2)
        x = this.linear(x, 'network.3.weight', 'network.3.bias');
        x = this.relu(x);
        // Skip dropout (network.5)
        x = this.linear(x, 'network.6.weight', 'network.6.bias');
        x = this.relu(x);
        x = this.linear(x, 'network.8.weight', 'network.8.bias');
        return x;
    }

    /**
     * Predict gesture from MediaPipe hand landmarks.
     * @param {Array} landmarks - Array of 21 {x, y, z} landmark objects
     * @returns {{gesture: string, confidence: number, probabilities: Object}}
     */
    predict(landmarks) {
        if (!this.ready || !landmarks || landmarks.length < 21) {
            return { gesture: 'unknown', confidence: 0, probabilities: {} };
        }

        const features = this.extractFeatures(landmarks);
        const scaled = this.standardize(features);
        const logits = this.forward(scaled);
        const probs = this.softmax(logits);

        let maxIdx = 0;
        for (let i = 1; i < probs.length; i++) {
            if (probs[i] > probs[maxIdx]) maxIdx = i;
        }

        const probabilities = {};
        this.classNames.forEach((name, i) => {
            probabilities[name] = probs[i];
        });

        return {
            gesture: this.classNames[maxIdx],
            confidence: probs[maxIdx],
            probabilities,
        };
    }

    /**
     * Reset state (call when hand tracking is lost).
     */
    reset() {
        this.prevLandmarks = null;
        this.prevTime = null;
    }
}
