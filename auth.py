import streamlit as st
import pandas as pd
import hashlib
from typing import Optional, Dict, Any
import json
import os
import random
import time

def init_session_state():
    """Initialize session state variables"""
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'last_attempt' not in st.session_state:
        st.session_state.last_attempt = 0
    if 'locked_until' not in st.session_state:
        st.session_state.locked_until = 0

def check_password():
    """Check if the password is correct"""
    # Check if account is locked
    if st.session_state.locked_until > time.time():
        remaining_time = int(st.session_state.locked_until - time.time())
        st.error(f"Account locked. Please try again in {remaining_time} seconds.")
        return False

    # Get username and password from session state
    username = st.session_state.get('login_username', '')
    password = st.session_state.get('login_password', '')

    # Check if both username and password are provided
    if not username or not password:
        st.error("Please enter both username and password")
        return False

    # Check credentials (for demo purposes, using admin/admin123)
    if username == "admin" and password == "admin123":
        st.session_state.is_logged_in = True
        st.session_state.authenticated = True
        st.session_state.login_attempts = 0
        st.session_state.last_attempt = 0
        st.session_state.locked_until = 0
        return True
    else:
        # Increment login attempts
        st.session_state.login_attempts += 1
        st.session_state.last_attempt = time.time()
        
        # Check if account should be locked
        if st.session_state.login_attempts >= 3:
            st.session_state.locked_until = time.time() + 300  # Lock for 5 minutes
            st.error("Too many failed attempts. Account locked for 5 minutes.")
        else:
            st.error("Invalid username or password")
        
        return False

# Load users from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin user if file doesn't exist
        default_users = {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "role": "admin"
            }
        }
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

def verify_password(username, password):
    users = load_users()
    if username in users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == users[username]["password"]
    return False

def show_login_page():
    """Display the login page with username and password fields"""
    # Hide sidebar and main menu
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Override Streamlit defaults */
            .stApp {
                background: #0B0B1E !important;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            /* Custom styles for form elements */
            [data-testid="stTextInput"] > div > div > input {
                background-color: rgba(0, 0, 0, 0.5) !important;
                border: 2px solid #00F5FF !important;
                border-radius: 25px !important;
                color: #00F5FF !important;
                font-size: 1em !important;
                padding: 12px 25px !important;
                font-family: 'Orbitron', sans-serif !important;
                box-shadow: 0 0 10px rgba(0, 245, 255, 0.3) !important;
                margin-bottom: 15px !important;
                width: 100% !important;
            }

            [data-testid="stTextInput"] > div > div > input:focus {
                border-color: #00F5FF !important;
                box-shadow: 0 0 20px rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stTextInput"] > div > div > input::placeholder {
                color: rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stButton"] > button {
                width: 100% !important;
                background: linear-gradient(90deg, #00F5FF, #FF00FF) !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 12px !important;
                font-size: 1.1em !important;
                border-radius: 25px !important;
                border: none !important;
                transition: all 0.3s ease !important;
                font-family: 'Orbitron', sans-serif !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
                margin-top: 20px !important;
            }

            [data-testid="stButton"] > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 30px rgba(0, 245, 255, 0.5) !important;
            }

            /* Base layout */
            .main {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                font-family: 'Orbitron', sans-serif;
            }

            /* Container and login box */
            .container {
                width: 100%;
                max-width: 400px;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }

            .login-box {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 0 50px rgba(0, 245, 255, 0.3);
                border: 2px solid #00F5FF;
            }

            /* Title and subtitle */
            .login-box h1 {
                color: #00F5FF;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
                font-family: 'Orbitron', sans-serif;
            }

            .login-box p {
                color: rgba(0, 245, 255, 0.7);
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.1em;
            }

            /* Form elements */
            .form-group {
                margin-bottom: 20px;
            }

            .form-group label {
                display: block;
                color: #00F5FF;
                margin-bottom: 8px;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            /* Remember me and Forgot password */
            .options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
                color: #00F5FF;
                font-size: 0.9em;
            }

            .remember-me {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .remember-me input[type="checkbox"] {
                accent-color: #00F5FF;
            }

            .forgot-password {
                color: #00F5FF;
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .forgot-password:hover {
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
            }

            /* Particles */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                pointer-events: none;
            }

            .particle {
                position: fixed;
                width: 5px;
                height: 5px;
                border-radius: 50%;
                animation: particle-animation 20s infinite linear;
            }

            @keyframes particle-animation {
                0% {
                    transform: translateY(100vh) translateX(0) scale(0);
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100vh) translateX(100px) scale(1);
                    opacity: 0;
                }
            }

            /* Generate multiple particles with different colors */
            .particle:nth-child(3n) { background: #00F5FF; }
            .particle:nth-child(3n+1) { background: #FF00FF; }
            .particle:nth-child(3n+2) { background: #FFD700; }
        </style>
    """, unsafe_allow_html=True)

    # Generate particles HTML
    particles_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.randint(0, 20)
        duration = random.randint(15, 25)
        particles_html += f'<div class="particle" style="left: {left}vw; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'

    # Create the main container with particles
    st.markdown(f"""
        <div class="main">
            <div class="particles">
                {particles_html}
            </div>
            <div class="container">
                <div class="login-box">
                    <h1>Welcome Back</h1>
                    <p>Please sign in to continue</p>
                    <div id="login-form">
    """, unsafe_allow_html=True)

    # Add custom font
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Create columns for centering the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Username input
        st.markdown('<div class="form-group"><label>Username</label></div>', unsafe_allow_html=True)
        username = st.text_input("", value="", placeholder="Enter your username", key="login_username", label_visibility="collapsed")

        # Password input
        st.markdown('<div class="form-group"><label>Password</label></div>', unsafe_allow_html=True)
        password = st.text_input("", value="", placeholder="Enter your password", type="password", key="login_password", label_visibility="collapsed")

        if st.button("SIGN IN", key="login_button"):
            if check_password():
                st.rerun()

        # Remember me and Forgot password
        st.markdown("""
            <div class="options">
                <label class="remember-me">
                    <input type="checkbox" checked>
                    Remember me
                </label>
                <a href="#" class="forgot-password">Forgot password?</a>
            </div>
        """, unsafe_allow_html=True)

    # Close the containers
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def is_authenticated():
    return st.session_state.get("authenticated", False)

def get_current_user():
    return st.session_state.get("username") if is_authenticated() else None

def logout():
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Reinitialize authentication state
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username: str, password: str) -> bool:
    """Authenticate a user"""
    if username in USERS and USERS[username] == password:  # Simplified check
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

# Hardcoded users (in a real app, this would be in a database)
USERS = {
    "admin": "admin123"  # Simplified user structure
} 
