import streamlit as st
import numpy as np
import time
from streamlit.components.v1 import html
from particle_config import ParticleConfig

# Custom CSS for futuristic styling
st.markdown("""
<style>
    /* Futuristic theme colors */
    :root {
        --primary-color: #00ff9d;
        --secondary-color: #00b8ff;
        --background-color: #0a0a0a;
        --card-background: rgba(255, 255, 255, 0.05);
        --text-color: #ffffff;
        --accent-color: #ff00ff;
        --border-color: rgba(255, 255, 255, 0.1);
    }

    /* Main container */
    .stApp {
        background: var(--background-color);
        color: var(--text-color);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Login container */
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: var(--card-background);
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }

    .login-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(0, 255, 157, 0.1),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }

    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    /* Form elements */
    .stTextInput > div > div > input,
    .stPassword > div > div > input {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stPassword > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.3) !important;
    }

    /* Labels */
    .stTextInput > label,
    .stPassword > label {
        color: var(--text-color) !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: black;
        border: none;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 157, 0.3);
    }

    .stButton > button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }

    /* Checkbox styling */
    .stCheckbox > label {
        color: var(--text-color) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }

    /* Links */
    .link-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    .link-container a {
        color: var(--primary-color);
        text-decoration: none;
        font-size: 0.9rem;
        transition: color 0.3s ease;
    }

    .link-container a:hover {
        color: var(--secondary-color);
    }

    /* Particles container */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Particle effect JavaScript
particles_js = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const container = document.createElement('div');
        container.className = 'particles';
        document.body.appendChild(container);

        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random position
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight;
            
            // Random size
            const size = Math.random() * 3 + 1;
            
            // Random animation duration
            const duration = Math.random() * 20 + 10;
            
            particle.style.cssText = `
                left: ${x}px;
                top: ${y}px;
                width: ${size}px;
                height: ${size}px;
                animation: float ${duration}s linear infinite;
            `;
            
            container.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                particle.remove();
            }, duration * 1000);
        }

        // Create initial particles
        for (let i = 0; i < 50; i++) {
            createParticle();
        }

        // Create new particles periodically
        setInterval(createParticle, 2000);
    });
</script>
"""

# Add particle effect
html(particles_js)

# Example customization
ParticleConfig.PARTICLE_COUNT = 75
ParticleConfig.PARTICLE_COLOR = "rgba(255, 0, 255, 0.3)"
ParticleConfig.ANIMATION_TYPE = "bounce"

def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Title with gradient effect
    st.markdown("""
        <h1 style="
            text-align: center;
            background: linear-gradient(45deg, #00ff9d, #00b8ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">Welcome Back</h1>
    """, unsafe_allow_html=True)
    
    # Login form
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    # Remember me checkbox
    remember_me = st.checkbox("Remember me", key="login_remember")
    
    # Login button
    if st.button("Login", key="login_button"):
        if username and password:
            with st.spinner("Authenticating..."):
                time.sleep(1)  # Simulate authentication
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.experimental_rerun()
        else:
            st.error("Please enter both username and password")
    
    # Links container
    st.markdown("""
        <div class="link-container">
            <a href="#">Forgot Password?</a>
            <a href="#">Create Account</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        st.success("You are logged in!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()

# In your HTML template
st.markdown(ParticleConfig.get_animation_keyframes(), unsafe_allow_html=True)
st.markdown(ParticleConfig.get_particle_script(), unsafe_allow_html=True) 
