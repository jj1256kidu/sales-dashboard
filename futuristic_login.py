import streamlit as st
import streamlit.components.v1 as components
import hashlib
import sqlite3
import time
from datetime import datetime

# Initialize DB
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 username TEXT PRIMARY KEY,
                 password TEXT,
                 created_date TEXT,
                 last_login TEXT)''')
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify user
def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == hash_password(password)

# Update last login
def update_last_login(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET last_login=? WHERE username=?", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
    conn.commit()
    conn.close()

# Create user
def create_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, created_date) VALUES (?, ?, ?)",
                 (username, hash_password(password), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Handle login attempts
def handle_login(username, password):
    if st.session_state.login_attempts >= 3:
        if time.time() - st.session_state.last_attempt < 300:
            return "Too many failed attempts. Try again in 5 minutes."
        st.session_state.login_attempts = 0

    if verify_user(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_attempts = 0
        update_last_login(username)
        return "success"
    else:
        st.session_state.login_attempts += 1
        st.session_state.last_attempt = time.time()
        return "Invalid username or password"

# Initialize
init_db()
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "last_attempt" not in st.session_state:
    st.session_state.last_attempt = None

# Streamlit page config
st.set_page_config(page_title="Futuristic Login", layout="centered")

# Inject particles background with exact HTML/CSS/JS
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
    }

    .login-box h2 {
      text-align: center;
      color: #00f0ff;
      margin-bottom: 30px;
      font-size: 26px;
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
      transition: box-shadow 0.3s;
    }

    .input-wrapper input:focus {
      box-shadow: 0 0 10px #00f0ff;
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
    }

    .login-box button:hover {
      transform: scale(1.03);
      box-shadow: 0 0 15px #00f0ff;
    }

    .options {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #a0cbe8;
      margin-top: 10px;
    }

    .options a {
      color: #a0cbe8;
      text-decoration: underline;
    }
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
      <input type="text" id="username" placeholder="Username" required />
    </div>
    <div class="input-wrapper">
      <i class="fas fa-lock"></i>
      <input type="password" id="password" placeholder="Password" required />
    </div>
    <button type="submit">LOGIN</button>
    <div class="options">
      <label><input type="checkbox" checked /> Remember me</label>
      <a href="#">Forgot password?</a>
    </div>
  </form>
</div>

<!-- tsparticles config -->
<script>
  tsParticles.load("tsparticles", {
    fullScreen: { enable: false },
    background: { color: "#0f0c29" },
    particles: {
      number: { value: 100 },
      color: { value: ["#00f0ff", "#ff00e0", "#ffc400"] },
      shape: { type: ["circle", "square"] },
      opacity: { value: 0.7 },
      size: { value: 4 },
      move: {
        enable: true,
        speed: 1,
        direction: "none",
        random: false,
        straight: false,
        outModes: "bounce"
      }
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
  });

  // Handle form submission
  document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Send data to Streamlit
    window.parent.postMessage({
      type: 'streamlit:setComponentValue',
      value: {
        username: username,
        password: password
      }
    }, '*');
  });
</script>

</body>
</html>
""", height=800, scrolling=False)

# Hide Streamlit elements
st.markdown("""
<style>
    .block-container {
        padding-top: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.empty()  # Prevent default Streamlit layout from interfering

# Handle login
if st.session_state.authenticated:
    st.success(f"🎉 Welcome back, {st.session_state.username}!")
    if st.button("Logout", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
else:
    # Get form data from JavaScript
    form_data = st.session_state.get('form_data', {})
    if form_data:
        username = form_data.get('username', '')
        password = form_data.get('password', '')
        
        result = handle_login(username, password)
        if result == "success":
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error(result)

# Optional: Create default user for testing
if not verify_user("demo", "password123"):
    create_user("demo", "password123")
