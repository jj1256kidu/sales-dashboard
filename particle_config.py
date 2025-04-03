"""
Particle theme configuration for the futuristic login page.
This file contains the tsParticles configuration settings.
"""

PARTICLE_CONFIG = {
    "fullScreen": {
        "enable": False
    },
    "background": {
        "color": "#0f0c29"
    },
    "particles": {
        "number": {
            "value": 100
        },
        "color": {
            "value": ["#00f0ff", "#ff00e0", "#ffc400"]
        },
        "shape": {
            "type": ["circle", "square"]
        },
        "opacity": {
            "value": 0.7
        },
        "size": {
            "value": 4
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
        "events": {
            "onHover": {
                "enable": True,
                "mode": "repulse"
            },
            "onClick": {
                "enable": True,
                "mode": "push"
            }
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
    "detectRetina": True
}

# Simple theme configurations
NEON_THEME = {
    "colors": {
        "primary": "#00f0ff",
        "secondary": "#ff00e0",
        "accent": "#ffc400",
        "background": "#0f0c29"
    }
}

CYBER_THEME = {
    "colors": {
        "primary": "#00f0ff",
        "secondary": "#ff00e0",
        "accent": "#ffc400",
        "background": "#000033"
    }
}

MATRIX_THEME = {
    "colors": {
        "primary": "#00ff00",
        "secondary": "#00ff00",
        "accent": "#00ff00",
        "background": "#000000"
    }
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
    
    # Update base configuration with theme colors
    config = PARTICLE_CONFIG.copy()
    config["particles"]["color"]["value"] = [
        theme["colors"]["primary"],
        theme["colors"]["secondary"],
        theme["colors"]["accent"]
    ]
    config["background"]["color"] = theme["colors"]["background"]
    
    return config 
