import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for debugging
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
    st.session_state.login_attempts = 0

# Page configuration
try:
    st.set_page_config(page_title="Futuristic Login", layout="centered")
except Exception as e:
    st.error(f"Page configuration error: {str(e)}")

# Debug mode toggle
with st.sidebar:
    st.session_state.debug_mode = st.checkbox("Debug Mode", value=st.session_state.debug_mode)
    if st.session_state.debug_mode:
        st.write("Debug Information:")
        st.write(f"Login attempts: {st.session_state.login_attempts}")
        st.write("Session State:", st.session_state)

# Title
st.markdown("<h1 style='text-align:center; color:cyan;'>🚀 Welcome to the Futuristic Login Page</h1>", unsafe_allow_html=True)

# Embed HTML with console logging for debugging
components.html("""
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
    * {
      margin: 0; padding: 0; box-sizing: border-box;
      font-family: 'Orbitron', sans-serif;
    }
    html, body {
      height: 100%;
      background: #0f0c29;
    }
    #tsparticles {
      position: fixed;
      width: 100%;
      height: 100%;
      z-index: 0;
    }
    .login-box {
      position: relative;
      z-index: 1;
      margin: 0 auto;
      top: 10vh;
      background: rgba(0,0,0,0.7);
      padding: 40px;
      border-radius: 20px;
      max-width: 400px;
      color: white;
      box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
    }
    .login-box h2 {
      text-align: center;
      color: #00f0ff;
      margin-bottom: 30px;
    }
    .input-wrapper {
      position: relative;
      margin-bottom: 20px;
    }
    .input-wrapper i {
      position: absolute;
      top: 50%;
      left: 15px;
      transform: translateY(-50%);
      color: #7efcff;
    }
    .input-wrapper input {
      width: 100%;
      height: 45px;
      padding: 0 15px 0 40px;
      border: 1px solid #00f0ff;
      background: transparent;
      color: white;
      border-radius: 25px;
      font-size: 14px;
      outline: none;
    }
    .login-box button {
      width: 100%;
      height: 48px;
      background: linear-gradient(135deg, #00f0ff, #ff00e0);
      color: white;
      font-weight: bold;
      font-size: 16px;
      border: none;
      border-radius: 25px;
      cursor: pointer;
    }
    /* Debug styles */
    .debug-info {
      position: fixed;
      bottom: 10px;
      right: 10px;
      background: rgba(0,0,0,0.8);
      padding: 10px;
      border-radius: 5px;
      color: #00f0ff;
      font-size: 12px;
      z-index: 1000;
      display: none;
    }
    .debug-info.show {
      display: block;
    }
  </style>
</head>
<body>
  <div id="tsparticles"></div>
  <div class="login-box">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username" id="username" oninput="logInput('username')"/>
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password" id="password" oninput="logInput('password')"/>
    </div>
    <button onclick="handleLogin()">LOGIN</button>
  </div>
  
  <!-- Debug information panel -->
  <div class="debug-info" id="debugInfo">
    <div>Last Action: <span id="lastAction">None</span></div>
    <div>Input Status: <span id="inputStatus">Waiting</span></div>
  </div>

  <script>
    // Debug logging function
    function logToDebug(message) {
      if (window.debugMode) {
        console.log(`[Debug] ${message}`);
        document.getElementById('lastAction').textContent = message;
      }
    }

    // Input logging
    function logInput(field) {
      const input = document.getElementById(field);
      logToDebug(`${field} changed: ${input.value.length} characters`);
      document.getElementById('inputStatus').textContent = `${field} updated`;
    }

    // Login handler with debug info
    function handleLogin() {
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      
      logToDebug(`Login attempt - Username: ${username.length} chars, Password: ${password.length} chars`);
      
      if (!username || !password) {
        alert('Please fill in all fields');
        logToDebug('Login failed: Empty fields');
        return;
      }
      
      alert('Simulated login. Integrate backend for real auth.');
      logToDebug('Login simulation complete');
    }

    // Initialize particles with error handling
    try {
      tsParticles.load("tsparticles", {
        background: { color: "#0f0c29" },
        particles: {
          number: { value: 100 },
          color: { value: ["#00f0ff", "#ff00e0", "#ffc400"] },
          shape: { type: ["circle", "square"] },
          opacity: { value: 0.7 },
          size: { value: 4 },
          move: { enable: true, speed: 1, outModes: "bounce" }
        },
        interactivity: {
          events: {
            onHover: { enable: true, mode: "repulse" },
            onClick: { enable: true, mode: "push" }
          },
          modes: {
            repulse: { distance: 100 },
            push: { quantity: 4 }
          }
        },
        detectRetina: true
      }).then(() => {
        logToDebug('Particles initialized successfully');
      }).catch(error => {
        console.error('Particles initialization error:', error);
        logToDebug('Particles error: ' + error.message);
      });
    } catch (error) {
      console.error('Critical error:', error);
      logToDebug('Critical error: ' + error.message);
    }

    // Show debug panel based on Streamlit's debug mode
    window.debugMode = """ + str(st.session_state.debug_mode).lower() + """;
    if (window.debugMode) {
      document.getElementById('debugInfo').classList.add('show');
    }
  </script>
</body>
</html>
""", height=600, width=800)

# Update login attempts in debug mode
if st.session_state.debug_mode:
    if st.button("Simulate Login Attempt"):
        st.session_state.login_attempts += 1
        st.write(f"Simulated login attempt #{st.session_state.login_attempts}") 
