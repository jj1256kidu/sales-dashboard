import streamlit as st
import streamlit.components.v1 as components
from typing import Optional
import time

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "last_attempt_time" not in st.session_state:
    st.session_state.last_attempt_time = 0

# Simple user credentials
USERS = {
    "admin": "admin123",
    "guest": "guest123"
}

def login(username: str, password: str) -> bool:
    """Authenticate user and set session state"""
    current_time = time.time()
    
    # Check for brute force protection
    if st.session_state.login_attempts >= 3:
        if current_time - st.session_state.last_attempt_time < 30:  # 30 second cooldown
            st.error("Too many failed attempts. Please wait 30 seconds.")
            return False
        else:
            st.session_state.login_attempts = 0
    
    if username in USERS and password == USERS[username]:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_attempts = 0
        return True
    
    st.session_state.login_attempts += 1
    st.session_state.last_attempt_time = current_time
    return False

def logout():
    """Log out the current user and clear session state"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.clear()
    st.rerun()

def is_authenticated() -> bool:
    """Check if the user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[str]:
    """Get the current user's username"""
    return st.session_state.get("username")

# Cache the CSS to prevent recomputation
@st.cache_data
def get_css():
    return """
        <style>
            #MainMenu, footer, header { display: none !important; }
            [data-testid="stAlert"] {
                position: fixed !important;
                top: 20px !important;
                left: 50% !important;
                transform: translateX(-50%) !important;
                z-index: 9999 !important;
                background: rgba(255, 0, 224, 0.1) !important;
                border: 1px solid rgba(255, 0, 224, 0.2) !important;
                color: #ff00e0 !important;
                padding: 0.75rem !important;
                border-radius: 12px !important;
                backdrop-filter: blur(10px) !important;
                box-shadow: 0 0 15px rgba(255, 0, 224, 0.2) !important;
                min-width: 300px !important;
                text-align: center !important;
            }
            .stForm {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }
            .stButton > button { display: none !important; }
        </style>
    """

# Cache the HTML template to prevent recomputation
@st.cache_data
def get_html_template():
    return """
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        font-family: 'Orbitron', sans-serif;
        background-color: #0f0f25;
        color: #00f0ff;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    canvas {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 0;
        width: 100%;
        height: 100%;
    }

    .login-container {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(17, 17, 17, 0.9);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.67);
        text-align: center;
        width: 350px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        z-index: 1;
    }

    .login-container h2 {
        font-size: 28px;
        margin-bottom: 30px;
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }

    .input-box {
        display: flex;
        align-items: center;
        background-color: rgba(26, 26, 46, 0.8);
        border-radius: 30px;
        padding: 12px 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.27);
        transition: all 0.3s ease;
    }

    .input-box:focus-within {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        background-color: rgba(26, 26, 46, 0.9);
    }

    .input-box input {
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        color: #fff;
        font-size: 14px;
        margin-left: 10px;
        font-family: 'Orbitron', sans-serif;
    }

    .input-box input::placeholder {
        color: rgba(204, 204, 204, 0.7);
    }

    .icon {
        font-size: 16px;
        color: #00ffff;
        width: 20px;
        text-align: center;
    }

    .login-btn {
        background: linear-gradient(135deg, #00f0ff, #ff00ff);
        border: none;
        color: white;
        padding: 12px 40px;
        border-radius: 30px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        width: 100%;
    }

    .login-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.7);
        background: linear-gradient(135deg, #ff00ff, #00f0ff);
    }

    .login-btn:active {
        transform: translateY(1px);
    }

    .options {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        color: rgba(204, 204, 204, 0.8);
        font-size: 12px;
    }

    .options label {
        display: flex;
        align-items: center;
        gap: 5px;
        cursor: pointer;
    }

    .options input[type="checkbox"] {
        cursor: pointer;
        accent-color: #00ffff;
    }

    .options a {
        color: rgba(204, 204, 204, 0.8);
        text-decoration: none;
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    .options a:hover {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    </style>

    <canvas id="particles"></canvas>

    <div class="login-container">
        <h2>Welcome Back</h2>
        <form id="loginForm">
            <div class="input-box">
                <span class="icon">👤</span>
                <input type="text" id="username" placeholder="Username" required />
            </div>
            <div class="input-box">
                <span class="icon">🔒</span>
                <input type="password" id="password" placeholder="Password" required />
            </div>
            <button type="submit" class="login-btn">LOGIN</button>
            <div class="options">
                <label><input type="checkbox" checked /> Remember me</label>
                <a href="#">Forgot password?</a>
            </div>
        </form>
    </div>

    <script>
    (function() {
        // Canvas setup and particle animation
        const canvas = document.getElementById("particles");
        const ctx = canvas.getContext("2d");

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        let particles = [];
        const colors = ["#ff00ff", "#00ffff", "#ffaa00", "#ffffff"];

        function createParticles() {
            particles = [];
            const particleCount = Math.min(100, Math.floor((canvas.width * canvas.height) / 20000));
            
            for (let i = 0; i < particleCount; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 2 + 1,
                    dx: (Math.random() - 0.5) * 0.5,
                    dy: (Math.random() - 0.5) * 0.5,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    alpha: Math.random() * 0.5 + 0.5
                });
            }
        }
        createParticles();
        window.addEventListener('resize', createParticles);

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            ctx.globalCompositeOperation = 'lighter';
            for (let p of particles) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color + Math.floor(p.alpha * 255).toString(16).padStart(2, '0');
                ctx.fill();

                p.x += p.dx;
                p.y += p.dy;

                // Wrap particles around screen edges
                if (p.x < 0) p.x = canvas.width;
                if (p.x > canvas.width) p.x = 0;
                if (p.y < 0) p.y = canvas.height;
                if (p.y > canvas.height) p.y = 0;

                // Subtle alpha animation
                p.alpha += (Math.random() - 0.5) * 0.01;
                p.alpha = Math.max(0.3, Math.min(0.8, p.alpha));
            }
            ctx.globalCompositeOperation = 'source-over';
            
            requestAnimationFrame(draw);
        }
        draw();

        // Form handling
        const form = document.getElementById('loginForm');
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const parent = window.parent;
            const usernameInput = parent.document.querySelector('input[aria-label="Username"]');
            const passwordInput = parent.document.querySelector('input[aria-label="Password"]');
            const submitButton = parent.document.querySelector('button[type="submit"]');
            if (usernameInput && passwordInput && submitButton) {
                usernameInput.value = username;
                passwordInput.value = password;
                submitButton.click();
            }
        });
    })();
    </script>
    """

def show_login_page():
    # Add custom CSS
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Create form for handling submission
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", key="username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", key="password", label_visibility="collapsed")
        submitted = st.form_submit_button("Submit", type="primary")
    
    # Render the HTML
    components.html(get_html_template(), height=650, scrolling=False)
    
    # Handle form submission
    if submitted:
        if not username or not password:
            st.error("Please enter both username and password")
        elif login(username, password):
            st.rerun()
        else:
            st.error("Invalid username or password") 
