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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        margin: 0;
        padding: 0;
        height: 100vh;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Debug mode toggle and information
with st.sidebar:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.debug_mode = st.checkbox("Debug Mode", value=st.session_state.debug_mode)
    with col2:
        if st.session_state.debug_mode and st.button("Clear Log"):
            st.session_state.debug_log = []
            st.session_state.login_attempts = 0
            log_debug_event('system', 'Debug log cleared')
    
    if st.session_state.debug_mode:
        st.write("### Debug Information")
        st.write("#### System Status")
        st.write(f"- Session Duration: {int(time.time() - st.session_state.performance_metrics['page_load_time'])}s")
        st.write(f"- Login Attempts: {st.session_state.login_attempts}")
        
        st.write("#### Performance Metrics")
        if st.session_state.performance_metrics['login_attempts_timing']:
            avg_time = sum(st.session_state.performance_metrics['login_attempts_timing']) / len(st.session_state.performance_metrics['login_attempts_timing'])
            st.write(f"- Avg Login Time: {avg_time:.2f}s")
        
        st.write("#### Last Error")
        if st.session_state.last_error:
            st.error(st.session_state.last_error)
        
        st.write("#### Debug Log")
        if st.session_state.debug_log:
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

# Theme selector in sidebar
with st.sidebar:
    theme = st.selectbox(
        "Select Theme",
        ["Neon", "Cyber", "Matrix"],
        index=0
    )

# Get particle configuration
particle_config = get_theme_config(theme)
particle_config_json = json.dumps(particle_config)

# Embed the login page with dynamic particle configuration
components.html(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Futuristic Login</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Orbitron', sans-serif;
        }}

        html, body {{
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            background: #0f0c29;
            margin: 0;
            padding: 0;
        }}

        #tsparticles {{
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
            pointer-events: none;
        }}

        .container {{
            position: relative;
            z-index: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 0;
        }}

        .login-box {{
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            padding: 15px 20px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            margin: 0;
        }}

        .login-box h2 {{
            text-align: center;
            color: #00f0ff;
            margin: 0 0 12px 0;
            font-size: 20px;
            line-height: 1;
        }}

        .input-wrapper {{
            position: relative;
            margin-bottom: 10px;
        }}

        .input-wrapper i {{
            position: absolute;
            top: 50%;
            left: 12px;
            transform: translateY(-50%);
            color: #7efcff;
            font-size: 12px;
        }}

        .input-wrapper input {{
            width: 100%;
            height: 36px;
            padding: 0 12px 0 32px;
            border: 1px solid #00f0ff;
            background: transparent;
            color: white;
            border-radius: 16px;
            font-size: 12px;
            outline: none;
            transition: box-shadow 0.3s;
        }}

        .input-wrapper input:focus {{
            box-shadow: 0 0 10px #00f0ff;
        }}

        .login-box button {{
            width: 100%;
            height: 36px;
            background: linear-gradient(135deg, #00f0ff, #ff00e0);
            color: white;
            font-weight: bold;
            font-size: 12px;
            border: none;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 2px;
        }}

        .login-box button:hover {{
            transform: scale(1.02);
            box-shadow: 0 0 15px #00f0ff;
        }}

        .options {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #a0cbe8;
            margin-top: 5px;
        }}

        .options a {{
            color: #a0cbe8;
            text-decoration: underline;
        }}

        @media (max-width: 480px) {{
            .login-box {{
                padding: 12px 15px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Particle Background -->
    <div id="tsparticles"></div>

    <!-- Login Form -->
    <div class="container">
        <form class="login-box">
            <h2>Welcome Back</h2>
            <div class="input-wrapper">
                <i class="fas fa-user"></i>
                <input type="text" placeholder="Username" required />
            </div>
            <div class="input-wrapper">
                <i class="fas fa-lock"></i>
                <input type="password" placeholder="Password" required />
            </div>
            <button type="submit">LOGIN</button>
            <div class="options">
                <label><input type="checkbox" checked /> Remember me</label>
                <a href="#">Forgot password?</a>
            </div>
        </form>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            tsParticles.load("tsparticles", {particle_config_json}).then(function() {{
                console.log('Particles loaded successfully');
            }}).catch(function(error) {{
                console.error('Error loading particles:', error);
            }});
        }});
    </script>
</body>
</html>
""", height=1000, width=None, scrolling=False)

# Enhanced debug controls
if st.session_state.debug_mode:
    st.write("---")
    st.write("### Debug Controls")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Simulate Success"):
            log_debug_event('test', 'Simulated successful login')
            st.session_state.login_attempts += 1
            st.session_state.performance_metrics['login_attempts_timing'].append(time.time() % 1)
            st.success("Login simulation successful!")
            
    with col2:
        if st.button("Simulate Error"):
            log_debug_event('test', 'Simulated login error')
            st.session_state.last_error = "Simulated authentication error"
            st.error("Login simulation failed!")
            
    with col3:
        if st.button("Clear Errors"):
            st.session_state.last_error = None
            log_debug_event('system', 'Errors cleared')
            st.info("Error log cleared") 
