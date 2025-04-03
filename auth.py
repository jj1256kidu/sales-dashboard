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
            /* Vibrant animated background with particles effect */
            .stApp {
                background: linear-gradient(-45deg, #FF512F, #DD2476, #4158D0, #23D5AB);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                position: relative;
                overflow: hidden;
            }
            
            .stApp::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 25% 25%, rgba(255,255,255,0.2) 1px, transparent 1px),
                    radial-gradient(circle at 75% 75%, rgba(255,255,255,0.2) 1px, transparent 1px);
                background-size: 100px 100px;
                animation: sparkle 4s linear infinite;
            }
            
            @keyframes sparkle {
                0% { transform: translateY(0); }
                100% { transform: translateY(-100px); }
            }
            
            @keyframes gradient {
                0% {
                    background-position: 0% 50%;
                }
                50% {
                    background-position: 100% 50%;
                }
                100% {
                    background-position: 0% 50%;
                }
            }
            
            /* Enhanced floating login container with 3D effect */
            .login-container {
                max-width: 450px;
                margin: 2rem auto;
                padding: 3rem;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                box-shadow: 
                    0 8px 32px 0 rgba(31, 38, 135, 0.37),
                    0 0 0 1px rgba(255, 255, 255, 0.1),
                    inset 0 0 32px 0 rgba(31, 38, 135, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.18);
                transform-style: preserve-3d;
                animation: float 6s ease-in-out infinite, rotate 20s linear infinite;
            }
            
            @keyframes float {
                0%, 100% {
                    transform: translateY(0) rotateX(0) rotateY(0);
                }
                25% {
                    transform: translateY(-20px) rotateX(5deg) rotateY(5deg);
                }
                50% {
                    transform: translateY(0) rotateX(0) rotateY(0);
                }
                75% {
                    transform: translateY(20px) rotateX(-5deg) rotateY(-5deg);
                }
            }
            
            @keyframes rotate {
                0% { transform: rotate3d(1, 1, 1, 0deg); }
                100% { transform: rotate3d(1, 1, 1, 360deg); }
            }
            
            /* Enhanced glowing title with neon effect */
            .login-title {
                color: #fff;
                text-align: center;
                font-size: 3em;
                margin-bottom: 2rem;
                text-transform: uppercase;
                letter-spacing: 4px;
                animation: neon 3s infinite alternate;
            }
            
            @keyframes neon {
                from {
                    text-shadow: 
                        0 0 10px #fff,
                        0 0 20px #fff,
                        0 0 30px #FF512F,
                        0 0 40px #DD2476,
                        0 0 50px #4158D0,
                        0 0 60px #23D5AB;
                }
                to {
                    text-shadow: 
                        0 0 5px #fff,
                        0 0 10px #fff,
                        0 0 15px #FF512F,
                        0 0 20px #DD2476,
                        0 0 25px #4158D0,
                        0 0 30px #23D5AB;
                }
            }
            
            /* Animated input fields with glow effect */
            .stTextInput > div > div {
                background: rgba(255,255,255,0.05) !important;
                border: 2px solid rgba(255,255,255,0.1) !important;
                border-radius: 15px !important;
                padding: 12px 20px !important;
                color: white !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 0 10px rgba(255,255,255,0.1);
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus {
                border-color: rgba(255,255,255,0.5) !important;
                background: rgba(255,255,255,0.15) !important;
                transform: translateY(-5px) scale(1.02);
                box-shadow: 
                    0 10px 20px rgba(0,0,0,0.2),
                    0 0 20px rgba(255,255,255,0.2);
            }
            
            .stTextInput > label {
                color: rgba(255,255,255,0.9) !important;
                font-size: 1.2em !important;
                font-weight: 500 !important;
                text-shadow: 0 0 10px rgba(255,255,255,0.3);
                transform: translateY(-5px);
            }
            
            /* Enhanced login button with gradient animation */
            .stButton > button {
                background: linear-gradient(90deg, #FF512F, #DD2476, #4158D0, #23D5AB, #FF512F);
                background-size: 400% 400%;
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 15px;
                font-weight: 600;
                font-size: 1.1em;
                letter-spacing: 2px;
                text-transform: uppercase;
                width: 100%;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                animation: gradient-shift 8s linear infinite;
                box-shadow: 
                    0 4px 15px rgba(0,0,0,0.2),
                    0 0 20px rgba(255,255,255,0.1);
            }
            
            @keyframes gradient-shift {
                0% { background-position: 0% 50%; }
                100% { background-position: 400% 50%; }
            }
            
            .stButton > button:hover {
                transform: translateY(-5px) scale(1.05);
                box-shadow: 
                    0 8px 25px rgba(0,0,0,0.3),
                    0 0 30px rgba(255,255,255,0.2);
                letter-spacing: 4px;
            }
            
            .stButton > button:active {
                transform: translateY(-2px) scale(1.02);
            }
            
            /* Enhanced error message with ripple effect */
            .error-message {
                color: #FF512F;
                text-align: center;
                margin-top: 1.5rem;
                padding: 1rem;
                background: rgba(255,99,99,0.1);
                border-radius: 15px;
                border: 1px solid rgba(255,99,99,0.2);
                animation: ripple 0.5s ease-out;
                box-shadow: 0 0 20px rgba(255,99,99,0.2);
            }
            
            @keyframes ripple {
                0% {
                    transform: scale(0.8);
                    opacity: 0;
                }
                50% {
                    transform: scale(1.1);
                    opacity: 0.5;
                }
                100% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            /* Enhanced credentials info with floating effect */
            .credentials-info {
                color: white;
                text-align: center;
                margin-top: 2rem;
                padding: 1.5rem;
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.2);
                animation: float-subtle 4s ease-in-out infinite;
                box-shadow: 
                    0 8px 32px rgba(31, 38, 135, 0.2),
                    0 0 20px rgba(255,255,255,0.1);
            }
            
            @keyframes float-subtle {
                0%, 100% { transform: translateY(0) rotate(0); }
                50% { transform: translateY(-10px) rotate(1deg); }
            }
            
            .credentials-info code {
                background: rgba(255,255,255,0.15);
                padding: 0.4rem 1rem;
                border-radius: 10px;
                color: #fff;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255,255,255,0.3);
                transition: all 0.3s ease;
                display: inline-block;
                margin: 0.3rem;
                box-shadow: 0 0 15px rgba(255,255,255,0.1);
            }
            
            .credentials-info code:hover {
                background: rgba(255,255,255,0.25);
                transform: translateY(-3px) scale(1.1);
                box-shadow: 
                    0 5px 15px rgba(0,0,0,0.2),
                    0 0 20px rgba(255,255,255,0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">Sales Dashboard</h1>', unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
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
                            <br><br>
                            <code>guest</code> / <code>guest123</code>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) 
