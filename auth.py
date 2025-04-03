import streamlit as st
import hashlib
from typing import Dict, Optional

# User credentials (username: hashed_password)
USERS = {
    "admin": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin123
    "guest": "84983c60f7daadc1cb8698621f802c0d9f9a3c3c295c810748fb048115c186ec"   # guest123
}

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed_password

def login(username: str, password: str) -> bool:
    """Attempt to log in a user"""
    if username in USERS:
        # Debug information
        print(f"Username found: {username}")
        print(f"Stored hash: {USERS[username]}")
        print(f"Input password hash: {hash_password(password)}")
        
        if verify_password(password, USERS[username]):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            return True
        else:
            print("Password verification failed")
    else:
        print(f"Username not found: {username}")
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
            .login-input {
                background: rgba(255,255,255,0.1);
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: white;
                margin-bottom: 1rem;
            }
            .login-input::placeholder {
                color: rgba(255,255,255,0.7);
            }
            .login-button {
                background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                width: 100%;
                font-size: 1.1em;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .login-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .error-message {
                color: #ff6b6b;
                text-align: center;
                margin-top: 1rem;
                font-weight: bold;
            }
            .credentials-info {
                color: #666;
                text-align: center;
                margin-top: 1rem;
                font-size: 0.9em;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="login-container">
            <h1 class="login-title">Sales Dashboard</h1>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        submit = st.form_submit_button("Login")

        if submit:
            if login(username, password):
                st.rerun()
            else:
                st.markdown('<p class="error-message">Invalid username or password</p>', unsafe_allow_html=True)
                st.markdown("""
                    <p class="credentials-info">
                        Try these credentials:<br>
                        Username: admin, Password: admin123<br>
                        Username: guest, Password: guest123
                    </p>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True) 
