class ParticleConfig:
    """Configuration class for particle effects in the login page."""
    
    # Particle appearance
    PARTICLE_COUNT = 50
    PARTICLE_MIN_SIZE = 1
    PARTICLE_MAX_SIZE = 4
    PARTICLE_COLOR = "rgba(108, 99, 255, 0.3)"
    PARTICLE_SHAPE = "circle"  # circle, square, or triangle
    
    # Animation settings
    ANIMATION_DURATION_MIN = 10
    ANIMATION_DURATION_MAX = 20
    ANIMATION_TYPE = "float"  # float, bounce, or wave
    
    # Movement patterns
    MOVEMENT_RANGE_X = 100  # pixels
    MOVEMENT_RANGE_Y = "100vh"  # viewport height
    MOVEMENT_SPEED = "linear"  # linear, ease, or ease-in-out
    
    # Interactive settings
    INTERACTIVE = True
    HOVER_EFFECT = True
    CLICK_EFFECT = True
    
    # Performance settings
    MAX_PARTICLES = 100
    FPS_LIMIT = 60
    USE_REQUEST_ANIMATION_FRAME = True
    
    @classmethod
    def get_particle_style(cls, x, y, size, duration):
        """Generate CSS style for a particle."""
        return f"""
            left: {x}px;
            top: {y}px;
            width: {size}px;
            height: {size}px;
            background: {cls.PARTICLE_COLOR};
            border-radius: {cls._get_border_radius()};
            animation: {cls.ANIMATION_TYPE} {duration}s {cls.MOVEMENT_SPEED} infinite;
        """
    
    @classmethod
    def _get_border_radius(cls):
        """Get border radius based on particle shape."""
        if cls.PARTICLE_SHAPE == "circle":
            return "50%"
        elif cls.PARTICLE_SHAPE == "square":
            return "0"
        elif cls.PARTICLE_SHAPE == "triangle":
            return "0"
        return "50%"
    
    @classmethod
    def get_animation_keyframes(cls):
        """Generate CSS keyframes for particle animation."""
        if cls.ANIMATION_TYPE == "float":
            return f"""
                @keyframes float {{
                    0% {{
                        transform: translateY(0) translateX(0);
                        opacity: 0;
                    }}
                    10% {{
                        opacity: 1;
                    }}
                    90% {{
                        opacity: 1;
                    }}
                    100% {{
                        transform: translateY(-{cls.MOVEMENT_RANGE_Y}) translateX({cls.MOVEMENT_RANGE_X}px);
                        opacity: 0;
                    }}
                }}
            """
        elif cls.ANIMATION_TYPE == "bounce":
            return """
                @keyframes bounce {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-20px);
                    }
                }
            """
        elif cls.ANIMATION_TYPE == "wave":
            return """
                @keyframes wave {
                    0%, 100% {
                        transform: translateX(0);
                    }
                    50% {
                        transform: translateX(20px);
                    }
                }
            """
    
    @classmethod
    def get_particle_script(cls):
        """Generate JavaScript for particle creation and management."""
        return f"""
        <script>
            class ParticleSystem {{
                constructor() {{
                    this.container = document.getElementById('particles');
                    this.particles = [];
                    this.maxParticles = {cls.MAX_PARTICLES};
                    this.fpsLimit = {cls.FPS_LIMIT};
                    this.lastFrameTime = 0;
                    this.frameInterval = 1000 / this.fpsLimit;
                }}

                createParticle() {{
                    if (this.particles.length >= this.maxParticles) return;

                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    
                    const x = Math.random() * window.innerWidth;
                    const y = Math.random() * window.innerHeight;
                    const size = Math.random() * ({cls.PARTICLE_MAX_SIZE} - {cls.PARTICLE_MIN_SIZE}) + {cls.PARTICLE_MIN_SIZE};
                    const duration = Math.random() * ({cls.ANIMATION_DURATION_MAX} - {cls.ANIMATION_DURATION_MIN}) + {cls.ANIMATION_DURATION_MIN};
                    
                    particle.style.cssText = `{cls.get_particle_style(x, y, size, duration)}`;
                    
                    if ({str(cls.INTERACTIVE).lower()}) {{
                        this._addInteractivity(particle);
                    }}
                    
                    this.container.appendChild(particle);
                    this.particles.push(particle);
                    
                    // Remove particle after animation
                    setTimeout(() => {{
                        particle.remove();
                        this.particles = this.particles.filter(p => p !== particle);
                    }}, duration * 1000);
                }}

                _addInteractivity(particle) {{
                    if ({str(cls.HOVER_EFFECT).lower()}) {{
                        particle.addEventListener('mouseenter', () => {{
                            particle.style.transform = 'scale(2)';
                            particle.style.background = '{cls.PARTICLE_COLOR.replace("0.3", "0.6")}';
                        }});
                        
                        particle.addEventListener('mouseleave', () => {{
                            particle.style.transform = 'scale(1)';
                            particle.style.background = '{cls.PARTICLE_COLOR}';
                        }});
                    }}

                    if ({str(cls.CLICK_EFFECT).lower()}) {{
                        particle.addEventListener('click', () => {{
                            particle.style.animation = 'none';
                            particle.style.transform = 'scale(3)';
                            particle.style.opacity = '0';
                            setTimeout(() => particle.remove(), 500);
                        }});
                    }}
                }}

                update() {{
                    const now = performance.now();
                    const delta = now - this.lastFrameTime;

                    if (delta >= this.frameInterval) {{
                        this.lastFrameTime = now - (delta % this.frameInterval);
                        
                        if (this.particles.length < this.maxParticles) {{
                            this.createParticle();
                        }}
                    }}

                    if ({str(cls.USE_REQUEST_ANIMATION_FRAME).lower()}) {{
                        requestAnimationFrame(() => this.update());
                    }}
                }}

                start() {{
                    // Create initial particles
                    for (let i = 0; i < {cls.PARTICLE_COUNT}; i++) {{
                        this.createParticle();
                    }}
                    
                    // Start update loop
                    this.update();
                }}
            }}

            // Initialize particle system
            document.addEventListener('DOMContentLoaded', () => {{
                const particleSystem = new ParticleSystem();
                particleSystem.start();
            }});
        </script>
        """ 
