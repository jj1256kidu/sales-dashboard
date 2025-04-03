import streamlit as st
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
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
        background-color: #0f0c29;
    }
    .stTextInput>div>div>input, .stTextInput>div>div>div>input {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
        border: 1px solid #00f0ff;
        border-radius: 30px;
        padding-left: 40px;
    }
    .stTextInput>div:before {
        content: '';
        position: absolute;
        left: 16px;
        top: 12px;
        width: 16px;
        height: 16px;
        background-size: contain;
    }
    button[kind="primary"] {
        background: linear-gradient(to right, #00f0ff, #ff00e0);
        border-radius: 25px;
        color: white;
        font-weight: bold;
    }
    .stCheckbox>div>label {
        color: #00f0ff !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 10px #00f0ff;
    }
    .block-container {
        padding-top: 5rem;
    }
    .stFormSubmitButton>button {
        width: 100%;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Add particle background
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<div id="tsparticles" style="position:fixed; width:100%; height:100%; z-index:0;"></div>
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
        move: { enable: true, speed: 1, direction: "none", outModes: "bounce" }
    },
    interactivity: {
        events: {
            onHover: { enable: true, mode: "repulse" },
            onClick: { enable: true, mode: "push" }
        },
        modes: { repulse: { distance: 100 }, push: { quantity: 4 } }
    },
    detectRetina: true
});
</script>
""", unsafe_allow_html=True)

# Login logic
if st.session_state.authenticated:
    st.success(f"🎉 Welcome back, {st.session_state.username}!")
    if st.button("Logout", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
else:
    with st.form("login_form", clear_on_submit=True):
        st.markdown("<h2 style='text-align: center; color: #00f0ff;'>Welcome Back</h2>", unsafe_allow_html=True)
        
        username = st.text_input(
            label="Username",
            placeholder="Enter your username",
            key="username_input",
            label_visibility="collapsed"
        )
        password = st.text_input(
            label="Password",
            type="password",
            placeholder="Enter your password",
            key="password_input",
            label_visibility="collapsed"
        )

        col1, col2 = st.columns(2)
        with col1:
            remember = st.checkbox("Remember me", value=True, key="remember_checkbox")
        with col2:
            st.markdown('<div style="text-align: right;"><a href="#" style="color: #a0cbe8;">Forgot password?</a></div>', unsafe_allow_html=True)
        
        login = st.form_submit_button("LOGIN", use_container_width=True)
        if login:
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
