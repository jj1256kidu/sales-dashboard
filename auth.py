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
            /* Modern animated background with mesh gradient */
            .stApp {
                background: linear-gradient(-45deg, #0A2647, #144272, #205295, #2C74B3);
                background-size: 300% 300%;
                animation: gradient 15s ease infinite;
                position: relative;
            }
            
            .stApp::before {
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                background: repeating-linear-gradient(
                    45deg,
                    rgba(255,255,255,0.05) 0px,
                    rgba(255,255,255,0.05) 1px,
                    transparent 1px,
                    transparent 10px
                );
                pointer-events: none;
            }
            
            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Enhanced login container with modern glass effect */
            .login-container {
                max-width: 450px;
                margin: 2rem auto;
                padding: 2.5rem;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1),
                    inset 0 0 64px rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.18);
                animation: float 4s ease-in-out infinite;
                position: relative;
                overflow: hidden;
            }
            
            .login-container::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(255,255,255,0.1) 0%,
                    transparent 50%
                );
                animation: rotate 15s linear infinite;
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            /* Enhanced title with modern glow */
            .login-title {
                color: #fff;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 2rem;
                text-transform: uppercase;
                letter-spacing: 3px;
                position: relative;
                text-shadow: 
                    0 0 10px rgba(255,255,255,0.5),
                    0 0 20px rgba(255,255,255,0.3),
                    0 0 30px rgba(255,255,255,0.2);
                animation: pulse 2s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.8; }
            }
            
            /* Modern input fields with glow effect */
            .stTextInput > div > div {
                background: rgba(255,255,255,0.07) !important;
                border: 2px solid rgba(255,255,255,0.1) !important;
                border-radius: 12px !important;
                padding: 10px 16px !important;
                color: white !important;
                transition: all 0.3s ease !important;
                box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus {
                border-color: rgba(255,255,255,0.3) !important;
                background: rgba(255,255,255,0.15) !important;
                transform: translateY(-2px);
                box-shadow: 
                    0 5px 15px rgba(0,0,0,0.2),
                    inset 0 0 15px rgba(255,255,255,0.1);
            }
            
            .stTextInput > label {
                color: rgba(255,255,255,0.9) !important;
                font-size: 1.1em !important;
                font-weight: 500 !important;
                text-shadow: 0 0 10px rgba(255,255,255,0.3);
            }
            
            /* Enhanced button with modern gradient */
            .stButton > button {
                background: linear-gradient(135deg, #205295, #2C74B3);
                color: white;
                border: none;
                padding: 0.8rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1.1em;
                letter-spacing: 1px;
                text-transform: uppercase;
                width: 100%;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255,255,255,0.2),
                    transparent
                );
                transition: 0.5s;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .stButton > button:hover::before {
                left: 100%;
            }
            
            /* Enhanced error message */
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
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
            
            /* Enhanced credentials info */
            .credentials-info {
                color: white;
                text-align: center;
                margin-top: 1.5rem;
                padding: 1.2rem;
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(5px);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.2);
                position: relative;
                overflow: hidden;
            }
            
            .credentials-info::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(
                    circle,
                    rgba(255,255,255,0.1) 0%,
                    transparent 60%
                );
                animation: rotate 10s linear infinite;
            }
            
            .credentials-info code {
                background: rgba(255,255,255,0.15);
                padding: 0.3rem 0.8rem;
                border-radius: 8px;
                color: #fff;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255,255,255,0.2);
                display: inline-block;
                margin: 0.3rem;
                transition: all 0.3s ease;
                position: relative;
                z-index: 1;
            }
            
            .credentials-info code:hover {
                background: rgba(255,255,255,0.25);
                transform: translateY(-2px);
                box-shadow: 
                    0 5px 15px rgba(0,0,0,0.2),
                    0 0 20px rgba(255,255,255,0.1);
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
