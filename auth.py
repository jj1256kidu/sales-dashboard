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
            .login-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 2rem;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .login-title {
                color: white;
                text-align: center;
                font-size: 2em;
                margin-bottom: 2rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .stTextInput > div > div {
                background: rgba(255,255,255,0.1) !important;
                color: white !important;
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
