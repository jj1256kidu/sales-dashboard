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

# Page configuration with error handling
try:
    st.set_page_config(page_title="Futuristic Login", layout="wide", initial_sidebar_state="collapsed")
    log_debug_event('config', 'Page configuration successful')
except Exception as e:
    st.error(f"Page configuration error: {str(e)}")
    log_debug_event('error', f'Page configuration failed: {str(e)}')
    st.session_state.last_error = str(e)

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
    st.session_state.theme = st.selectbox(
        "Select Theme",
        ["Neon", "Cyber", "Matrix"],
        index=["Neon", "Cyber", "Matrix"].index(st.session_state.theme.capitalize())
    )

# Get particle configuration based on selected theme
particle_config = get_theme_config(st.session_state.theme)

# Update the particle initialization in the JavaScript
particles_init = f"""
    try {{
      tsParticles.load("tsparticles", {json.dumps(particle_config)}).then(() => {{
        logToDebug('Particles initialized successfully', 'system');
      }}).catch(error => {{
        errorCount++;
        console.error('Particles initialization error:', error);
        logToDebug(`Particles error: ${{error.message}}`, 'error');
        document.getElementById('errors').textContent = `Particle Init: ${{error.message}}`;
      }});
    }} catch (error) {{
      errorCount++;
      console.error('Critical error:', error);
      logToDebug(`Critical error: ${{error.message}}`, 'error');
      document.getElementById('errors').textContent = `Critical: ${{error.message}}`;
    }}
"""

# Title with reduced margin
st.markdown("<h1 style='text-align:center; color:cyan; margin: 0 0 1rem 0;'>🚀 Welcome to the Futuristic Login Page</h1>", unsafe_allow_html=True)

# Read and display the HTML file
with open('login.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
    components.html(html_content, height=800, width=None, scrolling=False)

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
