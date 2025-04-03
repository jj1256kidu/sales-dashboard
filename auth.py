import streamlit as st
from typing import Optional
import random
import time

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "last_attempt_time" not in st.session_state:
    st.session_state.last_attempt_time = 0

# Simple user credentials
USERS = {
    "admin": "admin123",
    "guest": "guest123"
}

def login(username: str, password: str) -> bool:
    """Authenticate user and set session state"""
    current_time = time.time()
    
    # Check for brute force protection
    if st.session_state.login_attempts >= 3:
        if current_time - st.session_state.last_attempt_time < 30:  # 30 second cooldown
            st.error("Too many failed attempts. Please wait 30 seconds.")
            return False
        else:
            st.session_state.login_attempts = 0
    
    if username in USERS and password == USERS[username]:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_attempts = 0
        return True
    
    st.session_state.login_attempts += 1
    st.session_state.last_attempt_time = current_time
    return False

def logout():
    """Log out the current user and clear session state"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.clear()
    st.rerun()

def is_authenticated() -> bool:
    """Check if the user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get the current user's username"""
    return st.session_state.get("username")

def show_login_page():
    # Add base styles first
    st.markdown("""
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            .stApp {
                background: linear-gradient(45deg, #0f0c29, #302b63, #24243e) !important;
            }
            
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            
            .block-container {
                max-width: 100% !important;
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }
            
            [data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                max-width: 400px !important;
                margin: 0 auto !important;
            }
            
            /* Main container */
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                position: relative;
                z-index: 2;
            }
            
            /* Login box */
            .login-box {
                background: rgba(0, 0, 0, 0.7);
                border-radius: 20px;
                padding: 40px 30px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 240, 255, 0.1);
            }
            
            .login-box h2 {
                text-align: center;
                color: #00f0ff;
                margin-bottom: 30px;
                font-size: 26px;
                font-weight: 700;
                font-family: 'Orbitron', sans-serif;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }
            
            /* Input styling */
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
                z-index: 3;
            }
            
            .stTextInput > div {
                margin: 0 !important;
            }
            
            .stTextInput > div > div {
                width: 100% !important;
                height: 45px !important;
                padding: 0 15px 0 40px !important;
                border: 1px solid rgba(0, 240, 255, 0.3) !important;
                background: rgba(0, 0, 0, 0.3) !important;
                color: white !important;
                border-radius: 25px !important;
                font-size: 14px !important;
            }
            
            .stTextInput input {
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            .stTextInput input::placeholder {
                color: rgba(126, 252, 255, 0.7) !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            /* Button styling */
            .stButton > button {
                width: 100% !important;
                height: 48px !important;
                background: linear-gradient(135deg, #00f0ff, #ff00e0) !important;
                color: white !important;
                font-weight: bold !important;
                font-size: 16px !important;
                border: none !important;
                border-radius: 25px !important;
                cursor: pointer !important;
                margin-top: 10px !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            /* Options styling */
            .options {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                color: #a0cbe8;
                margin-top: 15px;
            }
            
            .options label {
                display: flex;
                align-items: center;
                gap: 5px;
                cursor: pointer;
            }
            
            .options input[type="checkbox"] {
                cursor: pointer;
                accent-color: #00f0ff;
            }
            
            .options a {
                color: #a0cbe8;
                text-decoration: none;
            }
            
            /* Error message */
            [data-testid="stAlert"] {
                background: rgba(255, 0, 224, 0.1) !important;
                border: 1px solid rgba(255, 0, 224, 0.2) !important;
                color: #ff00e0 !important;
                padding: 0.75rem !important;
                border-radius: 12px !important;
                margin: 1rem 0 !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add required external resources
    st.markdown("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown("""
        <div class="login-container">
            <div class="login-box">
                <h2>Welcome Back</h2>
    """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form", clear_on_submit=True):
        st.markdown('<div class="input-wrapper"><i class="fas fa-user"></i>', unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            placeholder="Username",
            key="username",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-wrapper"><i class="fas fa-lock"></i>', unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Password",
            key="password",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        submit = st.form_submit_button("LOGIN")
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            elif login(username, password):
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.markdown("""
            <div class="options">
                <label><input type="checkbox" checked /> Remember me</label>
                <a href="#">Forgot password?</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True) 
