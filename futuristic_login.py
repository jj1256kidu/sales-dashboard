import streamlit as st
import streamlit.components.v1 as components
import time
import json
import pandas as pd
from particle_config import get_theme_config

# Initialize session state for debugging and theme
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
    st.session_state.login_attempts = 0
    st.session_state.debug_log = []
    st.session_state.last_error = None
    st.session_state.theme = "neon"
    st.session_state.performance_metrics = {
        'page_load_time': time.time(),
        'login_attempts_timing': []
    }

def log_debug_event(event_type, details):
    if st.session_state.debug_mode:
        st.session_state.debug_log.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'type': event_type,
            'details': details
        })

# Page configuration
st.set_page_config(
    page_title="Futuristic Login",
    layout="centered",
    page_icon="🔐",
    initial_sidebar_state="collapsed"
)

# Inject Colorful Floating Particles
components.html("""
<div id="tsparticles"></div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<script>
  tsParticles.load("tsparticles", {
    fullScreen: { enable: true, zIndex: -1 },
    background: { color: "#0a0520" },
    particles: {
      number: { value: 80 },
      color: { value: ["#00f0ff", "#ff00e0", "#ffc400", "#00ff99"] },
      shape: { type: ["circle", "square"] },
      opacity: { 
        value: 0.6,
        random: true,
        animation: {
          enable: true,
          speed: 1,
          minimumValue: 0.3,
          sync: false
        }
      },
      size: { 
        value: { min: 2, max: 4 },
        animation: {
          enable: true,
          speed: 2,
          minimumValue: 0.5,
          sync: false
        }
      },
      move: {
        enable: true,
        speed: 1.2,
        direction: "none",
        random: true,
        outModes: "bounce",
        attract: {
          enable: true,
          rotateX: 600,
          rotateY: 1200
        }
      },
      links: {
        enable: true,
        distance: 150,
        color: "#00f0ff",
        opacity: 0.2,
        width: 1
      }
    },
    interactivity: {
      events: {
        onHover: { enable: true, mode: ["grab", "bubble"] },
        onClick: { enable: true, mode: "push" }
      },
      modes: {
        grab: {
          distance: 140,
          links: { opacity: 0.4 }
        },
        bubble: {
          distance: 200,
          size: 6,
          duration: 2,
          opacity: 0.8,
          speed: 3
        },
        push: { quantity: 4 }
      }
    },
    detectRetina: true
  });
</script>
""", height=0)

# Custom CSS
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500&display=swap" rel="stylesheet">

<style>
.stApp {
    background: transparent !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

div[data-testid="stVerticalBlock"] {
    padding-top: 2rem;
}

.login-box {
    background: rgba(2, 4, 18, 0.85);
    border-radius: 25px;
    padding: 30px;
    width: 380px;
    margin: 50px auto;
    box-shadow: 0 0 30px rgba(0, 240, 255, 0.15),
               inset 0 0 20px rgba(0, 240, 255, 0.05);
    backdrop-filter: blur(10px);
    font-family: 'Orbitron', sans-serif;
    border: 1px solid rgba(0, 240, 255, 0.1);
    position: relative;
    z-index: 1;
}

.login-box h2 {
    text-align: center;
    color: #00f0ff;
    margin: 0 0 30px 0;
    font-size: 28px;
    font-weight: 500;
    letter-spacing: 2px;
    text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
}

.input-wrapper {
    position: relative;
    margin-bottom: 20px;
}

.input-wrapper i {
    position: absolute;
    top: 50%;
    left: 18px;
    transform: translateY(-50%);
    color: #00f0ff;
    font-size: 15px;
    opacity: 0.8;
    z-index: 2;
}

.input-wrapper input {
    width: 100%;
    height: 45px;
    padding: 0 20px 0 45px;
    border: 1px solid rgba(0, 240, 255, 0.3);
    background: rgba(0, 0, 0, 0.25);
    color: #fff;
    border-radius: 50px;
    font-size: 14px;
    letter-spacing: 1px;
    font-family: 'Orbitron', sans-serif;
    outline: none;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.1),
               inset 0 0 10px rgba(0, 240, 255, 0.05);
}

.input-wrapper input:focus {
    border-color: rgba(0, 240, 255, 0.6);
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2),
               inset 0 0 15px rgba(0, 240, 255, 0.1);
    background: rgba(0, 0, 0, 0.3);
}

.input-wrapper input::placeholder {
    color: rgba(255, 255, 255, 0.4);
    letter-spacing: 1px;
    font-weight: 400;
    font-size: 14px;
}

.login-button {
    width: 100%;
    height: 45px;
    background: linear-gradient(90deg, #00f0ff, #ff00ff);
    color: white;
    font-weight: 500;
    font-size: 16px;
    letter-spacing: 3px;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    margin-top: 15px;
    text-transform: uppercase;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    font-family: 'Orbitron', sans-serif;
    transition: all 0.3s ease;
}

.login-button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(0, 240, 255, 0.3);
    background: linear-gradient(90deg, #ff00ff, #00f0ff);
}

.options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: rgba(0, 240, 255, 0.7);
    margin-top: 15px;
    letter-spacing: 0.5px;
}

.options label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    opacity: 0.9;
}

.options input[type="checkbox"] {
    accent-color: #00f0ff;
    width: 14px;
    height: 14px;
    opacity: 0.8;
}

.options a {
    color: rgba(0, 240, 255, 0.7);
    text-decoration: none;
    opacity: 0.8;
    transition: opacity 0.3s;
}

.options a:hover {
    opacity: 1;
    text-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
}

div[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Login Form UI
st.markdown("""
<div class="login-box">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
        <i class="fas fa-user"></i>
        <input type="text" placeholder="Username" name="username" required />
    </div>
    <div class="input-wrapper">
        <i class="fas fa-lock"></i>
        <input type="password" placeholder="Password" name="password" required />
    </div>
    <button class="login-button" type="submit">LOGIN</button>
    <div class="options">
        <label><input type="checkbox" checked /> Remember me</label>
        <a href="#">Forgot password?</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Debug section
if st.session_state.debug_mode:
    st.write("---")
    st.write("### Debug Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("#### System Status")
        st.write(f"- Session Duration: {int(time.time() - st.session_state.performance_metrics['page_load_time'])}s")
        st.write(f"- Login Attempts: {st.session_state.login_attempts}")
    
    with col2:
        st.write("#### Performance Metrics")
        if st.session_state.performance_metrics['login_attempts_timing']:
            avg_time = sum(st.session_state.performance_metrics['login_attempts_timing']) / len(st.session_state.performance_metrics['login_attempts_timing'])
            st.write(f"- Avg Login Time: {avg_time:.2f}s")
    
    with col3:
        if st.button("Clear Debug Log"):
            st.session_state.debug_log = []
            st.session_state.login_attempts = 0
            log_debug_event('system', 'Debug log cleared')
    
    if st.session_state.debug_log:
        st.write("#### Debug Log")
        log_df = pd.DataFrame(st.session_state.debug_log)
        st.dataframe(log_df, height=200)
        
        if st.button("Export Debug Log"):
            log_json = json.dumps(st.session_state.debug_log, indent=2)
            st.download_button(
                "Download Debug Log",
                log_json,
                "debug_log.json",
                "application/json"
            ) 
