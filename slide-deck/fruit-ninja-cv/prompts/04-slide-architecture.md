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
Visual Elements: Precise lines, technical schematics, straight/90-degree connections, cross-section diagrams, isometric projections
Style Rules: Do use grid alignment, geometric precision. Don't use hand-drawn shapes, curved lines, photos.

---

## SLIDE CONTENT

**Slide 4 of 10 — Content**
**Filename**: 04-slide-architecture.png

// NARRATIVE GOAL
Present the system architecture as a three-layer pipeline — the technical core of the presentation.

// KEY CONTENT
Headline: System Architecture — Three-Layer Pipeline
Sub-headline: From camera input to rendered game frame in under 16ms
Body:
- Input Layer: Webcam (30-60 FPS) → MediaPipe HandLandmarker → 21 3D landmarks, dual-hand
- Processing Layer: GestureClassifier MLP (126→4) + TrailRenderer (neon effects)
- Rendering Layer: Three.js 3D + fruit physics + particle explosion + scoring

// VISUAL
A vertical three-tier blueprint diagram. Top tier (Input): webcam icon → arrow → hand with 21 landmark dots connected by skeleton lines. Middle tier (Processing): neural network schematic (input→hidden→output nodes) + trail visualization pattern. Bottom tier (Rendering): 3D scene with geometric fruit shapes and particle burst. Precise connection lines between tiers with data flow labels. Dimension indicators showing latency. Each layer has a Navy Blue header bar with Light Blue content area. Blueprint grid background.

// LAYOUT
Layout: hierarchical-layers
Three distinct layers stacked vertically with precise connection lines and data flow labels.
