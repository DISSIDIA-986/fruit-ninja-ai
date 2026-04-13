# Slide Deck Outline

**Topic**: Fruit Ninja - AI Gesture-Controlled Game (CV Course Project)
**Style**: blueprint
**Dimensions**: grid + cool + technical + balanced
**Audience**: intermediate (classmates + professor, SAIT Integrated AI)
**Language**: en
**Slide Count**: 10 slides
**Generated**: 2026-04-10 17:55

---

<STYLE_INSTRUCTIONS>
Design Aesthetic: Technical grid overlay with engineering precision. Cool analytical blues and grays creating a structured, professional visual language. Clean schematics and diagrams with consistent line weights. Information presented in grid-based layouts with clear visual hierarchy.

Background:
  Texture: Subtle grid overlay, light engineering paper feel
  Base Color: Blueprint Off-White (#FAF8F5)

Typography:
  Headlines: Bold geometric sans-serif with clean, precise letterforms and consistent spacing. Technical, authoritative presence with strong visual weight.
  Body: Elegant serif with clean readability at smaller sizes. Professional editorial quality with clear hierarchy.

Color Palette:
  Primary Text: Deep Slate (#334155) - Headlines, body text
  Background: Blueprint Paper (#FAF8F5) - Primary background
  Grid: Light Gray (#E5E5E5) - Background grid lines
  Accent 1: Engineering Blue (#2563EB) - Key elements, highlights, connections
  Accent 2: Navy Blue (#1E3A5F) - Supporting elements, section headers
  Tertiary: Light Blue (#BFDBFE) - Backgrounds, fills, cards
  Warning: Amber (#F59E0B) - Warnings, emphasis, bomb indicators

Visual Elements:
  - Precise lines with consistent stroke weights
  - Technical schematics and clean vector graphics
  - Connection lines using straight lines or 90-degree angles only
  - Data visualization with clean, minimal charts
  - Dimension lines and measurement indicators
  - Cross-section style diagrams for architecture
  - Isometric projections for system components

Density Guidelines:
  - Content per slide: 2-3 key points with supporting detail
  - Whitespace: Balanced, ~40% whitespace
  - Element count: 3-5 visual elements per slide

Style Rules:
  Do: Maintain consistent line weights, use grid alignment for all elements, keep color palette restrained, create clear visual hierarchy through scale, use geometric precision for all shapes
  Don't: Use hand-drawn or organic shapes, add decorative flourishes, use curved connection lines, include photographic elements, add slide numbers or footers or logos
</STYLE_INSTRUCTIONS>

---

## Slide 1 of 10

**Type**: Cover
**Filename**: 01-slide-cover.png

// NARRATIVE GOAL
Establish the project identity and team. Create a strong first impression that communicates both the gaming fun and the technical sophistication.

// KEY CONTENT
Headline: Fruit Ninja
Sub-headline: AI Gesture-Controlled Game — Real-time Hand Tracking with MediaPipe & Three.js
Body:
- Group 9 | Introduction to Computer Vision
- SAIT Integrated AI Program
- Bustamante Perez, Angel Daniel | Lemes Cordeiro, Romilson | Niu, Jason | Si, Jack

// VISUAL
A blueprint-style technical illustration of a hand silhouette with 21 landmark points connected by precise lines, positioned centrally. Geometric fruit shapes (apple, watermelon, orange) arranged around the hand in an isometric grid. Subtle grid overlay on the background. Engineering Blue accent lines connecting the hand landmarks. The overall composition feels like a technical blueprint for a gesture recognition system, but with playful fruit elements.

// LAYOUT
Layout: title-hero
Large centered title with subtitle below. Team member names in a clean row at the bottom. Hand landmark diagram as a subtle background element.

---

## Slide 2 of 10

**Type**: Content
**Filename**: 02-slide-problem.png

// NARRATIVE GOAL
Explain the real-world problem: why gesture-controlled gaming matters and what limitations exist in current approaches. Make the audience understand the gap before showing the solution.

// KEY CONTENT
Headline: The Problem — Gaming Beyond Controllers
Sub-headline: Natural interaction requires expensive hardware or complex setups
Body:
- Traditional gaming relies on controllers, keyboards, or touchscreens — creating a barrier between player and game
- Gesture-based interaction is more natural but existing solutions require expensive hardware (Kinect ~$150, Leap Motion ~$90)
- Our goal: gesture-controlled fruit cutting using ONLY a webcam — no special hardware, runs in any modern browser
- Target: real-time hand tracking at 60 FPS with sub-16ms latency, deployed on the web

// VISUAL
Blueprint-style binary comparison. Left side: traditional input devices (controller, keyboard, touchscreen) shown as technical drawings with dimension lines and "BARRIER" label. Right side: a webcam icon with radiating detection lines showing a hand, labeled "NATURAL INTERACTION." A bridge element connects the two sides with the label "Our Solution." Clean schematic style with Engineering Blue accents.

// LAYOUT
Layout: binary-comparison
Left panel shows the problem (traditional inputs), right panel shows the opportunity (webcam-only gesture control). Bridge element in center.

---

## Slide 3 of 10

**Type**: Content
**Filename**: 03-slide-challenges.png

// NARRATIVE GOAL
Present the 5 key technical challenges and their corresponding solutions. Show that the team understood the hard problems and solved them methodically.

// KEY CONTENT
Headline: Technical Challenges & Solutions
Sub-headline: Five engineering problems we solved
Body:
- Challenge: Hand detection in varied lighting → Solution: MediaPipe + adaptive brightness
- Challenge: Distinguishing slash vs. idle vs. grab → Solution: Custom MLP classifier (126 features)
- Challenge: Real-time performance across devices → Solution: 3-tier adaptive performance system
- Challenge: 3D game overlay on live camera → Solution: Three.js transparent WebGL rendering
- Challenge: Production deployment with HTTPS → Solution: Aliyun ESA with CDN fallback

// VISUAL
Five horizontal rows, each split into two zones. Left zone (amber/warning tone): challenge icon + text. Right zone (blue/accent tone): solution icon + text. Connected by precise arrow lines. Each row has a small technical icon: lightbulb, gesture hand, speedometer, layers, cloud. Blueprint grid background with clean measurement indicators between rows.

// LAYOUT
Layout: bullet-list
Five challenge-solution pairs in structured rows with consistent spacing and alignment.

---

## Slide 4 of 10

**Type**: Content
**Filename**: 04-slide-architecture.png

// NARRATIVE GOAL
Present the system architecture as a three-layer pipeline. This is the technical core of the presentation — show how all components connect.

// KEY CONTENT
Headline: System Architecture — Three-Layer Pipeline
Sub-headline: From camera input to rendered game frame in under 16ms
Body:
- Input Layer: Webcam (30-60 FPS) → MediaPipe HandLandmarker (21 3D landmarks per hand) → Dual-hand support
- Processing Layer: GestureClassifier MLP (126 features → 4 classes) + TrailRenderer (fluorescent neon effects)
- Rendering Layer: Three.js 3D scene + Fruit physics (parabolic trajectories) + Particle explosion + ScoreSystem (+10 fruit / -20 bomb / 60s timer)

// VISUAL
A vertical three-tier blueprint diagram. Top tier (Input): webcam icon → arrow → hand with 21 dots. Middle tier (Processing): neural network diagram → gesture labels + trail visualization. Bottom tier (Rendering): 3D scene with fruits and particles. Precise connection lines between tiers with data flow labels (landmarks, gesture class, render calls). Dimension indicators showing latency at each stage. Blueprint grid background with layer separators.

// LAYOUT
Layout: hierarchical-layers
Three distinct layers stacked vertically with connection lines. Each layer has a header bar in Navy Blue and content in Light Blue cards.

---

## Slide 5 of 10

**Type**: Content
**Filename**: 05-slide-mediapipe.png

// NARRATIVE GOAL
Deep dive into the hand tracking technology. Explain MediaPipe, the 21 landmarks, and the optimizations made for real-time gaming.

// KEY CONTENT
Headline: Hand Tracking — MediaPipe Hand Landmarker
Sub-headline: 21 3D landmarks per hand, running entirely in the browser
Body:
- Google's MediaPipe Tasks Vision v0.10.22 — state-of-the-art hand tracking
- Detects 21 3D landmarks per hand in real-time, no server round-trip
- Optimizations: 3-frame smoothing buffer, 150ms trail retention, adaptive detection (16-33ms)
- Performance: Low-end 30fps / Medium 45fps / High-end 60fps with auto-adjustment

// VISUAL
Left side: A detailed blueprint drawing of a hand showing all 21 MediaPipe landmarks as numbered circles connected by precise lines matching the MediaPipe hand skeleton. Each landmark group labeled (thumb: 1-4, index: 5-8, middle: 9-12, ring: 13-16, pinky: 17-20, wrist: 0). Right side: A performance metrics table rendered as a clean blueprint data card showing the three device tiers with FPS and particle counts. Bottom: timeline arrow showing the smoothing pipeline (raw → 3-frame buffer → smoothed output).

// LAYOUT
Layout: split-screen
Left: hand landmark diagram. Right: performance metrics and optimization details.

---

## Slide 6 of 10

**Type**: Content
**Filename**: 06-slide-gesture-ml.png

// NARRATIVE GOAL
Explain the custom ML pipeline for gesture classification. Show the data collection, feature engineering, and model architecture that turns raw landmarks into game actions.

// KEY CONTENT
Headline: Gesture Classification — Custom ML Pipeline
Sub-headline: From 21 landmarks to 4 game actions in real-time
Body:
- Data Collection: Custom script captures MediaPipe landmarks with labeled gestures
- Feature Engineering: 63 position features (xyz relative to wrist) + 63 velocity features (frame-to-frame displacement / dt) = 126 dimensions
- Model: MLP trained in PyTorch, weights exported to JSON for browser inference
- 4 Classes: slash, idle, grab, open_palm — pure JavaScript forward pass, no Python server

// VISUAL
A horizontal pipeline diagram flowing left to right. Stage 1 (Data): hand icon with labeled gesture below → Stage 2 (Features): a 126-element feature vector shown as a blueprint data block with position (63) and velocity (63) sections highlighted in different blues → Stage 3 (Model): MLP neural network diagram with input layer, hidden layers, output layer → Stage 4 (Output): four labeled output nodes (slash, idle, grab, open_palm) with slash highlighted. Connection lines between stages with data dimension labels. Blueprint grid background.

// LAYOUT
Layout: linear-progression
Four stages flowing left to right: Data → Features → Model → Output.

---

## Slide 7 of 10

**Type**: Content
**Filename**: 07-slide-game-engine.png

// NARRATIVE GOAL
Show the visual effects and game engine: Three.js rendering, fluorescent trails, and collision detection that make the game fun to play.

// KEY CONTENT
Headline: Game Engine & Visual Effects
Sub-headline: Three.js 3D rendering layered over live camera feed
Body:
- 5 fruit types (apple, watermelon, orange, banana, pineapple) with parabolic physics
- Fluorescent trails: Neon Blue (#00FFFF) left hand, Neon Green (#00FF00) right hand
- Collision detection: 3D ray-based cutting path intersection with screen-to-world mapping
- Progressive difficulty: spawn rate increases over game time, bomb penalty -20 points

// VISUAL
A layered cross-section diagram showing the rendering stack. Bottom layer: webcam video feed (shown as a blueprint camera). Middle layer: 2D canvas with neon trail paths drawn in bright cyan and green. Top layer: Three.js 3D scene with geometric fruit shapes and particle burst effects. Side panel: small isometric views of each fruit type rendered as technical drawings. Color callouts for the neon trail colors (#00FFFF, #00FF00, #FF1493). Blueprint grid background with layer separation indicators.

// LAYOUT
Layout: hierarchical-layers
Three rendering layers shown as a cross-section with labeled separators. Side panel with fruit type catalog.

---

## Slide 8 of 10

**Type**: Content
**Filename**: 08-slide-demo.png

// NARRATIVE GOAL
Transition to the live demo. Set expectations and show what the audience will see.

// KEY CONTENT
Headline: Live Demo
Sub-headline: Gesture-controlled fruit cutting in action
Body:
- Real-time hand tracking with webcam
- Dual-hand fluorescent trail effects
- Score tracking and difficulty progression
- Fallback: mouse control if camera unavailable
- Try it: esa-project02.7fc1132f.er.aliyun-esa.net

// VISUAL
A large blueprint-style screen frame showing a simplified game interface: a camera feed area with a hand outline, flying fruit shapes with trajectory arcs, neon trail lines following the hand path, and a score HUD in the corner. The frame is drawn as a technical blueprint with dimension lines showing the screen layout. A "LIVE" indicator in Engineering Blue at the top. URL displayed at the bottom in a clean technical callout box.

// LAYOUT
Layout: image-caption
Large central game screen mockup with supporting text overlay. URL callout at bottom.

---

## Slide 9 of 10

**Type**: Content
**Filename**: 09-slide-contributions.png

// NARRATIVE GOAL
Clearly attribute each team member's specific contributions. This will be cross-checked during Q&A.

// KEY CONTENT
Headline: Team Contributions
Sub-headline: Who built what
Body:
- Niu, Jason: Hand tracking integration (MediaPipe), gesture classifier ML pipeline, performance optimization, deployment (Aliyun ESA)
- Si, Jack: Three.js game engine, fruit physics & collision detection, visual effects (trails, particles), UI/UX design
- Bustamante Perez, Angel Daniel: Data collection for gesture training, testing & QA across devices, documentation
- Lemes Cordeiro, Romilson: YOLO26 object detection integration, Python backend (FastAPI + WebSocket), benchmark testing

// VISUAL
A hub-spoke diagram with the project name at center. Four branches radiating outward, each leading to a member card. Each card is a blueprint-style data block with the member's name as header and their responsibilities as a checklist below. Color-coded accent strips on each card (Engineering Blue, Navy Blue, Amber, Light Blue) to differentiate members. Connection lines from each card to the relevant system components shown as small icons.

// LAYOUT
Layout: hub-spoke
Central project node with four member branches. Each branch ends in a detailed contribution card.

---

## Slide 10 of 10

**Type**: Back Cover
**Filename**: 10-slide-back-cover.png

// NARRATIVE GOAL
Summarize results with concrete metrics, share key lessons, and close with a memorable takeaway. Invite questions.

// KEY CONTENT
Headline: Results & Lessons Learned
Sub-headline: What we achieved and what we'd do differently
Body:
- Results: 60 FPS hand tracking (<16ms latency), high-accuracy gesture classifier, YOLO26 at 134 FPS on M3 Pro, deployed on Aliyun ESA
- Key Lessons: Client-side ML eliminates server latency, 3-frame smoothing prevents false triggers, device-adaptive presets are essential, HTTPS required for camera in production
- Future Work: More gesture types (pinch, rotate), multiplayer mode, mobile optimization
- Questions & Discussion — Thank you!

// VISUAL
Two-column layout on blueprint grid. Left column: "Results" section with key metrics displayed as blueprint data cards — FPS gauge showing 60, latency indicator showing <16ms, YOLO26 speed callout showing 134 FPS. Right column: "Lessons Learned" as a numbered blueprint checklist with checkmarks. Bottom section: "Future Work" as a winding roadmap with 3 milestone nodes. Footer: "Questions & Discussion" in Engineering Blue with "Thank You" as a clean closing element.

// LAYOUT
Layout: two-columns
Left: Results metrics. Right: Lessons learned checklist. Bottom strip: Future work roadmap and closing.
