import streamlit as st
from typing import Optional

# Set page config at the very start
st.set_page_config(
    page_title="Futuristic Login",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple user credentials
USERS = {
    "admin": "admin123",
    "guest": "guest123"
}

def login(username: str, password: str) -> bool:
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
    # Add required resources and base styles
    st.markdown("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
        
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            html, body {
                height: 100vh;
                overflow: hidden;
            }
            
            .stApp {
                background: linear-gradient(45deg, #0f0c29, #302b63, #24243e) !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                right: 0 !important;
                bottom: 0 !important;
                overflow: auto !important;
            }
            
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            
            [data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                max-width: 400px !important;
                margin: 0 auto !important;
                position: relative !important;
                z-index: 2 !important;
            }
            
            /* Animated background */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
                pointer-events: none;
                overflow: hidden;
            }
            
            .particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: #00f0ff;
                border-radius: 50%;
                animation: float 8s infinite linear;
            }
            
            .particle:nth-child(3n) {
                background: #ff00e0;
                animation-duration: 12s;
            }
            
            .particle:nth-child(3n + 1) {
                background: #ffc400;
                animation-duration: 10s;
            }
            
            @keyframes float {
                0% {
                    transform: translate(0, 0) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 1;
                }
                100% {
                    transform: translate(100vw, 100vh) rotate(360deg);
                    opacity: 0;
                }
            }
            
            /* Container styles */
            .container {
                position: relative;
                z-index: 2;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }
            
            /* Login box styles */
            .login-box {
                background: rgba(0, 0, 0, 0.7);
                border-radius: 20px;
                padding: 40px 30px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 240, 255, 0.1);
                position: relative;
                z-index: 2;
            }
            
            .login-box h2 {
                text-align: center;
                color: #00f0ff;
                margin-bottom: 30px;
                font-size: 26px;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }
            
            /* Input field styles */
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
                border: 1px solid #00f0ff !important;
                background: rgba(0, 0, 0, 0.3) !important;
                color: white !important;
                border-radius: 25px !important;
                font-size: 14px !important;
                outline: none !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus-within {
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
                border-color: #00f0ff !important;
                background: rgba(0, 0, 0, 0.5) !important;
            }
            
            .stTextInput input {
                color: white !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            .stTextInput input::placeholder {
                color: rgba(126, 252, 255, 0.7) !important;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            /* Button styles */
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
                transition: all 0.3s ease !important;
                margin: 0 !important;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
                letter-spacing: 2px !important;
                position: relative !important;
                z-index: 2 !important;
            }
            
            .stButton > button:hover {
                transform: scale(1.03) !important;
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
                background: linear-gradient(135deg, #ff00e0, #00f0ff) !important;
            }
            
            /* Options styles */
            .options {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                color: #a0cbe8;
                margin-top: 15px;
                position: relative;
                z-index: 2;
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
                transition: all 0.3s ease;
            }
            
            .options a:hover {
                color: #00f0ff;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }
            
            /* Error message styling */
            [data-testid="stAlert"] {
                background: rgba(255, 0, 224, 0.1) !important;
                border: 1px solid rgba(255, 0, 224, 0.2) !important;
                color: #ff00e0 !important;
                padding: 0.75rem !important;
                border-radius: 12px !important;
                margin: 1rem 0 !important;
                font-family: 'Orbitron', sans-serif !important;
                position: relative !important;
                z-index: 2 !important;
            }
            
            [data-testid="stAlert"] > div {
                padding: 0 !important;
            }
            
            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
            
            /* Mobile responsiveness */
            @media (max-width: 480px) {
                .login-box {
                    padding: 30px 20px;
                }
                
                .stTextInput > div > div {
                    font-size: 13px !important;
                }
                
                .stButton > button {
                    font-size: 15px !important;
                }
                
                .options {
                    font-size: 11px;
                }
            }
        </style>
        
        <div class="particles">
            ${Array(50).fill().map((_, i) => `
                <div class="particle" style="
                    left: ${Math.random() * 100}vw;
                    top: ${Math.random() * 100}vh;
                    animation-delay: -${Math.random() * 8}s;
                "></div>
            `).join('')}
        </div>
        
        <div class="container">
            <div class="login-box">
                <h2>Welcome Back</h2>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
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
            if login(username, password):
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
