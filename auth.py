import streamlit as st
from typing import Optional

# Set page config at the very start - MUST be the first Streamlit command
st.set_page_config(
    page_title="Sales Dashboard Login",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    # Add required external resources and base styles
    st.markdown("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Orbitron', sans-serif !important;
                }

                .stApp {
                    background: #0f0c29 !important;
                }

                div[data-testid="stVerticalBlock"] {
                    gap: 0 !important;
                    padding: 0 !important;
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

                #tsparticles {
                    position: fixed;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    z-index: 0;
                }

                .container {
                    position: relative;
                    z-index: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }

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
                    z-index: 2;
                }

                .stTextInput > div {
                    margin: 0 !important;
                }

                .stTextInput > div > div {
                    width: 100% !important;
                    height: 45px !important;
                    padding: 0 15px 0 40px !important;
                    border: 1px solid #00f0ff !important;
                    background: transparent !important;
                    color: white !important;
                    border-radius: 25px !important;
                    font-size: 14px !important;
                    outline: none !important;
                    transition: box-shadow 0.3s !important;
                }

                .stTextInput > div > div:focus-within {
                    box-shadow: 0 0 10px #00f0ff !important;
                }

                .stTextInput input {
                    color: white !important;
                }

                .stTextInput input::placeholder {
                    color: #7efcff !important;
                    opacity: 0.7 !important;
                }

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

                .options input[type="checkbox"] {
                    cursor: pointer;
                }

                .options a {
                    color: #a0cbe8;
                    text-decoration: underline;
                }

                .stAlert {
                    background: rgba(255, 0, 224, 0.1) !important;
                    border: 1px solid rgba(255, 0, 224, 0.2) !important;
                    color: #ff00e0 !important;
                    padding: 0.75rem !important;
                    border-radius: 12px !important;
                    margin: 1rem 0 !important;
                }

                .stAlert > div {
                    padding: 0 !important;
                }

                #MainMenu, footer, header {
                    display: none !important;
                }

                @media (max-width: 480px) {
                    .login-box {
                        padding: 30px 20px;
                    }
                }
            </style>
        </head>
        <body>
            <div id="tsparticles"></div>
            <script>
                window.onload = function() {
                    if (typeof tsParticles !== 'undefined') {
                        tsParticles.load("tsparticles", {
                            fullScreen: { enable: false },
                            background: { color: "#0f0c29" },
                            particles: {
                                number: { value: 100 },
                                color: { value: ["#00f0ff", "#ff00e0", "#ffc400"] },
                                shape: { type: ["circle", "square"] },
                                opacity: { value: 0.7 },
                                size: { value: 4 },
                                move: {
                                    enable: true,
                                    speed: 1,
                                    direction: "none",
                                    random: false,
                                    straight: false,
                                    outModes: "bounce"
                                }
                            },
                            interactivity: {
                                events: {
                                    onHover: { enable: true, mode: "repulse" },
                                    onClick: { enable: true, mode: "push" }
                                },
                                modes: {
                                    repulse: { distance: 100 },
                                    push: { quantity: 4 }
                                }
                            },
                            detectRetina: true
                        });
                    }
                }
            </script>
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
        </body>
        </html>
    """, unsafe_allow_html=True) 
