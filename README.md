# Mindala Project

**Biofeedback-Responsive Immersive Dome Installation for LUMA Projection Arts Festival 2026 Small Works**

Mindala (Mind + Mandala) is a cutting-edge, participant-driven immersive art installation that transforms real-time human neurophysiological data into a living, 360-degree generative audiovisual mandala. It represents a paradigm shift in projection mapping—from passive architectural spectacle to active, cybernetic self-exploration and therapeutic entrainment.

## Project Overview

Mindala creates a closed feedback loop where participants' brainwaves (via Emotiv EPOC EEG), heart-rate variability, respiration, and electrodermal activity directly drive generative visuals, spatial audio (isochronic tones), and physical cymatics. The experience unfolds in five narrative phases: Arrival, Grounding, Attention, Coherence, and Release, culminating in personalized 'mandala signatures.'

The installation can be deployed as a seamless negative-pressure fulldome (interior + optional exterior mapping) or scaled for lobby/small works contexts. It aligns perfectly with LUMA's Small Works initiative for experimental, tech-based, immersive installations in intimate urban spaces.

**Key Innovation:** Proprietary VUSIC engine fusing digital signal processing, adaptive LSTM machine learning, analog cymatics chamber, and generative shaders for stable, aesthetically coherent real-time output.

## Artist Background

Created by Robert F. Thomas (Metta), a world-class projection artist and applied physicist with extensive experience in large-scale immersive events (Envision Festival, Miami Fashion Week, Shambhala, etc.). After Hurricane Helene devastated his Asheville studio and equipment (~$80k loss), leading to homelessness and bureaucratic challenges, Mindala emerged as a resilient, healing-focused technological vision. This project is both artistic triumph and professional resurrection.

## Technical Architecture

### Biometric Acquisition
- Emotiv EPOC EEG (14 channels): Delta, Theta, Alpha, Beta, Gamma bands
- Integrated chair sensors: PPG (HRV RMSSD), Respiration, EDA
- Multi-modal 'group coherence vector' for collective response

### VUSIC Engine
- Digital signal preprocessing (band-pass filters)
- Feature extraction and normalization to control vector C(t)
- OSC/MIDI routing to DAW (Ableton) for sonification and isochronic tones
- Audio-driven cymatics chamber (Faraday waves in reflective fluid)
- OLED shader overlay + multispectral camera capture
- LSTM adaptive model for aesthetic stabilization
- Real-time 3D spherical projection mapping with edge-blending (UST laser projectors, compatible with LUMA's Panasonic ecosystem)

### Auditory Component
- Isochronic tones for neural entrainment (no headphones needed)
- Spatial audio array mapped to dome acoustics
- Phase-specific frequencies (e.g., 40Hz gamma for Attention, 5Hz theta for Release)

### Projection & Mapping
- Fulldome interior with ultra-short throw projectors
- Optional exterior mapping for public beacon effect
- Real-time warping and calibration
- Fallback to pre-rendered deterministic masters

## Scalable Deployment Tiers

**Tier 1: Standalone Flagship Dome** (600-1200 sq ft, 20-25 min sessions, ticketed potential)
**Tier 2: Lobby Module (Small Works)** (120-200 sq ft, 6-8 min micro-sessions)
**Tier 3: Dome Prelude** (plug-in activation, 60-120 sec)

All tiers support high audience throughput and sponsor branding opportunities.

## Functional Demo

This repository includes a self-contained Python demonstration of the core signal processing pipeline:

**EEG/Biofeedback Signal → Feature Extraction → Sonification Parameters → Cymatic Pattern Generation → Control Vector for Video Mapping**

The demo simulates realistic physiological signals for different mental states (relaxed/meditative vs. focused/attentive), processes them, generates corresponding audio parameters and visual cymatic patterns (2D wave simulations), and outputs OSC-ready control data suitable for mixing in Resolume, TouchDesigner, MadMapper, or Synesthesia.

### Running the Demo

1. Clone the repo: `git clone https://github.com/IAmM3ta/mindala.git`
2. Install dependencies: `pip install numpy matplotlib scipy`
3. Run: `python demo/pipeline_demo.py`

The script will:
- Simulate time-series data for multiple 'participants'
- Compute band powers, coherence metrics
- Map to generative parameters (complexity, symmetry, speed, color palette)
- Generate and save animated cymatic visualizations (matplotlib)
- Print real-time control vectors (e.g., for OSC: /mindala/coherence 0.85)
- Demonstrate blending logic for mixing with external animations

See `demo/pipeline_demo.py` and inline comments for integration examples (OSC to Resolume/TouchDesigner, Spout/Syphon for video layers).

## Proof of Concept & Resources

- Full project proposal and technical details available upon request or in supporting application materials
- This repo serves as living proof-of-concept and development hub
- Future expansions: Full open-source VUSIC engine components, 3D dome models, custom shaders

## LUMA 2026 Alignment

Mindala directly responds to the Small Works call for experimental, immersive, tech-based storytellers with something to say. It offers intimate, high-impact experiences that create profound emotional connections—exactly LUMA's mission—while providing a luminous exterior beacon visible across the festival footprint. The dual interior/exterior mapping capability bridges personal psychological exploration with grand public spectacle.

**Artist Contact:** Robert F. Thomas (Metta) | m3tamix@gmail.com | Asheville, NC (recovering from Hurricane Helene impacts)

*Mindala: From chaos to coherence. Out of destruction, ultimate order, beauty, and coherence emerge.*

## License
- Demo code and scripts: MIT License
- Core artistic concept, VUSIC engine, and installation design: All rights reserved (patent-pending elements)

---

*This project is submitted to the 2026 LUMA Projection Arts Festival Small Works Open Call. Submission Deadline: July 1, 2026, 11:59 PM.*