Create a presentation slide image following these guidelines:

## Image Specifications

- **Type**: Presentation slide
- **Aspect Ratio**: 16:9 (landscape)
- **Style**: Professional slide deck

## Core Principles

- NO realistic or photographic elements
- NO slide numbers, page numbers, footers, headers, or logos
- Clean, uncluttered layouts with clear visual hierarchy

## STYLE_INSTRUCTIONS

Design Aesthetic: Technical grid overlay with engineering precision. Cool analytical blues and grays. Clean schematics with consistent line weights.

Background: Subtle grid overlay, Blueprint Off-White (#FAF8F5)
Typography: Headlines in bold geometric sans-serif. Body in clean readable serif.
Color Palette: Primary Text Deep Slate (#334155), Accent Engineering Blue (#2563EB), Navy Blue (#1E3A5F), Light Blue (#BFDBFE), Amber (#F59E0B)
Visual Elements: Precise lines, technical schematics, straight/90-degree connections, data visualization
Style Rules: Do use grid alignment, geometric precision. Don't use hand-drawn shapes, curved lines, photos.

---

## SLIDE CONTENT

**Slide 6 of 10 — Content**
**Filename**: 06-slide-gesture-ml.png

// NARRATIVE GOAL
Explain the custom ML pipeline: data collection → feature engineering → MLP model → browser inference.

// KEY CONTENT
Headline: Gesture Classification — Custom ML Pipeline
Sub-headline: From 21 landmarks to 4 game actions in real-time
Body:
- Data: Custom script captures MediaPipe landmarks with labeled gestures
- Features: 63 position (xyz relative to wrist) + 63 velocity (displacement/dt) = 126 dimensions
- Model: MLP trained in PyTorch, weights exported to JSON
- Output: slash, idle, grab, open_palm — pure JS forward pass, no server

// VISUAL
Horizontal pipeline flowing left to right with four stages. Stage 1 (Data): hand icon with gesture label below, in a Light Blue card. Stage 2 (Features): 126-element feature vector as a blueprint data block with two sections — position (63, blue) and velocity (63, navy). Stage 3 (Model): MLP neural network diagram showing input layer (126 nodes), two hidden layers, output layer (4 nodes), drawn as precise circles connected by straight lines. Stage 4 (Output): four labeled output nodes with icons — slash (diagonal line), idle (flat line), grab (closed hand), open_palm (open hand), with slash highlighted in Engineering Blue. Precise arrow connections between stages with dimension labels. Blueprint grid background.

// LAYOUT
Layout: linear-progression
Four stages flowing left to right: Data → Features → Model → Output. Each in a card with header.
