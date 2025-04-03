import streamlit as st
from typing import Optional

# Simple user credentials without hashing for now
USERS = {
    "admin": "admin123",
    "guest": "guest123"
}

def login(username: str, password: str) -> bool:
    """Attempt to log in a user"""
    if username in USERS and password == USERS[username]:
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        return True
    return False

def logout():
    """Log out the current user"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state.clear()

def is_authenticated() -> bool:
    """Check if the user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get the current user's username"""
    return st.session_state.get("username")

def show_login_page():
    """Display the login page"""
    st.markdown("""
        <style>
            /* Modern animated background with purple gradient */
            .stApp {
                background: linear-gradient(45deg, #1E1E2E, #2D1E4F, #4A1E6D, #6B1E8F);
                background-size: 300% 300%;
                animation: gradient 15s ease infinite;
                min-height: 100vh;
            }
            
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Wave animation */
            .wave-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                pointer-events: none;
            }
            
            .wave {
                position: absolute;
                width: 150%;
                height: 150%;
                background: linear-gradient(45deg, rgba(66, 99, 235, 0.1), rgba(142, 84, 233, 0.1));
                transform-origin: 50% 48%;
                border-radius: 40%;
                animation: wave 10s infinite linear;
            }
            
            .wave-2 {
                animation: wave 16s infinite linear;
                opacity: 0.5;
            }
            
            .wave-3 {
                animation: wave 20s infinite linear;
                opacity: 0.3;
            }
            
            @keyframes wave {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            /* Enhanced login container with modern glass effect */
            .login-container {
                max-width: 900px;
                margin: 2rem auto;
                padding: 0;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 24px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                overflow: hidden;
                display: flex;
            }
            
            /* Left side - Login form */
            .login-form {
                flex: 1;
                padding: 2.5rem;
                position: relative;
            }
            
            /* Right side - Welcome section */
            .welcome-section {
                flex: 1.2;
                padding: 3rem;
                background: rgba(255, 255, 255, 0.03);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;
                position: relative;
                overflow: hidden;
            }
            
            .welcome-section::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(142, 84, 233, 0.1) 0%,
                    transparent 50%
                );
                animation: rotate 20s linear infinite;
            }
            
            /* Logo style */
            .logo {
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.5em;
                font-weight: 700;
                margin-bottom: 3rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Welcome text */
            .welcome-title {
                color: #fff;
                font-size: 3.5em;
                font-weight: 700;
                margin-bottom: 1rem;
                line-height: 1.2;
                position: relative;
                z-index: 1;
            }
            
            .welcome-subtitle {
                color: rgba(255, 255, 255, 0.7);
                font-size: 1.1em;
                line-height: 1.6;
                position: relative;
                z-index: 1;
            }
            
            /* Modern input fields */
            .stTextInput > div > div {
                background: rgba(255,255,255,0.05) !important;
                border: 2px solid rgba(255,255,255,0.1) !important;
                border-radius: 12px !important;
                padding: 12px 20px !important;
                color: white !important;
                transition: all 0.3s ease !important;
                margin-bottom: 1rem !important;
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus {
                border-color: rgba(142, 84, 233, 0.5) !important;
                background: rgba(255,255,255,0.08) !important;
                transform: translateY(-2px);
            }
            
            .stTextInput > label {
                color: rgba(255,255,255,0.8) !important;
                font-size: 1rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Enhanced button */
            .stButton > button {
                background: linear-gradient(45deg, #8E54E9, #4263EB);
                color: white;
                border: none;
                padding: 0.8rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1rem;
                letter-spacing: 0.5px;
                width: 100%;
                transition: all 0.3s ease;
                margin-top: 1rem;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(142, 84, 233, 0.3);
            }
            
            /* Error message */
            .error-message {
                color: #FF6B6B;
                text-align: center;
                margin-top: 1rem;
                padding: 0.8rem;
                background: rgba(255,107,107,0.1);
                border-radius: 12px;
                border: 1px solid rgba(255,107,107,0.2);
                animation: shake 0.5s ease-in-out;
            }
            
            /* Credentials info */
            .credentials-info {
                color: rgba(255,255,255,0.8);
                text-align: center;
                margin-top: 1.5rem;
                padding: 1.2rem;
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            
            .credentials-info code {
                background: rgba(255,255,255,0.1);
                padding: 0.3rem 0.8rem;
                border-radius: 8px;
                color: #fff;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255,255,255,0.15);
                display: inline-block;
                margin: 0.3rem;
                transition: all 0.3s ease;
            }
            
            .credentials-info code:hover {
                background: rgba(255,255,255,0.15);
                transform: translateY(-2px);
            }
        </style>
        
        <div class="wave-container">
            <div class="wave"></div>
            <div class="wave wave-2"></div>
            <div class="wave wave-3"></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="login-container">
            <div class="login-form">
                <div class="logo">
                    📊 Sales Dashboard
                </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit = st.form_submit_button("Login")

        if submit:
            if login(username, password):
                st.rerun()
            else:
                st.markdown("""
                    <div class="error-message">
                        ⚠️ Invalid username or password
                    </div>
                    <div class="credentials-info">
                        <p><strong>Available Accounts</strong></p>
                        <p>
                            <code>admin</code> / <code>admin123</code>
                            <br>
                            <code>guest</code> / <code>guest123</code>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("""
            </div>
            <div class="welcome-section">
                <h1 class="welcome-title">Welcome.</h1>
                <p class="welcome-subtitle">Access your sales dashboard to track performance, analyze trends, and make data-driven decisions.</p>
            </div>
        </div>
    """, unsafe_allow_html=True) 
