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
    "admin": {
        "password": "admin123",
        "role": "admin"
    }
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
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None

def show_login_page():
    """Show the login page with futuristic design"""
    st.markdown("""
        <style>
            /* Override Streamlit defaults */
            .stApp {
                background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%) !important;
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
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 8px !important;
                color: white !important;
                font-size: 1em !important;
                padding: 12px 15px !important;
            }

            [data-testid="stTextInput"] > div > div > input:focus {
                border-color: #4A90E2 !important;
                box-shadow: 0 0 10px rgba(74, 144, 226, 0.3) !important;
            }

            [data-testid="stButton"] > button {
                width: 100% !important;
                background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 12px !important;
                font-size: 1.1em !important;
                border-radius: 8px !important;
                border: none !important;
                transition: all 0.3s ease !important;
            }

            [data-testid="stButton"] > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4) !important;
            }

            /* Base layout */
            .main {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
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
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* Title */
            .login-box h1 {
                color: white;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2em;
                font-weight: 600;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            }

            /* Error message */
            [data-testid="stAlert"] {
                background-color: rgba(255, 0, 0, 0.1) !important;
                border: 1px solid rgba(255, 0, 0, 0.2) !important;
                color: #ff4444 !important;
                padding: 10px !important;
                border-radius: 5px !important;
                margin-bottom: 20px !important;
                text-align: center !important;
                font-size: 0.9em !important;
            }

            /* Credentials info */
            .credentials-info {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
                font-size: 0.9em;
                color: rgba(255, 255, 255, 0.7);
            }

            /* Particle effect */
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
                position: absolute;
                width: 3px;
                height: 3px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                animation: float 20s infinite linear;
            }

            @keyframes float {
                0% {
                    transform: translateY(100vh) scale(0);
                    opacity: 0;
                }
                50% {
                    opacity: 0.5;
                }
                100% {
                    transform: translateY(-100vh) scale(1);
                    opacity: 0;
                }
            }
        </style>

        <div class="main">
            <div class="particles">
                <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
                <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
                <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
                <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
                <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
                <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
                <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
                <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
                <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
                <div class="particle" style="left: 95%; animation-delay: 18s;"></div>
            </div>
            <div class="container">
                <div class="login-box">
                    <h1>Login</h1>
    """, unsafe_allow_html=True)

    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_button"):
            if authenticate(username, password):
                st.rerun()
            else:
                st.error("Invalid username or password")

        # Show credentials info
        st.markdown("""
            <div class="credentials-info">
                <strong>Demo Credentials:</strong><br>
                Username: admin<br>
                Password: admin123
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True) 
