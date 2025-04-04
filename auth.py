import streamlit as st
import pandas as pd
import hashlib
from typing import Optional, Dict, Any
import json
import os
import random

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "df" not in st.session_state:
        st.session_state.df = None
    if "sales_target" not in st.session_state:
        st.session_state.sales_target = 0.0

# Load users from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin user if file doesn't exist
        default_users = {
            "jobin.john@kritikalvision.ai": {
                "password": hashlib.sha256("kspl@jjsales123".encode()).hexdigest(),
                "role": "admin"
            }
        }
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

def verify_password(username, password):
    users = load_users()
    if username in users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == users[username]["password"]
    return False

def show_login_page():
    # Hide sidebar and main menu
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            .stApp {
                background: #0B0B1E !important;
            }

            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            [data-testid="stTextInput"] > div > div > input {
                background-color: #000 !important;
                border: 2px solid #00F5FF !important;
                border-radius: 25px !important;
                color: #00F5FF !important;
                font-size: 1em !important;
                padding: 12px 25px !important;
                font-family: 'Orbitron', sans-serif !important;
                box-shadow: 0 0 10px rgba(0, 245, 255, 0.3) !important;
            }

            [data-testid="stTextInput"] > div > div > input:focus {
                border-color: #00F5FF !important;
                box-shadow: 0 0 20px rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stTextInput"] > div > div > input::placeholder {
                color: rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stButton"] > button {
                width: 100% !important;
                background: linear-gradient(90deg, #00F5FF, #FF00FF) !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 12px !important;
                font-size: 1.1em !important;
                border-radius: 25px !important;
                border: none !important;
                transition: all 0.3s ease !important;
                font-family: 'Orbitron', sans-serif !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
            }

            [data-testid="stButton"] > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 30px rgba(0, 245, 255, 0.5) !important;
            }

            .main {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                font-family: 'Orbitron', sans-serif;
            }

            .container {
                width: 100%;
                max-width: 400px;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }

            .login-box {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 0 50px rgba(0, 245, 255, 0.3);
                border: 2px solid #00F5FF;
            }

            .login-box h1 {
                color: #00F5FF;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
                font-family: 'Orbitron', sans-serif;
            }

            .options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
                color: #00F5FF;
                font-size: 0.9em;
            }

            .remember-me {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .remember-me input[type="checkbox"] {
                accent-color: #00F5FF;
            }

            .forgot-password {
                color: #00F5FF;
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .forgot-password:hover {
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
            }

            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                pointer-events: none;
            }

            .particle {
                position: fixed;
                width: 5px;
                height: 5px;
                border-radius: 50%;
                animation: particle-animation 20s infinite linear;
            }

            @keyframes particle-animation {
                0% {
                    transform: translateY(100vh) translateX(0) scale(0);
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100vh) translateX(100px) scale(1);
                    opacity: 0;
                }
            }

            .particle:nth-child(3n) { background: #00F5FF; }
            .particle:nth-child(3n+1) { background: #FF00FF; }
            .particle:nth-child(3n+2) { background: #
