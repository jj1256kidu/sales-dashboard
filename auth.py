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
    print(f"\n=== Login Attempt ===")
    print(f"Input username: '{username}'")
    print(f"Input password: '{password}'")
    
    if username in USERS:
        print(f"Username '{username}' found in USERS")
        stored_hash = USERS[username]
        input_hash = hash_password(password)
        
        print(f"Stored hash: {stored_hash}")
        print(f"Input hash:  {input_hash}")
        print(f"Hashes match: {stored_hash == input_hash}")
        
        if verify_password(password, stored_hash):
            print("Password verification successful")
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            return True
        else:
            print("Password verification failed")
    else:
        print(f"Username '{username}' not found in USERS")
        print(f"Available usernames: {list(USERS.keys())}")
    
    print("=== End Login Attempt ===\n")
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
                background: rgba(255,255,255,0.1);
                padding: 10px;
                border-radius: 8px;
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
                    <div class="credentials-info">
                        <strong>Try these exact credentials:</strong><br>
                        <code>Username: admin</code><br>
                        <code>Password: admin123</code><br><br>
                        <strong>Or:</strong><br>
                        <code>Username: guest</code><br>
                        <code>Password: guest123</code>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

print(hashlib.sha256("guest123".encode()).hexdigest())
# Should output: 84983c60f7daadc1cb8698621f802c0d9f9a3c3c295c810748fb048115c186ec 
