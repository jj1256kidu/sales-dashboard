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

# Inject Particles
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

# Custom CSS for futuristic look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

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
        background: rgba(2, 4, 18, 0.8);
        border-radius: 30px;
        padding: 25px;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.1);
        backdrop-filter: blur(20px);
        width: 360px;
        margin: 0 auto;
        font-family: 'Orbitron', sans-serif;
    }

    .login-title {
        text-align: center;
        color: #00f0ff;
        margin: 0 0 25px 0;
        font-size: 26px;
        font-weight: 500;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    .stTextInput > div > div > input {
        width: 100% !important;
        height: 48px !important;
        padding: 0 20px 0 45px !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        background: rgba(0, 0, 0, 0.2) !important;
        color: #fff !important;
        border-radius: 50px !important;
        font-size: 15px !important;
        letter-spacing: 2px !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1),
                   inset 0 0 15px rgba(0, 240, 255, 0.1) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00f0ff !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2),
                   inset 0 0 20px rgba(0, 240, 255, 0.15) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
        letter-spacing: 2px !important;
        font-weight: 400 !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        background: linear-gradient(90deg, #00f0ff 0%, #ff00ff 100%) !important;
        color: white !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        letter-spacing: 4px !important;
        border: none !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        margin-top: 10px !important;
        text-transform: uppercase !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.4) !important;
    }

    .stCheckbox {
        color: rgba(0, 240, 255, 0.8) !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
    }

    .stCheckbox > label > div {
        gap: 6px !important;
    }

    .stCheckbox > label > div > input {
        accent-color: #00f0ff !important;
        width: 13px !important;
        height: 13px !important;
        opacity: 0.9 !important;
    }

    .forgot-password {
        text-align: right !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
        margin-top: 5px !important;
    }

    .forgot-password a {
        color: rgba(0, 240, 255, 0.8) !important;
        text-decoration: none !important;
        opacity: 0.9 !important;
        transition: opacity 0.3s !important;
    }

    .forgot-password a:hover {
        opacity: 1 !important;
    }

    div[data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    </style>
""", unsafe_allow_html=True)

# Login layout
with st.form("login_form"):
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 class="login-title">Welcome Back</h2>', unsafe_allow_html=True)

    username = st.text_input("", placeholder="Username", key="username")
    password = st.text_input("", placeholder="Password", type="password", key="password")

    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember me")
    with col2:
        st.markdown('<div class="forgot-password"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("LOGIN")

    if submitted:
        if username and password:
            st.session_state.login_attempts += 1
            log_debug_event('login_attempt', {'username': username, 'success': True})
            st.success(f"Welcome, {username}!")
        else:
            log_debug_event('login_attempt', {'error': 'Missing credentials'})
            st.error("Please enter both username and password.")

    st.markdown('</div>', unsafe_allow_html=True)

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
