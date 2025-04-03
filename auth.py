import streamlit as st
import hashlib
from typing import Optional, Dict, Any
import json
import os

# Set page config
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Hardcoded users (in a real app, this would be in a database)
USERS = {
    "admin": "admin123"  # Simplified user structure
}

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def is_authenticated() -> bool:
    """Check if the user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get the current authenticated user"""
    return st.session_state.get("username")

def authenticate(username: str, password: str) -> bool:
    """Authenticate a user"""
    if username in USERS and USERS[username] == password:  # Simplified check
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None

def show_login_page():
    """Show the login page with cyberpunk design"""
    st.markdown("""
        <style>
            /* Override Streamlit defaults */
            .stApp {
                background: #0B0B1E !important;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            section[data-testid="stSidebar"] {
                display: none !important;
            }

            header[data-testid="stHeader"] {
                display: none !important;
            }

            #MainMenu {
                display: none !important;
            }

            footer {
                display: none !important;
            }

            /* Custom styles for form elements */
            [data-testid="stTextInput"] > div > div > input {
                background-color: #000 !important;
                border: 2px solid #00F5FF !important;
                border-radius: 25px !important;
                color: #00F5FF !important;
                font-size: 1em !important;
                padding: 12px 25px !important;
                font-family: 'Orbitron', sans-serif !important;
                box-shadow: 0 0 10px rgba(0, 245, 255, 0.3) !important;
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

            /* Title */
            .login-box h1 {
                color: #00F5FF;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
                font-family: 'Orbitron', sans-serif;
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

        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap" rel="stylesheet">

        <div class="main">
            <div class="particles">
                ${Array(30).fill().map((_, i) => `
                    <div class="particle" style="
                        left: ${Math.random() * 100}vw;
                        animation-delay: ${Math.random() * 20}s;
                        animation-duration: ${15 + Math.random() * 10}s;
                    "></div>
                `).join('')}
            </div>
            <div class="container">
                <div class="login-box">
                    <h1>Welcome Back</h1>
    """, unsafe_allow_html=True)

    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("", placeholder="Username", key="login_username")
        password = st.text_input("", placeholder="Password", type="password", key="login_password")

        if st.button("LOGIN", key="login_button"):
            if authenticate(username, password):
                st.rerun()
            else:
                st.error("Invalid username or password")

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

    st.markdown("""
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True) 
