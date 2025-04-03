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
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    
    # Add required external resources
    st.markdown("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
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
                background: #0f0c29 !important;
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
            
            /* Particle effect simulation with CSS */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 0;
            }
            
            .particle {
                position: absolute;
                width: 4px;
                height: 4px;
                border-radius: 50%;
                background: #00f0ff;
                animation: float 8s infinite linear;
                opacity: 0.7;
            }
            
            .particle:nth-child(2n) {
                background: #ff00e0;
            }
            
            .particle:nth-child(3n) {
                background: #ffc400;
            }
            
            @keyframes float {
                0% { transform: translate(0, 0); }
                100% { transform: translate(100px, 100px); }
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
                background: rgba(0, 0, 0, 0.7);
                border-radius: 20px;
                padding: 40px 30px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
            }
            
            .login-box h2 {
                text-align: center;
                color: #00f0ff;
                margin-bottom: 30px;
                font-size: 26px;
                font-weight: 700;
            }
            
            /* Input field styles */
            .input-wrapper {
                position: relative;
                margin-bottom: 20px;
            }
            
            .input-icon {
                position: absolute;
                top: 50%;
                left: 15px;
                transform: translateY(-50%);
                color: #7efcff;
                font-size: 14px;
                z-index: 2;
            }
            
            .stTextInput > div {
                margin: 0 !important;
            }
            
            .stTextInput > div > div {
                background: transparent !important;
                border: 1px solid #00f0ff !important;
                border-radius: 25px !important;
                padding: 0 15px 0 40px !important;
                height: 45px !important;
                color: white !important;
                font-size: 14px !important;
                transition: box-shadow 0.3s !important;
            }
            
            .stTextInput > div > div:focus {
                box-shadow: 0 0 10px #00f0ff !important;
            }
            
            .stTextInput > label {
                display: none !important;
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
            }
            
            .stButton > button:hover {
                transform: scale(1.03) !important;
                box-shadow: 0 0 15px #00f0ff !important;
            }
            
            /* Options styles */
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
            
            .options a {
                color: #a0cbe8;
                text-decoration: underline;
            }
            
            /* Error message */
            .error-message {
                color: #ff00e0;
                background: rgba(255, 0, 224, 0.1);
                border: 1px solid rgba(255, 0, 224, 0.2);
                padding: 0.75rem;
                border-radius: 12px;
                margin: 1rem 0;
                font-size: 0.9rem;
                text-align: center;
            }
            
            /* Credentials info */
            .credentials-info {
                background: rgba(0, 240, 255, 0.1);
                border: 1px solid rgba(0, 240, 255, 0.2);
                padding: 0.75rem;
                border-radius: 12px;
                margin-top: 1rem;
                text-align: center;
            }
            
            .credentials-info p {
                color: #a0cbe8;
                font-size: 0.85rem;
                margin: 0.25rem 0;
            }
            
            .credentials-info code {
                background: rgba(0, 240, 255, 0.1);
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
                font-size: 0.85rem;
                margin: 0 0.2rem;
                color: #00f0ff;
                border: 1px solid rgba(0, 240, 255, 0.2);
            }

            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
            
            /* Generate particles */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }
            
            @media (max-width: 480px) {
                .login-box {
                    padding: 30px 20px;
                }
            }
        </style>
        
        <div class="particles">
            ${Array(50).fill().map((_, i) => `
                <div class="particle" style="
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation-delay: -${Math.random() * 8}s;
                    animation-duration: ${5 + Math.random() * 5}s;
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
                <label><input type="checkbox" checked /> Remember me</label>
                <a href="#">Forgot password?</a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True) 
