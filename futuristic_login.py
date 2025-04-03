import streamlit as st
import streamlit.components.v1 as components
import hashlib
import sqlite3
import time
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT, 
                  created_date TEXT,
                  last_login TEXT)''')
    conn.commit()
    conn.close()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'last_attempt' not in st.session_state:
    st.session_state.last_attempt = None

# Initialize database
init_db()

st.set_page_config(
    page_title="Futuristic Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def update_last_login(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET last_login=? WHERE username=?", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect('users.db')
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

# Handle login submission
def handle_login(username, password):
    if st.session_state.login_attempts >= 3:
        if time.time() - st.session_state.last_attempt < 300:  # 5 minutes lockout
            return "Too many failed attempts. Please try again later."
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

# Hide Streamlit elements
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

# Handle the authenticated state
if st.session_state.authenticated:
    st.success(f"Welcome back, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
else:
    # Create a form with proper labels
    with st.form("login_form"):
        st.markdown("""
            <h2 style="text-align: center; color: #00f0ff; margin-bottom: 30px; font-family: 'Orbitron', sans-serif;">
                Welcome Back
            </h2>
        """, unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="username_input"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="password_input"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember = st.checkbox("Remember me", value=True)
        with col2:
            st.markdown(
                '<div style="text-align: right;"><a href="#" style="color: #a0cbe8;">Forgot password?</a></div>',
                unsafe_allow_html=True
            )
        
        submit = st.form_submit_button(
            "LOGIN",
            use_container_width=True,
            type="primary"
        )
        
        if submit:
            result = handle_login(username, password)
            if result == "success":
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(result)

# For demonstration, let's create a test user
if not verify_user("demo", "password123"):
    create_user("demo", "password123")

# Add the particle effect
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<div id="tsparticles"></div>
<script>
tsParticles.load("tsparticles", {
    fullScreen: { enable: true, zIndex: -1 },
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
</script>
""", unsafe_allow_html=True)
