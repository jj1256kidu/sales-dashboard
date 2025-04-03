import streamlit as st
import streamlit.components.v1 as components
import time
import re

st.set_page_config(page_title="Futuristic Login", layout="centered")

# Initialize session state for login attempts
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
    st.session_state.last_attempt = None
    st.session_state.is_locked = False

# Inject particles background with enhanced effects
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Orbitron', sans-serif;
    }

    html, body {
      height: 100%;
      overflow: hidden;
      background: #0f0c29;
    }

    #tsparticles {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: 0;
    }

    .container {
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      padding: 20px;
    }

    .login-box {
      background: rgba(0, 0, 0, 0.7);
      border-radius: 20px;
      padding: 40px 30px;
      width: 100%;
      max-width: 400px;
      box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
      animation: glow 3s infinite alternate;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(0, 240, 255, 0.1);
    }

    @keyframes glow {
      0% {
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
      }
      100% {
        box-shadow: 0 0 35px rgba(0, 255, 255, 0.4);
      }
    }

    .login-box h2 {
      text-align: center;
      color: #00f0ff;
      margin-bottom: 30px;
      font-size: 26px;
      text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
      animation: textGlow 2s infinite alternate;
    }

    @keyframes textGlow {
      from { text-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }
      to { text-shadow: 0 0 20px rgba(0, 240, 255, 0.8); }
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
      font-size: 14px;
      transition: all 0.3s ease;
    }

    .input-wrapper input:focus + i {
      color: #00f0ff;
      text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    .input-wrapper input {
      width: 100%;
      height: 45px;
      padding: 0 15px 0 40px;
      border: 1px solid #00f0ff;
      background: rgba(0, 0, 0, 0.3);
      color: white;
      border-radius: 25px;
      font-size: 14px;
      outline: none;
      transition: all 0.3s ease;
    }

    .input-wrapper input:focus {
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
      border-color: #00f0ff;
      background: rgba(0, 0, 0, 0.5);
    }

    .input-wrapper input::placeholder {
      color: rgba(255, 255, 255, 0.5);
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
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }

    .login-box button:before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        120deg,
        transparent,
        rgba(255, 255, 255, 0.2),
        transparent
      );
      transition: 0.5s;
    }

    .login-box button:hover:before {
      left: 100%;
    }

    .login-box button:hover {
      transform: scale(1.03);
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }

    .options {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #a0cbe8;
      margin-top: 15px;
      align-items: center;
    }

    .options label {
      display: flex;
      align-items: center;
      gap: 5px;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .options label:hover {
      color: #00f0ff;
    }

    .options input[type="checkbox"] {
      accent-color: #00f0ff;
      width: 14px;
      height: 14px;
    }

    .options a {
      color: #a0cbe8;
      text-decoration: none;
      transition: all 0.3s ease;
    }

    .options a:hover {
      color: #00f0ff;
      text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    .error-message {
      color: #ff4444;
      font-size: 12px;
      margin-top: 5px;
      text-align: center;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .error-message.show {
      opacity: 1;
    }

    .password-strength {
      height: 3px;
      background: #333;
      margin-top: 5px;
      border-radius: 2px;
      transition: all 0.3s ease;
    }

    .strength-weak { background: #ff4444; }
    .strength-medium { background: #ffaa00; }
    .strength-strong { background: #00ff00; }

  </style>
</head>
<body>

<!-- Particle Background -->
<div id="tsparticles"></div>

<!-- Login Form -->
<div class="container">
  <form class="login-box" id="loginForm">
    <h2>Welcome Back</h2>
    <div class="input-wrapper">
      <i class="fas fa-user"></i>
      <input type="text" placeholder="Username" required id="username" />
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" placeholder="Password" required id="password" />
      <div class="password-strength"></div>
    </div>
    <div class="error-message" id="errorMsg"></div>
    <button type="submit">LOGIN</button>
    <div class="options">
      <label><input type="checkbox" checked /> Remember me</label>
      <a href="#">Forgot password?</a>
    </div>
  </form>
</div>

<!-- Enhanced tsparticles config -->
<script>
  tsParticles.load("tsparticles", {
    fullScreen: { enable: false },
    background: { color: "#0f0c29" },
    particles: {
      number: { value: 100 },
      color: { 
        value: ["#00f0ff", "#ff00e0", "#ffc400"],
        animation: {
          enable: true,
          speed: 20,
          sync: false
        }
      },
      shape: { 
        type: ["circle", "square", "triangle"],
        options: {
          triangle: {
            sides: 3
          }
        }
      },
      opacity: { 
        value: 0.7,
        random: true,
        animation: {
          enable: true,
          speed: 1,
          minimumValue: 0.4,
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
        speed: 1.5,
        direction: "none",
        random: true,
        straight: false,
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
        width: 1,
        triangles: {
          enable: true,
          opacity: 0.05
        }
      },
      rotate: {
        value: 0,
        random: true,
        direction: "clockwise",
        animation: {
          enable: true,
          speed: 5,
          sync: false
        }
      }
    },
    interactivity: {
      events: {
        onHover: { 
          enable: true, 
          mode: ["grab", "bubble"],
          parallax: {
            enable: true,
            smooth: 10,
            force: 60
          }
        },
        onClick: { 
          enable: true, 
          mode: "push" 
        }
      },
      modes: {
        grab: {
          distance: 140,
          links: { opacity: 0.5 }
        },
        bubble: {
          distance: 200,
          size: 6,
          duration: 2,
          opacity: 0.8,
          speed: 3
        },
        push: { quantity: 6 }
      }
    },
    detectRetina: true
  });

  // Form validation and animations
  document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const errorMsg = document.getElementById('errorMsg');
    const strengthBar = document.querySelector('.password-strength');

    function showError(message) {
      errorMsg.textContent = message;
      errorMsg.classList.add('show');
      setTimeout(() => errorMsg.classList.remove('show'), 3000);
    }

    function validatePassword(pass) {
      const hasUpperCase = /[A-Z]/.test(pass);
      const hasLowerCase = /[a-z]/.test(pass);
      const hasNumbers = /\d/.test(pass);
      const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(pass);
      const isLongEnough = pass.length >= 8;

      const strength = [hasUpperCase, hasLowerCase, hasNumbers, hasSpecial, isLongEnough]
        .filter(Boolean).length;

      strengthBar.className = 'password-strength';
      if (strength < 2) strengthBar.classList.add('strength-weak');
      else if (strength < 4) strengthBar.classList.add('strength-medium');
      else strengthBar.classList.add('strength-strong');
    }

    password.addEventListener('input', (e) => validatePassword(e.target.value));

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      if (username.value.length < 3) {
        showError('Username must be at least 3 characters long');
        return;
      }

      if (password.value.length < 8) {
        showError('Password must be at least 8 characters long');
        return;
      }

      // Simulate login - replace with actual login logic
      showError('Login successful!');
      errorMsg.style.color = '#00ff00';
    });
  });
</script>

</body>
</html>
""", height=800, scrolling=False)

st.markdown("""
<style>
    .block-container {
        padding-top: 0 !important;
    }
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Handle form submission in Streamlit
if st.session_state.is_locked:
    remaining_time = 30 - (time.time() - st.session_state.last_attempt)
    if remaining_time <= 0:
        st.session_state.is_locked = False
        st.session_state.login_attempts = 0
    else:
        st.error(f"Too many login attempts. Please wait {int(remaining_time)} seconds.")

st.empty()  # Prevent default Streamlit layout from interfering 
