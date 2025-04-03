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
            /* Modern animated background */
            .stApp {
                background: #13111C;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                display: flex;
                align-items: stretch;
            }
            
            /* Split screen container */
            .split-container {
                display: flex;
                width: 100%;
                height: 100vh;
                margin: 0;
                padding: 0;
            }
            
            /* Left panel - Login form */
            .login-panel {
                flex: 0 0 40%;
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(10px);
                padding: 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            /* Right panel - Welcome visual */
            .welcome-panel {
                flex: 0 0 60%;
                background: linear-gradient(135deg, #2A1E5C, #4A1E6D, #7A1E7C);
                padding: 4rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
                overflow: hidden;
            }
            
            /* Animated background elements */
            .bg-element {
                position: absolute;
                border-radius: 50%;
                filter: blur(80px);
                opacity: 0.4;
                animation: float 8s infinite ease-in-out;
            }
            
            .bg-element-1 {
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, #FF3366, #FF338800);
                top: -100px;
                right: -100px;
            }
            
            .bg-element-2 {
                width: 400px;
                height: 400px;
                background: radial-gradient(circle, #3366FF, #3366FF00);
                bottom: -150px;
                left: -150px;
                animation-delay: -4s;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0) scale(1); }
                50% { transform: translateY(-20px) scale(1.05); }
            }
            
            /* Avatar/Logo */
            .avatar {
                width: 80px;
                height: 80px;
                background: linear-gradient(45deg, #FF3366, #FF33FF);
                border-radius: 50%;
                margin: 0 auto 2rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                color: white;
                box-shadow: 0 8px 32px rgba(255, 51, 102, 0.3);
            }
            
            /* Welcome text styles */
            .welcome-title {
                color: #fff;
                font-size: 3.5em;
                font-weight: 700;
                margin-bottom: 1rem;
                line-height: 1.2;
                position: relative;
            }
            
            .welcome-subtitle {
                color: rgba(255, 255, 255, 0.7);
                font-size: 1.1em;
                line-height: 1.6;
                max-width: 500px;
            }
            
            /* Form container */
            .form-container {
                width: 100%;
                max-width: 320px;
                margin: 0 auto;
            }
            
            /* Input fields */
            .stTextInput > div > div {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px !important;
                padding: 0.8rem 1rem !important;
                color: white !important;
                transition: all 0.3s ease !important;
                margin-bottom: 1rem !important;
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus {
                border-color: #FF3366 !important;
                background: rgba(255, 255, 255, 0.05) !important;
                transform: translateY(-2px);
            }
            
            .stTextInput > label {
                color: rgba(255, 255, 255, 0.8) !important;
                font-size: 0.9rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.5rem !important;
                text-align: left !important;
            }
            
            /* Login button */
            .stButton > button {
                background: linear-gradient(45deg, #FF3366, #FF33FF) !important;
                color: white !important;
                border: none !important;
                padding: 0.8rem !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                letter-spacing: 0.5px !important;
                width: 100% !important;
                transition: all 0.3s ease !important;
                margin-top: 1rem !important;
                text-transform: uppercase !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(255, 51, 102, 0.4) !important;
            }
            
            /* Error message */
            .error-message {
                color: #FF3366;
                text-align: left;
                margin-top: 1rem;
                padding: 1rem;
                background: rgba(255, 51, 102, 0.1);
                border-radius: 12px;
                border: 1px solid rgba(255, 51, 102, 0.2);
                font-size: 0.9rem;
            }
            
            /* Credentials info */
            .credentials-info {
                margin-top: 1.5rem;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .credentials-info p {
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.9rem;
                margin: 0.5rem 0;
            }
            
            .credentials-info code {
                background: rgba(255, 255, 255, 0.1);
                padding: 0.3rem 0.8rem;
                border-radius: 8px;
                color: #fff;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255, 255, 255, 0.15);
                display: inline-block;
                margin: 0.2rem;
                font-size: 0.85rem;
            }

            /* Hide Streamlit branding */
            #MainMenu, footer, header {
                visibility: hidden;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .split-container {
                    flex-direction: column;
                }
                .login-panel, .welcome-panel {
                    flex: 0 0 100%;
                    padding: 2rem;
                }
                .welcome-panel {
                    display: none;
                }
            }
        </style>
        
        <div class="split-container">
            <div class="login-panel">
                <div class="bg-element bg-element-1"></div>
                <div class="bg-element bg-element-2"></div>
                <div class="form-container">
                    <div class="avatar">📊</div>
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
            </div>
            <div class="welcome-panel">
                <h1 class="welcome-title">Welcome Back</h1>
                <p class="welcome-subtitle">Access your sales dashboard to track performance, analyze trends, and make data-driven decisions that drive business growth.</p>
            </div>
        </div>
    """, unsafe_allow_html=True) 
