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
                background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
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
            
            /* Floating login container with glass effect */
            .login-container {
                max-width: 450px;
                margin: 2rem auto;
                padding: 2.5rem;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                border: 1px solid rgba(255, 255, 255, 0.18);
                animation: float 6s ease-in-out infinite;
            }
            
            @keyframes float {
                0% {
                    transform: translatey(0px);
                }
                50% {
                    transform: translatey(-20px);
                }
                100% {
                    transform: translatey(0px);
                }
            }
            
            /* Glowing title effect */
            .login-title {
                color: white;
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 2rem;
                text-shadow: 0 0 10px rgba(255,255,255,0.3),
                             0 0 20px rgba(255,255,255,0.3),
                             0 0 30px rgba(255,255,255,0.3);
                animation: glow 3s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from {
                    text-shadow: 0 0 10px rgba(255,255,255,0.3),
                                0 0 20px rgba(255,255,255,0.3),
                                0 0 30px rgba(255,255,255,0.3);
                }
                to {
                    text-shadow: 0 0 20px rgba(255,255,255,0.5),
                                0 0 30px rgba(255,255,255,0.5),
                                0 0 40px rgba(255,255,255,0.5);
                }
            }
            
            /* Modern input fields */
            .stTextInput > div > div {
                background: rgba(255,255,255,0.05) !important;
                border: 2px solid rgba(255,255,255,0.1) !important;
                border-radius: 12px !important;
                padding: 8px 16px !important;
                color: white !important;
                transition: all 0.3s ease !important;
            }
            
            .stTextInput > div > div:hover,
            .stTextInput > div > div:focus {
                border-color: rgba(255,255,255,0.3) !important;
                background: rgba(255,255,255,0.1) !important;
                transform: translateY(-2px);
            }
            
            .stTextInput > label {
                color: white !important;
            }
            .stButton > button {
                background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
                color: white;
                border: none;
                padding: 0.5rem 2rem;
                width: 100%;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .error-message {
                color: #ff6b6b;
                text-align: center;
                margin-top: 1rem;
                padding: 0.5rem;
                background: rgba(255,99,99,0.1);
                border-radius: 8px;
            }
            .credentials-info {
                color: white;
                text-align: center;
                margin-top: 1rem;
                padding: 1rem;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
            }
            .credentials-info code {
                background: rgba(255,255,255,0.2);
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
                color: #fff;
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
                        Invalid username or password
                    </div>
                    <div class="credentials-info">
                        <p><strong>Available accounts:</strong></p>
                        <p>
                            <code>admin</code> / <code>admin123</code>
                            <br>
                            <code>guest</code> / <code>guest123</code>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) 
