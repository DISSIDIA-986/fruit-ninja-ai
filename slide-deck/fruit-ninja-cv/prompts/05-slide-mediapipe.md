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
Visual Elements: Precise lines, technical schematics, data visualization, measurement indicators
Style Rules: Do use grid alignment, geometric precision. Don't use hand-drawn shapes, curved lines, photos.

---

## SLIDE CONTENT

**Slide 5 of 10 — Content**
**Filename**: 05-slide-mediapipe.png

// NARRATIVE GOAL
Deep dive into hand tracking: MediaPipe landmarks and performance optimizations.

// KEY CONTENT
Headline: Hand Tracking — MediaPipe Hand Landmarker
Sub-headline: 21 3D landmarks per hand, running entirely in the browser
Body:
- MediaPipe Tasks Vision v0.10.22 — state-of-the-art, no server needed
- 21 landmarks: thumb (1-4), index (5-8), middle (9-12), ring (13-16), pinky (17-20), wrist (0)
- Optimizations: 3-frame smoothing, 150ms trail retention, adaptive detection 16-33ms
- Performance tiers: Low 30fps | Medium 45fps | High 60fps

// VISUAL
Left side: Detailed blueprint drawing of a hand showing all 21 MediaPipe landmarks as numbered circles connected by precise skeleton lines. Each finger group labeled and color-coded with Engineering Blue. Right side: Performance data card rendered as a clean blueprint table showing three device tiers (Low/Medium/High) with columns for Detection FPS, Particle Count, and Target FPS. Bottom: horizontal timeline arrow showing smoothing pipeline: raw input → 3-frame buffer → smoothed output, with timing labels.

// LAYOUT
Layout: split-screen
Left: hand landmark diagram with numbered points. Right: performance metrics table and optimization pipeline.
