#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

DEFAULT_CONFIG = {
    'camera': 0,
    'mode': 0,  # 0: Normal, 1: Above, 2: Behind
    'sensitivity': 30,
    'smoothing': 3,  # 1-10, higher = smoother but slower
    'dead_zone': 2,  # pixels, movements below this are ignored
    'skip_setup': False
}

def load_config():
    """Load config from file, return defaults if not found"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                return {**DEFAULT_CONFIG, **config}
    except Exception as e:
        print(f"[NonMouse] Error loading config: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save config to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"[NonMouse] Config saved to {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"[NonMouse] Error saving config: {e}")
        return False

def get_config_value(key, default=None):
    """Get a single config value"""
    config = load_config()
    return config.get(key, default)

def set_config_value(key, value):
    """Set a single config value"""
    config = load_config()
    config[key] = value
    return save_config(config)
