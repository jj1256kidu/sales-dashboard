"""
Particle theme configuration for the futuristic login page.
This file contains the tsParticles configuration settings.
"""

PARTICLE_CONFIG = {
    "fullScreen": {
        "enable": True,
        "zIndex": 0
    },
    "fpsLimit": 60,
    "background": {
        "color": "#0f0c29"
    },
    "particles": {
        "number": {
            "value": 80,
            "density": {
                "enable": True,
                "value_area": 800
            }
        },
        "color": {
            "value": ["#00f0ff", "#ff00e0", "#ffc400"]
        },
        "shape": {
            "type": ["circle", "triangle"],
            "options": {
                "triangle": {
                    "sides": 3
                }
            }
        },
        "opacity": {
            "value": 0.8,
            "random": True,
            "anim": {
                "enable": True,
                "speed": 1,
                "opacity_min": 0.4,
                "sync": False
            }
        },
        "size": {
            "value": 6,
            "random": True,
            "anim": {
                "enable": True,
                "speed": 2,
                "size_min": 3,
                "sync": False
            }
        },
        "line_linked": {
            "enable": True,
            "distance": 150,
            "color": "#00f0ff",
            "opacity": 0.6,
            "width": 1
        },
        "move": {
            "enable": True,
            "speed": 2,
            "direction": "none",
            "random": False,
            "straight": False,
            "outModes": {
                "default": "bounce"
            },
            "attract": {
                "enable": True,
                "rotateX": 600,
                "rotateY": 1200
            }
        }
    },
    "interactivity": {
        "detect_on": "window",
        "events": {
            "onHover": {
                "enable": True,
                "mode": ["grab", "bubble"]
            },
            "onClick": {
                "enable": True,
                "mode": "push"
            },
            "resize": True
        },
        "modes": {
            "grab": {
                "distance": 140,
                "line_linked": {
                    "opacity": 0.8
                }
            },
            "bubble": {
                "distance": 200,
                "size": 12,
                "duration": 2,
                "opacity": 0.8,
                "speed": 3
            },
            "push": {
                "particles_nb": 6
            }
        }
    },
    "retina_detect": True
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
        "primary": "#0af",
        "secondary": "#f0a",
        "accent": "#fa0",
        "background": "#000033"
    }
}

MATRIX_THEME = {
    "colors": {
        "primary": "#0f0",
        "secondary": "#0f0",
        "accent": "#0f0",
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
    config["particles"]["line_linked"]["color"] = theme["colors"]["primary"]
    
    return config 
