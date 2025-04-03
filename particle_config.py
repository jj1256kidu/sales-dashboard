"""
Particle theme configuration for the futuristic login page.
This file contains the tsParticles configuration settings.
"""

PARTICLE_CONFIG = {
    "fullScreen": {
        "enable": False
    },
    "fpsLimit": 60,
    "particles": {
        "number": {
            "value": 100,
            "density": {
                "enable": True,
                "value_area": 800
            }
        },
        "color": {
            "value": ["#00f0ff", "#ff00e0", "#ffc400"]
        },
        "shape": {
            "type": ["circle", "square"]
        },
        "opacity": {
            "value": 0.7,
            "random": False
        },
        "size": {
            "value": 4,
            "random": False
        },
        "move": {
            "enable": True,
            "speed": 1,
            "direction": "none",
            "random": False,
            "straight": False,
            "outModes": "bounce"
        }
    },
    "interactivity": {
        "detectsOn": "canvas",
        "events": {
            "onHover": {
                "enable": True,
                "mode": "repulse"
            },
            "onClick": {
                "enable": True,
                "mode": "push"
            },
            "resize": True
        },
        "modes": {
            "repulse": {
                "distance": 100
            },
            "push": {
                "quantity": 4
            }
        }
    },
    "background": {
        "color": "#0f0c29"
    },
    "detectRetina": True
}

# Preset themes with simpler particle settings
NEON_THEME = {
    "colors": {
        "primary": "#00f0ff",
        "secondary": "#ff00e0",
        "accent": "#ffc400",
        "background": "#0f0c29"
    },
    "particle_size": 4,
    "particle_count": 100,
    "movement_speed": 1
}

CYBER_THEME = {
    "colors": {
        "primary": "#00f0ff",
        "secondary": "#ff00e0",
        "accent": "#ffc400",
        "background": "#000033"
    },
    "particle_size": 4,
    "particle_count": 100,
    "movement_speed": 1
}

MATRIX_THEME = {
    "colors": {
        "primary": "#00ff00",
        "secondary": "#00ff00",
        "accent": "#00ff00",
        "background": "#000000"
    },
    "particle_size": 4,
    "particle_count": 120,
    "movement_speed": 1
}

def get_theme_config(theme_name="neon"):
    """
    Get particle configuration for a specific theme.
    
    Args:
        theme_name (str): Name of the theme ("neon", "cyber", or "matrix")
        
    Returns:
        dict: Particle configuration dictionary
    """
    themes = {
        "neon": NEON_THEME,
        "cyber": CYBER_THEME,
        "matrix": MATRIX_THEME
    }
    
    theme = themes.get(theme_name.lower(), NEON_THEME)
    
    # Update base configuration with theme settings
    config = PARTICLE_CONFIG.copy()
    config["particles"]["number"]["value"] = theme["particle_count"]
    config["particles"]["size"]["value"] = theme["particle_size"]
    config["particles"]["move"]["speed"] = theme["movement_speed"]
    config["particles"]["color"]["value"] = [
        theme["colors"]["primary"],
        theme["colors"]["secondary"],
        theme["colors"]["accent"]
    ]
    config["background"]["color"] = theme["colors"]["background"]
    
    return config 
