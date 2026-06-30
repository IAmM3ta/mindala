#!/usr/bin/env python3
"""
Mindala Pipeline Demo: EEG/Biofeedback Signal → Sonification → Cymatic Generation → Video Mapping

This self-contained script simulates the core real-time signal processing pipeline for the Mindala installation.
It demonstrates:
- Multi-channel EEG + biometric feature extraction
- Mapping to generative control parameters
- Sonification parameter generation
- 2D Cymatic wave pattern simulation (visual proxy for the physical chamber)
- Output of OSC-ready control vectors for integration with Resolume, TouchDesigner, MadMapper, Synesthesia, etc.

The demo supports 'mixing' by outputting parameters that can blend with external animation layers (e.g., via opacity, shader uniforms, or layer blending modes).

Run: python demo/pipeline_demo.py
Requires: numpy, matplotlib, scipy (see requirements.txt)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time

# ============================================================
# 1. SIMULATE BIOMETRIC SIGNALS (EEG + Chair Sensors)
# ============================================================
def simulate_biometrics(duration=10.0, fs=256, state='relaxed', num_participants=3):
    """Simulate realistic multi-participant biometric time series."""
    t = np.linspace(0, duration, int(fs * duration))
    signals = {}
    
    for p in range(num_participants):
        prefix = f'p{p+1}_'
        if state == 'relaxed':
            # High alpha/theta, low beta, high HRV coherence
            alpha = 0.7 * np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(len(t))
            theta = 0.6 * np.sin(2 * np.pi * 6 * t) + 0.1 * np.random.randn(len(t))
            beta = 0.15 * np.sin(2 * np.pi * 20 * t) + 0.05 * np.random.randn(len(t))
            hrv = 0.85 + 0.1 * np.sin(2 * np.pi * 0.1 * t)  # High RMSSD-like coherence
            resp = 0.4 + 0.1 * np.sin(2 * np.pi * 0.25 * t)  # Slow deep breathing
            eda = 0.3 + 0.05 * np.sin(2 * np.pi * 0.05 * t)  # Low arousal
        else:  # 'focused' or 'attentive'
            alpha = 0.3 * np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(len(t))
            theta = 0.2 * np.sin(2 * np.pi * 6 * t)
            beta = 0.8 * np.sin(2 * np.pi * 22 * t) + 0.15 * np.random.randn(len(t))
            hrv = 0.5 + 0.2 * np.sin(2 * np.pi * 0.3 * t)  # Lower coherence
            resp = 0.6 + 0.15 * np.sin(2 * np.pi * 0.4 * t)  # Faster breathing
            eda = 0.7 + 0.2 * np.sin(2 * np.pi * 0.2 * t)   # Higher arousal
        
        signals[prefix + 'alpha'] = alpha
        signals[prefix + 'beta'] = beta
        signals[prefix + 'theta'] = theta
        signals[prefix + 'hrv'] = hrv
        signals[prefix + 'resp'] = resp
        signals[prefix + 'eda'] = eda
    
    return t, signals

# ============================================================
# 2. FEATURE EXTRACTION & COHERENCE VECTOR
# ============================================================
def extract_features(t, signals, fs=256):
    """Extract band powers, HRV, coherence metrics."""
    features = {}
    for key in ['alpha', 'beta', 'theta']:
        # Simple band power via Welch or RMS for demo
        power = np.mean([np.sqrt(np.mean(signals[f'p{i+1}_{key}']**2)) for i in range(3)])
        features[key + '_power'] = np.clip(power, 0, 1)
    
    # Group HRV coherence (RMSSD proxy)
    hrv_vals = [signals[f'p{i+1}_hrv'] for i in range(3)]
    features['group_hrv_coherence'] = np.mean([np.std(h) for h in hrv_vals])  # Simplified
    features['group_hrv_coherence'] = np.clip(1 - features['group_hrv_coherence'], 0, 1)  # Higher = more coherent
    
    features['avg_resp_rate'] = np.mean([np.mean(signals[f'p{i+1}_resp']) for i in range(3)])
    features['avg_eda'] = np.mean([np.mean(signals[f'p{i+1}_eda']) for i in range(3)])
    
    # Simple 'coherence vector' scalar for demo (0-1)
    coherence = (features['alpha_power'] * 0.4 + features['group_hrv_coherence'] * 0.4 + (1 - features['avg_eda']) * 0.2)
    features['coherence_vector'] = np.clip(coherence, 0, 1)
    
    return features

# ============================================================
# 3. MAPPING TO GENERATIVE & SONIFICATION PARAMETERS
# ============================================================
def map_to_parameters(features, phase='grounding'):
    """Map features to visual/audio control parameters. Supports blending with external layers."""
    coherence = features['coherence_vector']
    alpha_p = features['alpha_power']
    beta_p = features['beta_power']
    
    params = {
        'visual_complexity': np.clip(beta_p * 1.5 + (1 - coherence) * 0.5, 0.2, 2.0),
        'symmetry_strength': np.clip(coherence * 0.9 + alpha_p * 0.3, 0.3, 1.0),
        'animation_speed': np.clip(0.5 + beta_p * 1.5, 0.3, 3.0),
        'color_hue_shift': np.clip((1 - coherence) * 0.3 + alpha_p * 0.2, 0, 0.6),  # 0=calm blue-green, 1=energetic
        'particle_density': np.clip(coherence * 0.6 + 0.4, 0.3, 1.0),
        'audio_base_freq': 180 + alpha_p * 120,  # Hz
        'audio_mod_depth': beta_p * 0.8,
        'isochronic_rate': 5 if phase == 'release' else (40 if phase == 'attention' else 10),
        'external_blend_opacity': np.clip(1 - coherence, 0.2, 0.8),  # How much to blend with other animations
        'coherence_vector': coherence
    }
    return params

# ============================================================
# 4. CYMATIC GENERATION (2D Wave Simulation)
# ============================================================
def generate_cymatic_pattern(params, size=256, save_path='cymatic_output.png'):
    """Simulate 2D standing waves (Faraday/cymatic patterns) based on params."""
    x = np.linspace(-np.pi, np.pi, size)
    y = np.linspace(-np.pi, np.pi, size)
    X, Y = np.meshgrid(x, y)
    
    complexity = params['visual_complexity']
    symmetry = params['symmetry_strength']
    speed = params['animation_speed']
    
    # Multi-mode wave equation approximation (radial + angular)
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    # Base radial waves + angular modulation
    Z = (np.sin(complexity * r * 3) * np.cos(symmetry * theta * 4) * 
         np.exp(-r * 0.3) +  # Damping
         0.4 * np.sin(complexity * 1.5 * r + speed * 2))
    
    # Normalize and enhance contrast for visual appeal
    Z = (Z - Z.min()) / (Z.max() - Z.min() + 1e-8)
    Z = np.clip(Z ** 0.8, 0, 1)  # Gamma-like
    
    plt.figure(figsize=(8, 8))
    plt.imshow(Z, cmap='viridis', extent=[-np.pi, np.pi, -np.pi, np.pi])
    plt.title(f"Mindala Cymatic | Coherence: {params['coherence_vector']:.2f} | Complexity: {complexity:.2f}")
    plt.axis('off')
    plt.colorbar(label='Wave Amplitude')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved cymatic pattern to {save_path}")
    return Z

# ============================================================
# 5. MAIN DEMO LOOP
# ============================================================
def run_demo():
    print("=== Mindala Pipeline Demo ===\n")
    states = ['relaxed', 'focused']
    phases = ['grounding', 'attention', 'release']
    
    for state in states:
        print(f"\n--- State: {state.upper()} ---")
        t, signals = simulate_biometrics(state=state)
        features = extract_features(t, signals)
        
        for phase in phases:
            params = map_to_parameters(features, phase=phase)
            print(f"Phase: {phase} | Coherence: {params['coherence_vector']:.3f}")
            print(f"  Visual: complexity={params['visual_complexity']:.2f}, symmetry={params['symmetry_strength']:.2f}, speed={params['animation_speed']:.2f}")
            print(f"  Audio: base_freq={params['audio_base_freq']:.0f}Hz, isochronic={params['isochronic_rate']}Hz, mod={params['audio_mod_depth']:.2f}")
            print(f"  Blend opacity for external layers: {params['external_blend_opacity']:.2f}")
            
            # Generate cymatic visual
            cymatic = generate_cymatic_pattern(params, save_path=f'cymatic_{state}_{phase}.png')
            
            # OSC-style output for video mapping integration
            print("  OSC Control Vector (example for Resolume/TouchDesigner):")
            print(f"    /mindala/coherence {params['coherence_vector']:.3f}")
            print(f"    /mindala/complexity {params['visual_complexity']:.3f}")
            print(f"    /mindala/symmetry {params['symmetry_strength']:.3f}")
            print(f"    /mindala/speed {params['animation_speed']:.3f}")
            print(f"    /mindala/blend_opacity {params['external_blend_opacity']:.3f}")
            print(f"    /mindala/isochronic_rate {params['isochronic_rate']}")
            
            # Example blending instruction
            print("  Mixing tip: Use blend_opacity to fade between Mindala cymatic layer and your existing Resolume/TouchDesigner animations or shaders.")
            
            time.sleep(0.5)  # Simulate real-time pacing
    
    print("\n=== Demo Complete ===")
    print("Generated cymatic PNGs demonstrate the visual output.")
    print("Use the printed OSC addresses to drive parameters in your preferred mapping software.")
    print("For full integration: Send these values via OSC to control shader uniforms, layer opacity, or generative params in real-time.")

if __name__ == "__main__":
    run_demo()
