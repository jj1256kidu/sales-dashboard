import streamlit as st
from typing import Optional

# Set page config at the very start
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

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
    # Add required external resources
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Orbitron', sans-serif !important;
            }
            
            .stApp {
                background: #0B0B1F !important;
                height: 100vh;
                overflow: hidden;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }
            
            [data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }
            
            /* Stars background */
            .stars {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 0;
            }
            
            .star {
                position: absolute;
                width: 3px;
                height: 3px;
                background: #00f0ff;
                border-radius: 50%;
            }
            
            .star:nth-child(2n) {
                background: #ff00e0;
                width: 2px;
                height: 2px;
            }
            
            .star:nth-child(3n) {
                background: #ffc400;
                width: 2px;
                height: 2px;
            }
            
            .star:nth-child(4n) {
                background: #00f0ff;
                width: 1px;
                height: 1px;
            }
            
            /* Container styles */
            .container {
                position: relative;
                z-index: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }
            
            /* Login box styles */
            .login-box {
                background: rgba(2, 6, 23, 0.95);
                border-radius: 20px;
                padding: 40px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 0 40px rgba(0, 240, 255, 0.2);
                border: 1px solid rgba(0, 240, 255, 0.1);
            }
            
            .login-box h2 {
                text-align: center;
                color: #00f0ff;
                margin-bottom: 40px;
                font-size: 28px;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
            }
            
            /* Input field styles */
            .input-wrapper {
                position: relative;
                margin-bottom: 25px;
            }
            
            .input-icon {
                position: absolute;
                top: 50%;
                left: 20px;
                transform: translateY(-50%);
                color: #00f0ff;
                font-size: 16px;
                z-index: 2;
            }
            
            .stTextInput > div {
                margin: 0 !important;
            }
            
            .stTextInput > div > div {
                background: rgba(0, 240, 255, 0.05) !important;
                border: 1px solid #00f0ff !important;
                border-radius: 30px !important;
                padding: 0 20px 0 45px !important;
                height: 50px !important;
                color: #00f0ff !important;
                font-size: 16px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 0 10px rgba(0, 240, 255, 0.1) !important;
            }
            
            .stTextInput > div > div:focus {
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.2) !important;
                border-color: #00f0ff !important;
                background: rgba(0, 240, 255, 0.1) !important;
            }
            
            .stTextInput input::placeholder {
                color: rgba(0, 240, 255, 0.5) !important;
            }
            
            .stTextInput > label {
                display: none !important;
            }
            
            /* Button styles */
            .stButton > button {
                width: 100% !important;
                height: 50px !important;
                background: linear-gradient(90deg, #00f0ff, #ff00e0) !important;
                color: white !important;
                font-weight: bold !important;
                font-size: 18px !important;
                border: none !important;
                border-radius: 30px !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                margin: 10px 0 !important;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.5) !important;
            }
            
            /* Options styles */
            .options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
                padding: 0 10px;
            }
            
            .remember-me {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #00f0ff;
                font-size: 14px;
            }
            
            .remember-me input[type="checkbox"] {
                width: 16px;
                height: 16px;
                accent-color: #00f0ff;
            }
            
            .forgot-password {
                color: #00f0ff;
                font-size: 14px;
                text-decoration: none;
                transition: all 0.3s ease;
            }
            
            .forgot-password:hover {
                text-shadow: 0 0 10px #00f0ff;
            }

            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
        </style>
        
        <div class="stars">
            ${Array(100).fill().map((_, i) => `
                <div class="star" style="
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    opacity: ${0.3 + Math.random() * 0.7};
                "></div>
            `).join('')}
        </div>
        
        <div class="container">
            <div class="login-box">
                <h2>Welcome Back</h2>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<div class="input-wrapper"><i class="fas fa-user input-icon"></i>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="Username")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-wrapper"><i class="fas fa-lock input-icon"></i>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        submit = st.form_submit_button("LOGIN")
        
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
            <div class="options">
                <label class="remember-me">
                    <input type="checkbox" checked />
                    Remember me
                </label>
                <a href="#" class="forgot-password">Forgot password?</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True) 
