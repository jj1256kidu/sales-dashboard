"""
Particle theme configuration for the futuristic login page.
This file contains the tsParticles configuration settings.
"""

PARTICLE_CONFIG = {
    "fullScreen": {
        "enable": True,
        "zIndex": 1
    },
    "fpsLimit": 60,
    "particles": {
        "number": {
            "value": 80,
            "density": {
                "enable": True,
                "value_area": 800
            }
        },
        "color": {
            "value": ["#00f0ff", "#ff00e0", "#00ff00"],
            "animation": {
                "enable": True,
                "speed": 20,
                "sync": False
            }
        },
        "shape": {
            "type": ["circle", "triangle", "star"],
            "options": {
                "star": {
                    "sides": 5
                }
            }
        },
        "opacity": {
            "value": 1,
            "random": False,
            "animation": {
                "enable": True,
                "speed": 1,
                "minimumValue": 0.6,
                "sync": False
            }
        },
        "size": {
            "value": 15,
            "random": True,
            "animation": {
                "enable": True,
                "speed": 2,
                "minimumValue": 8,
                "sync": False
            }
        },
        "links": {
            "enable": True,
            "distance": 150,
            "color": "#00f0ff",
            "opacity": 0.8,
            "width": 3,
            "triangles": {
                "enable": True,
                "opacity": 0.4
            }
        },
        "move": {
            "enable": True,
            "speed": 4,
            "direction": "none",
            "random": True,
            "straight": False,
            "outModes": {
                "default": "bounce",
                "bottom": "bounce",
                "left": "bounce",
                "right": "bounce",
                "top": "bounce"
            },
            "attract": {
                "enable": True,
                "rotateX": 600,
                "rotateY": 1200
            }
        },
        "rotate": {
            "random": True,
            "direction": "random",
            "animation": {
                "enable": True,
                "speed": 5,
                "sync": False
            }
        },
        "glow": {
            "enable": True,
            "color": "#00f0ff",
            "blur": 20
        }
    },
    "interactivity": {
        "detectsOn": "canvas",
        "events": {
            "onHover": {
                "enable": True,
                "mode": ["grab", "bubble"],
                "parallax": {
                    "enable": True,
                    "force": 60,
                    "smooth": 10
                }
            },
            "onClick": {
                "enable": True,
                "mode": "push"
            },
            "resize": True
        },
        "modes": {
            "grab": {
                "distance": 250,
                "links": {
                    "opacity": 1,
                    "color": "#ff00e0"
                }
            },
            "bubble": {
                "distance": 250,
                "size": 25,
                "duration": 2,
                "opacity": 1,
                "color": "#00f0ff"
            },
            "push": {
                "quantity": 6
            }
        }
    },
    "background": {
        "color": "#0f0c29"
    },
    "detectRetina": True,
    "motion": {
        "disable": False,
        "reduce": {
            "factor": 4,
            "value": True
        }
    }
}

# Preset themes with larger particles
NEON_THEME = {
    "colors": {
        "primary": "#00f0ff",
        "secondary": "#ff00e0",
        "accent": "#00ff00",
        "background": "#0f0c29"
    },
    "particle_size": 15,
    "particle_count": 80,
    "movement_speed": 4
}

CYBER_THEME = {
    "colors": {
        "primary": "#0ff",
        "secondary": "#f0f",
        "accent": "#ff0",
        "background": "#000033"
    },
    "particle_size": 18,
    "particle_count": 60,
    "movement_speed": 5
}

MATRIX_THEME = {
    "colors": {
        "primary": "#00ff00",
        "secondary": "#003300",
        "accent": "#00cc00",
        "background": "#000000"
    },
    "particle_size": 12,
    "particle_count": 100,
    "movement_speed": 3
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
