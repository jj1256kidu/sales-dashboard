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
    st.set_page_config(page_title="Futuristic Login", layout="centered")
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

# Embed HTML with theme-based styling - fixed height/width and spacing
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
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: {particle_config["background"]["color"]};
        }}
        #tsparticles {{
            position: fixed;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            z-index: 1;
            pointer-events: none;
        }}
        .login-box {{
            position: fixed;
            z-index: 2;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.7);
            padding: 2rem;
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
            color: white;
            box-shadow: 0 0 25px {particle_config["particles"]["color"]["value"][0]}40;
            backdrop-filter: blur(10px);
        }}
        .login-box h2 {{
            text-align: center;
            color: {particle_config["particles"]["color"]["value"][0]};
            margin-bottom: 1.5rem;
        }}
        .input-wrapper {{
            position: relative;
            margin-bottom: 1rem;
        }}
        .input-wrapper i {{
            position: absolute;
            top: 50%;
            left: 15px;
            transform: translateY(-50%);
            color: {particle_config["particles"]["color"]["value"][0]};
        }}
        .input-wrapper input {{
            width: 100%;
            height: 45px;
            padding: 0 15px 0 40px;
            border: 1px solid {particle_config["particles"]["color"]["value"][0]};
            background: transparent;
            color: white;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
        }}
        .login-box button {{
            width: 100%;
            height: 48px;
            background: linear-gradient(135deg, 
                {particle_config["particles"]["color"]["value"][0]}, 
                {particle_config["particles"]["color"]["value"][1]}
            );
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }}
        .login-box button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px {particle_config["particles"]["color"]["value"][0]}40;
        }}
        .debug-info {{
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            background: rgba(0,0,0,0.9);
            padding: 1rem;
            border-radius: 8px;
            color: #00f0ff;
            font-size: 12px;
            z-index: 1000;
            display: none;
            border: 1px solid #00f0ff;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            max-width: 300px;
        }}
        .debug-info.show {{
            display: block;
        }}
        .debug-section {{
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.2);
        }}
        .debug-title {{
            color: #ff00e0;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .debug-value {{
            margin-left: 10px;
            word-break: break-all;
        }}
        .debug-error {{
            color: #ff3366;
        }}
    </style>
</head>
<body>
    <div id="tsparticles"></div>
    <div class="login-box">
        <h2>Welcome Back</h2>
        <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input type="text" placeholder="Username" id="username" oninput="logInput('username')" autocomplete="off"/>
        </div>
        <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input type="password" placeholder="Password" id="password" oninput="logInput('password')" autocomplete="off"/>
        </div>
        <button onclick="handleLogin()">LOGIN</button>
    </div>
    
    <!-- Enhanced debug information panel -->
    <div class="debug-info" id="debugInfo">
        <div class="debug-section">
            <div class="debug-title">System Status</div>
            <div class="debug-value" id="systemStatus">Initializing...</div>
        </div>
        <div class="debug-section">
            <div class="debug-title">Last Action</div>
            <div class="debug-value" id="lastAction">None</div>
        </div>
        <div class="debug-section">
            <div class="debug-title">Input Status</div>
            <div class="debug-value" id="inputStatus">Waiting</div>
        </div>
        <div class="debug-section">
            <div class="debug-title">Performance</div>
            <div class="debug-value" id="performance">Loading...</div>
        </div>
        <div class="debug-section">
            <div class="debug-title">Errors</div>
            <div class="debug-value debug-error" id="errors">None</div>
        </div>
    </div>

    <script>
        // Enhanced debug logging
        let debugStartTime = Date.now();
        let inputHistory = [];
        let errorCount = 0;
        
        function logToDebug(message, type = 'info') {
            if (window.debugMode) {
                const timestamp = new Date().toISOString();
                console.log(`[Debug][${type}][${timestamp}] ${message}`);
                
                // Update debug panel
                document.getElementById('lastAction').textContent = message;
                document.getElementById('systemStatus').textContent = `Running for ${((Date.now() - debugStartTime)/1000).toFixed(1)}s`;
                document.getElementById('performance').textContent = `Errors: ${errorCount}, Inputs: ${inputHistory.length}`;
                
                // Log to parent Streamlit
                window.parent.postMessage({
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Futuristic Login</title>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    * {{
      margin: 0; padding: 0; box-sizing: border-box;
      font-family: 'Orbitron', sans-serif;
    }}
    html, body {{
      height: 100vh;
      width: 100vw;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: {particle_config["background"]["color"]};
    }}
    #tsparticles {{
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      z-index: 0;
    }}
    .login-box {{
      position: absolute;
      z-index: 2;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0,0,0,0.7);
      padding: 40px;
      border-radius: 20px;
      width: 90%;
      max-width: 400px;
      color: white;
      box-shadow: 0 0 25px {particle_config["particles"]["color"]["value"][0]}40;
      backdrop-filter: blur(10px);
    }}
    .login-box h2 {{
      text-align: center;
      color: {particle_config["particles"]["color"]["value"][0]};
      margin-bottom: 30px;
    }}
    .input-wrapper {{
      position: relative;
      margin-bottom: 20px;
    }}
    .input-wrapper i {{
      position: absolute;
      top: 50%;
      left: 15px;
      transform: translateY(-50%);
      color: {particle_config["particles"]["color"]["value"][0]};
    }}
    .input-wrapper input {{
      width: 100%;
      height: 45px;
      padding: 0 15px 0 40px;
      border: 1px solid {particle_config["particles"]["color"]["value"][0]};
      background: transparent;
      color: white;
      border-radius: 25px;
      font-size: 14px;
      outline: none;
    }}
    .login-box button {{
      width: 100%;
      height: 48px;
      background: linear-gradient(135deg, 
        {particle_config["particles"]["color"]["value"][0]}, 
        {particle_config["particles"]["color"]["value"][1]}
      );
      color: white;
      font-weight: bold;
      font-size: 16px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      transition: all 0.3s ease;
    }}
    .login-box button:hover {{
      transform: translateY(-2px);
      box-shadow: 0 5px 15px {particle_config["particles"]["color"]["value"][0]}40;
    }}
    /* Enhanced debug styles */
    .debug-info {{
      position: fixed;
      bottom: 10px;
      right: 10px;
      background: rgba(0,0,0,0.9);
      padding: 15px;
      border-radius: 8px;
      color: #00f0ff;
      font-size: 12px;
      z-index: 1000;
      display: none;
      border: 1px solid #00f0ff;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
      max-width: 300px;
    }}
    .debug-info.show {{
      display: block;
    }}
    .debug-section {{
      margin-bottom: 10px;
      padding-bottom: 5px;
      border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    }}
    .debug-title {{
      color: #ff00e0;
      font-weight: bold;
      margin-bottom: 5px;
    }}
    .debug-value {{
      margin-left: 10px;
      word-break: break-all;
    }}
    .debug-error {{
      color: #ff3366;
    }}
  </style>
</head>
<body>
  <div id="tsparticles"></div>
  <div class="login-box">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username" id="username" oninput="logInput('username')" autocomplete="off"/>
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password" id="password" oninput="logInput('password')" autocomplete="off"/>
    </div>
    <button onclick="handleLogin()">LOGIN</button>
  </div>
  
  <!-- Enhanced debug information panel -->
  <div class="debug-info" id="debugInfo">
    <div class="debug-section">
      <div class="debug-title">System Status</div>
      <div class="debug-value" id="systemStatus">Initializing...</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Last Action</div>
      <div class="debug-value" id="lastAction">None</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Input Status</div>
      <div class="debug-value" id="inputStatus">Waiting</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Performance</div>
      <div class="debug-value" id="performance">Loading...</div>
    </div>
    <div class="debug-section">
      <div class="debug-title">Errors</div>
      <div class="debug-value debug-error" id="errors">None</div>
    </div>
  </div>

  <script>
    // Enhanced debug logging
    let debugStartTime = Date.now();
    let inputHistory = [];
    let errorCount = 0;
    
    function logToDebug(message, type = 'info') {
      if (window.debugMode) {
        const timestamp = new Date().toISOString();
        console.log(`[Debug][${type}][${timestamp}] ${message}`);
        
        // Update debug panel
        document.getElementById('lastAction').textContent = message;
        document.getElementById('systemStatus').textContent = `Running for ${((Date.now() - debugStartTime)/1000).toFixed(1)}s`;
        document.getElementById('performance').textContent = `Errors: ${errorCount}, Inputs: ${inputHistory.length}`;
        
        // Log to parent Streamlit
        window.parent.postMessage({
          type: 'streamlit:debug',
          message: message,
          timestamp: timestamp,
          category: type
        }, '*');
      }
    }

    // Enhanced input logging
    function logInput(field) {
      const input = document.getElementById(field);
      const timestamp = Date.now();
      const inputData = {
        field: field,
        length: input.value.length,
        timestamp: timestamp
      };
      inputHistory.push(inputData);
      
      logToDebug(`${field} changed: ${input.value.length} characters`, 'input');
      document.getElementById('inputStatus').textContent = 
        `${field} updated (${inputHistory.length} total inputs)`;
    }

    // Enhanced login handler
    function handleLogin() {
      const startTime = performance.now();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      
      try {
        logToDebug(`Login attempt started`, 'auth');
        
        if (!username || !password) {
          errorCount++;
          throw new Error('Empty fields');
        }
        
        // Simulate network delay
        setTimeout(() => {
          const endTime = performance.now();
          logToDebug(`Login attempt completed in ${(endTime-startTime).toFixed(1)}ms`, 'auth');
          alert('Simulated login. Integrate backend for real auth.');
        }, 500);
        
      } catch (error) {
        errorCount++;
        logToDebug(`Login error: ${error.message}`, 'error');
        document.getElementById('errors').textContent = error.message;
        alert('Please fill in all fields');
      }
    }

    // Initialize particles with theme configuration
    {particles_init}

    // Initialize debug mode
    window.debugMode = """ + str(st.session_state.debug_mode).lower() + """;
    if (window.debugMode) {
      document.getElementById('debugInfo').classList.add('show');
      logToDebug('Debug mode initialized', 'system');
    }
    
    // Performance monitoring
    window.addEventListener('load', () => {
      const loadTime = performance.now();
      logToDebug(`Page loaded in ${loadTime.toFixed(1)}ms`, 'performance');
    });
  </script>
</body>
</html>
""", height=600, width=800)

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
