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
    
    st.markdown("""
        <style>
            /* Reset and base styles */
            .stApp {
                background: #13111C !important;
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
            
            [data-testid="stVerticalBlock"] {
                padding: 0 !important;
                gap: 0 !important;
            }
            
            /* Login container */
            .login-wrapper {
                display: flex;
                min-height: 100vh;
                background: #13111C;
            }
            
            /* Left panel */
            .login-panel {
                flex: 0 0 40%;
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(10px);
                padding: 2rem;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }
            
            /* Right panel */
            .welcome-panel {
                flex: 0 0 60%;
                background: linear-gradient(135deg, #2A1E5C, #4A1E6D, #7A1E7C);
                padding: 4rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                position: relative;
            }
            
            /* Form styles */
            .form-container {
                width: 100%;
                max-width: 320px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.03);
                padding: 2rem;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Logo/Avatar */
            .avatar {
                width: 64px;
                height: 64px;
                background: linear-gradient(45deg, #FF3366, #FF33FF);
                border-radius: 50%;
                margin: 0 auto 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.8rem;
            }
            
            /* Input fields */
            .stTextInput > div > div {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 8px !important;
                padding: 0.6rem 1rem !important;
                color: white !important;
                transition: all 0.3s ease !important;
                margin-bottom: 1rem !important;
            }
            
            .stTextInput > div > div:focus {
                border-color: #FF3366 !important;
                box-shadow: 0 0 0 1px #FF3366 !important;
            }
            
            .stTextInput > label {
                color: rgba(255, 255, 255, 0.7) !important;
                font-size: 0.9rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.25rem !important;
            }
            
            /* Button */
            .stButton > button {
                background: linear-gradient(45deg, #FF3366, #FF33FF) !important;
                color: white !important;
                border: none !important;
                padding: 0.6rem !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                width: 100% !important;
                margin-top: 0.5rem !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                opacity: 0.9 !important;
                transform: translateY(-1px) !important;
            }
            
            /* Welcome text */
            .welcome-title {
                color: white;
                font-size: 2.8em;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            
            .welcome-subtitle {
                color: rgba(255, 255, 255, 0.7);
                font-size: 1.1em;
                line-height: 1.6;
                max-width: 480px;
            }
            
            /* Error message */
            .error-message {
                color: #FF3366;
                background: rgba(255, 51, 102, 0.1);
                border: 1px solid rgba(255, 51, 102, 0.2);
                padding: 0.75rem;
                border-radius: 8px;
                margin: 1rem 0;
                font-size: 0.9rem;
            }
            
            /* Credentials info */
            .credentials-info {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 0.75rem;
                border-radius: 8px;
                margin-top: 1rem;
            }
            
            .credentials-info p {
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.85rem;
                margin: 0.25rem 0;
            }
            
            .credentials-info code {
                background: rgba(255, 255, 255, 0.1);
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
                font-size: 0.85rem;
                margin: 0 0.2rem;
            }

            /* Hide Streamlit elements */
            #MainMenu, footer, header {
                display: none !important;
            }
            
            .stDeployButton {
                display: none !important;
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .login-wrapper {
                    flex-direction: column;
                }
                
                .login-panel {
                    flex: none;
                    width: 100%;
                    padding: 2rem 1rem;
                }
                
                .welcome-panel {
                    display: none;
                }
                
                .form-container {
                    padding: 1.5rem;
                }
            }
        </style>
        
        <div class="login-wrapper">
            <div class="login-panel">
                <div class="form-container">
                    <div class="avatar">📊</div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
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
                </div>
            </div>
            <div class="welcome-panel">
                <h1 class="welcome-title">Welcome Back</h1>
                <p class="welcome-subtitle">Access your sales dashboard to track performance, analyze trends, and make data-driven decisions.</p>
            </div>
        </div>
    """, unsafe_allow_html=True) 
