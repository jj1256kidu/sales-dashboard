import streamlit as st
import streamlit.components.v1 as components
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
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

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
    # Add custom CSS for error messages and Streamlit components
    st.markdown("""
        <style>
            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
            
            /* Style error messages */
            [data-testid="stAlert"] {
                position: fixed !important;
                top: 20px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                z-index: 9999 !important;
                background: rgba(255, 0, 224, 0.1) !important;
                border: 1px solid rgba(255, 0, 224, 0.2) !important;
                color: #ff00e0 !important;
                padding: 0.75rem !important;
                border-radius: 12px !important;
                backdrop-filter: blur(10px) !important;
                box-shadow: 0 0 15px rgba(255, 0, 224, 0.2) !important;
                min-width: 300px !important;
                text-align: center !important;
            }
            
            /* Style form container */
            .stForm {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }
            
            /* Style submit button */
            .stButton > button {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create form for handling submission
    with st.form("login_form", clear_on_submit=True):
        # Hidden inputs to store form data
        username = st.text_input("Username", key="username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", key="password", label_visibility="collapsed")
        submitted = st.form_submit_button("Submit", type="primary")
    
    # HTML template with embedded form handling
    html_code = """
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

    <style>
    body {
        background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
        font-family: 'Orbitron', sans-serif;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }

    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 600px;
    }

    .login-box {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 20px;
        padding: 50px 40px;
        width: 100%;
        max-width: 400px;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.2), 0 0 60px rgba(255, 0, 224, 0.1);
        color: #fff;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 240, 255, 0.1);
    }

    .login-box h2 {
        text-align: center;
        color: #00f0ff;
        font-size: 32px;
        margin-bottom: 30px;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    .input-wrapper {
        position: relative;
        margin-bottom: 25px;
    }

    .input-wrapper i {
        position: absolute;
        top: 50%;
        left: 15px;
        transform: translateY(-50%);
        color: #00f0ff;
        font-size: 14px;
        z-index: 2;
    }

    .input-wrapper input {
        width: 100%;
        height: 45px;
        padding: 0 15px 0 40px;
        border: 1px solid rgba(0, 240, 255, 0.3);
        background: rgba(0, 0, 0, 0.4);
        color: white;
        border-radius: 25px;
        font-size: 15px;
        font-family: 'Orbitron', sans-serif;
        outline: none;
        transition: all 0.3s ease;
        box-shadow: inset 0 0 8px rgba(0, 240, 255, 0.2);
    }

    .input-wrapper input:focus {
        border-color: #00f0ff;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3), 
                   inset 0 0 8px rgba(0, 240, 255, 0.3);
    }

    .input-wrapper input::placeholder {
        color: rgba(160, 203, 232, 0.6);
        font-family: 'Orbitron', sans-serif;
    }

    .login-box button {
        width: 100%;
        height: 48px;
        background: linear-gradient(135deg, #00f0ff, #ff00e0);
        color: white;
        font-weight: bold;
        font-size: 17px;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 1px;
        font-family: 'Orbitron', sans-serif;
        margin-top: 10px;
    }

    .login-box button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        background: linear-gradient(135deg, #ff00e0, #00f0ff);
    }

    .login-box button:active {
        transform: translateY(1px);
    }

    .options {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: rgba(160, 203, 232, 0.8);
        margin-top: 20px;
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
        color: rgba(160, 203, 232, 0.8);
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .options a:hover {
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    </style>

    <div class="login-container">
        <div class="login-box">
            <h2>Welcome Back</h2>
            <form id="loginForm">
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
    </div>

    <script>
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Find the hidden Streamlit form inputs and submit button
        const usernameInput = window.parent.document.querySelector('input[aria-label="Username"]');
        const passwordInput = window.parent.document.querySelector('input[aria-label="Password"]');
        const submitButton = window.parent.document.querySelector('button[type="submit"]');
        
        if (usernameInput && passwordInput && submitButton) {
            usernameInput.value = username;
            passwordInput.value = password;
            submitButton.click();
        }
    });
    </script>
    """
    
    # Render the HTML
    components.html(html_code, height=650, scrolling=False)
    
    # Handle form submission
    if submitted:
        if not username or not password:
            st.error("Please enter both username and password")
        elif login(username, password):
            st.rerun()
        else:
            st.error("Invalid username or password") 
