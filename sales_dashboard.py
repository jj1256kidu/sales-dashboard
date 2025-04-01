import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from streamlit_lottie import st_lottie
import requests
import json
import time
import random

# Set page config with full page mode and theme
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for theme and data
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'df' not in st.session_state:
    st.session_state.df = None
if 'column_map' not in st.session_state:
    st.session_state.column_map = {}
if 'upload_time' not in st.session_state:
    st.session_state.upload_time = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'sheet_name' not in st.session_state:
    st.session_state.sheet_name = None
if 'data_uploaded' not in st.session_state:
    st.session_state.data_uploaded = False
if 'dashboard_view' not in st.session_state:
    st.session_state.dashboard_view = 'welcome'
if 'query_index' not in st.session_state:
    st.session_state.query_index = 0
if 'animation_loaded' not in st.session_state:
    st.session_state.animation_loaded = False

# Initialize session state for navigation if not exists
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'data_input'

# Function to load lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load lottie animations
data_animation_url = "https://assets9.lottiefiles.com/packages/lf20_49rdyysj.json"
success_animation_url = "https://assets4.lottiefiles.com/packages/lf20_uu0x8lqv.json"
analytics_animation_url = "https://assets10.lottiefiles.com/private_files/lf30_qgah66oi.json"

# Borealis-inspired theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'background': '#0F172A',     # Dark slate background
            'text': '#F8FAFC',           # Brighter white text for better contrast
            'card_bg': '#1E293B',        # Slightly lighter slate for cards
            'border': '#334155',         # Border color
            'primary': '#60A5FA',        # Brighter blue accent
            'secondary': '#CBD5E1',      # Lighter gray for better visibility
            'success': '#4ADE80',        # Brighter green for success
            'hover': '#2D3748',          # Hover state
            'header': '#1E293B',         # Header background
            'metric_bg': '#1E293B',      # Metric card background
            'metric_border': '#334155',  # Metric card border
            'accent1': '#818CF8',        # Brighter indigo accent
            'accent2': '#F472B6',        # Brighter pink accent
            'warning': '#FBBF24',        # Brighter amber warning
            'error': '#F87171',          # Brighter red error
            'input_bg': '#1E293B',       # Input background
            'input_border': '#475569',   # Lighter input border
            'input_text': '#F8FAFC',     # Bright input text
            'select_bg': '#1E293B',      # Select background
            'select_border': '#475569',  # Lighter select border
            'select_text': '#F8FAFC',    # Bright select text
            'table_header': '#1E293B',   # Table header background
            'table_row': '#1E293B',      # Table row background
            'table_hover': '#2D3748',    # Table row hover
            'table_border': '#475569',   # Lighter table border
            'table_text': '#F8FAFC',     # Bright table text
            'sidebar_bg': '#1E293B',     # Sidebar background
            'sidebar_text': '#F8FAFC',   # Bright sidebar text
            'glass_bg': 'rgba(30, 41, 59, 0.7)', # Glass background
            'glass_border': 'rgba(51, 65, 85, 0.5)' # Glass border
        }
    else:
        return {
            'background': '#F2F6FF',     # Soft pastel background
            'text': '#1A1A1A',           # Dark text
            'card_bg': '#FFFFFF',        # White cards
            'border': '#E5E7EB',         # Light border
            'primary': '#60A5FA',        # Sky blue accent
            'secondary': '#6B7280',      # Muted gray
            'success': '#3DD598',        # Mint green
            'hover': '#F3F4F6',          # Hover state
            'header': '#FFFFFF',         # Header background
            'metric_bg': '#FFFFFF',      # Metric card background
            'metric_border': '#E5E7EB',  # Metric card border
            'accent1': '#A78BFA',        # Lavender accent
            'accent2': '#3DD598',        # Mint green accent
            'warning': '#F59E0B',        # Amber warning
            'error': '#EF4444',          # Red error
            'input_bg': '#FFFFFF',       # Input background
            'input_border': '#E5E7EB',   # Input border
            'input_text': '#1A1A1A',     # Input text
            'select_bg': '#FFFFFF',      # Select background
            'select_border': '#E5E7EB',  # Select border
            'select_text': '#1A1A1A',    # Select text
            'radio_bg': '#FFFFFF',       # Radio background
            'radio_border': '#E5E7EB',   # Radio border
            'radio_text': '#1A1A1A',     # Radio text
            'table_header': '#F8FAFC',   # Table header background
            'table_row': '#FFFFFF',      # Table row background
            'table_hover': '#F3F4F6',    # Table row hover
            'table_border': '#E5E7EB',   # Table border
            'table_text': '#1A1A1A',     # Table text
            'sidebar_bg': '#FFFFFF',     # Sidebar background
            'sidebar_text': '#1A1A1A',   # Sidebar text
            'glass_bg': 'rgba(255, 255, 255, 0.7)', # Glass background
            'glass_border': 'rgba(229, 231, 235, 0.5)' # Glass border
        }

# Get current theme colors
colors = get_theme_colors()

# Helper functions
def format_lakhs(value):
    try:
        return f"₹{float(value)/100000:,.2f}L"
    except (ValueError, TypeError):
        return "₹0.00L"

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def safe_sort_unique(series):
    """Safely sort unique values from a series, handling mixed types."""
    unique_values = series.unique()
    return sorted([str(x) for x in unique_values if pd.notna(x)])

def apply_theme_to_plot(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Inter, sans-serif",
            color=colors['text']
        ),
        xaxis=dict(
            gridcolor=colors['border'],
            color=colors['text']
        ),
        yaxis=dict(
            gridcolor=colors['border'],
            color=colors['text']
        ),
        legend=dict(
            font=dict(color=colors['text'])
        )
    )
    return fig

# Initialize session state for configuration
if 'dashboard_config' not in st.session_state:
    st.session_state.dashboard_config = {
        'show_kpis': True,
        'show_quarter_breakdown': True,
        'show_hunting_farming': True,
        'show_monthly_trend': True,
        'show_sales_funnel': True,
        'show_strategy_view': True,
        'show_leaderboard': True,
        'show_geo_view': True,
        'show_detailed_view': True,
        'show_weighted_revenue': True,
        'show_win_rate': True,
        'show_financial_year': True
    }

# Custom CSS for modern dashboard with animations and premium styling
st.markdown(f"""
<style>
    /* Google Fonts - Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base Theme */
    :root {{
        --background-color: {colors['background']};
        --text-color: {colors['text']};
        --card-bg-color: {colors['card_bg']};
        --glass-bg-color: {colors['glass_bg']};
        --glass-border-color: {colors['glass_border']};
        --border-color: {colors['border']};
        --primary-color: {colors['primary']};
        --secondary-color: {colors['secondary']};
        --success-color: {colors['success']};
        --accent1-color: {colors['accent1']};
        --accent2-color: {colors['accent2']};
        --hover-color: {colors['hover']};
    }}
    
    /* Main Layout */
    .main {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        font-family: 'Inter', sans-serif;
        padding: 0 !important;
        overflow-x: hidden;
    }}
    
    .stApp {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--background-color);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--secondary-color);
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{display: none;}}
    footer {{display: none;}}
    .reportview-container {{
        margin-top: -2em;
    }}
    .stDeployButton {{display:none;}}
    
    /* Animated Background */
    .animated-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }}
    
    .bubble {{
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(
            circle at 30% 30%,
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0.05) 100%
        );
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.02);
        backdrop-filter: blur(2px);
        -webkit-backdrop-filter: blur(2px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        animation: float-animation 20s infinite ease-in-out;
    }}
    
    @keyframes float-animation {{
        0% {{ transform: translate(0, 0) rotate(0deg); }}
        25% {{ transform: translate(5%, 10%) rotate(5deg); }}
        50% {{ transform: translate(10%, 5%) rotate(0deg); }}
        75% {{ transform: translate(5%, -5%) rotate(-5deg); }}
        100% {{ transform: translate(0, 0) rotate(0deg); }}
    }}
    
    .bubble:nth-child(1) {{
        width: 20vw;
        height: 20vw;
        top: 10%;
        left: 10%;
        animation-delay: 0s;
        animation-duration: 30s;
        opacity: 0.5;
    }}
    
    .bubble:nth-child(2) {{
        width: 25vw;
        height: 25vw;
        top: 60%;
        left: 15%;
        animation-delay: -5s;
        animation-duration: 25s;
        opacity: 0.3;
    }}
    
    .bubble:nth-child(3) {{
        width: 35vw;
        height: 35vw;
        top: 30%;
        right: 10%;
        animation-delay: -10s;
        animation-duration: 35s;
        opacity: 0.4;
    }}
    
    .bubble:nth-child(4) {{
        width: 15vw;
        height: 15vw;
        bottom: 10%;
        right: 20%;
        animation-delay: -7s;
        animation-duration: 20s;
        opacity: 0.2;
    }}
    
    /* Welcome Page */
    .welcome-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        width: 100%;
        padding: 2rem;
    }}
    
    /* Glassmorphism Card */
    .glass-card {{
        background: var(--glass-bg-color);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border-color);
        padding: 2.5rem;
        max-width: 800px;
        width: 100%;
        margin: 2rem auto;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform: translateY(0);
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px 0 rgba(31, 38, 135, 0.18);
    }}
    
    /* Typography */
    .hero-title {{
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(
            135deg, 
            var(--primary-color) 0%, 
            var(--accent1-color) 100%
        );
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.2;
    }}
    
    .subtitle {{
        font-size: 1.25rem;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 2.5rem;
        opacity: 0.85;
        font-weight: 400;
    }}
    
    /* Upload Zone */
    .upload-zone {{
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }}
    
    .upload-zone:hover {{
        background: rgba(255, 255, 255, 0.1);
        border-color: var(--primary-color);
        transform: scale(1.02);
    }}
    
    /* AI Query Box */
    .query-box {{
        background: rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }}
    
    .query-box:hover {{
        border-color: var(--primary-color);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }}
    
    .query-title {{
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .query-input {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        width: 100%;
        color: var(--text-color);
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }}
    
    .query-input:focus {{
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
    }}
    
    /* Button Styles */
    .primary-button {{
        background: linear-gradient(
            135deg, 
            var(--primary-color) 0%, 
            var(--accent1-color) 100%
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        display: block;
        width: 100%;
        text-decoration: none;
    }}
    
    .primary-button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(96, 165, 250, 0.3);
    }}
    
    .primary-button:active {{
        transform: translateY(0);
    }}
    
    /* Dashboard Navigation */
    .dashboard-nav {{
        display: flex;
        margin-bottom: 2rem;
        overflow-x: auto;
        padding: 0.5rem;
        gap: 0.5rem;
        background: var(--glass-bg-color);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    .nav-item {{
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .nav-item:hover {{
        background: rgba(255, 255, 255, 0.1);
    }}
    
    .nav-item.active {{
        background: rgba(96, 165, 250, 0.2);
        color: var(--primary-color);
    }}
    
    /* Dashboard Sections */
    .dashboard-section {{
        padding: 1rem 0;
        animation: fadeIn 0.5s ease;
    }}
    
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Dashboard Cards */
    .dashboard-card {{
        background: var(--glass-bg-color);
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border-color);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.07);
    }}
    
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .card-title {{
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }}
    
    /* Animated Placeholder Text */
    @keyframes textFade {{
        0%, 20% {{ opacity: 0; transform: translateY(5px); }}
        5%, 15% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animated-placeholder {{
        position: relative;
        display: inline-block;
    }}
    
    .placeholder-item {{
        position: absolute;
        top: 0;
        left: 0;
        opacity: 0;
        animation: textFade 10s infinite;
    }}
    
    /* Theme Toggle Button */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1000;
        background: var(--glass-bg-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border-color);
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 2.2rem;
        }}
        
        .subtitle {{
            font-size: 1rem;
        }}
        
        .glass-card {{
            padding: 1.5rem;
        }}
    }}
    
    /* Lottie animation container */
    .lottie-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }}
    
    /* Custom form elements styling */
    input, textarea, select {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: var(--text-color) !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }}
    
    input:focus, textarea:focus, select:focus {{
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
    }}
    
    /* Animation for the query placeholder text */
    @keyframes placeholderFade {{
        0%, 16% {{ opacity: 0; transform: translateY(5px); }}
        4%, 12% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .placeholder-text {{
        position: absolute;
        opacity: 0;
        animation: placeholderFade 24s infinite;
    }}
    
    .placeholder-text:nth-child(1) {{ animation-delay: 0s; }}
    .placeholder-text:nth-child(2) {{ animation-delay: 4s; }}
    .placeholder-text:nth-child(3) {{ animation-delay: 8s; }}
    .placeholder-text:nth-child(4) {{ animation-delay: 12s; }}
    .placeholder-text:nth-child(5) {{ animation-delay: 16s; }}
    .placeholder-text:nth-child(6) {{ animation-delay: 20s; }}
    
    /* Animation for page transitions */
    @keyframes slideIn {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .page-transition {{
        animation: slideIn 0.5s ease forwards;
    }}
    
    /* Loading animation */
    .loading-animation {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 200px;
    }}
    
    /* Hide Streamlit components when needed */
    .hide-component {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# Check if data is loaded
has_data = st.session_state.df is not None

# Main application flow
def main():
    # Animated background bubbles
    st.markdown("""
    <div class="animated-bg">
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle button in top right
    with st.container():
        cols = st.columns([20, 1])
        with cols[1]:
            theme_options = {
                "🌙": "dark",
                "☀️": "light"
            }
            current_theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
            if st.button(current_theme_icon, key="theme_toggle"):
                # Toggle theme
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
    
    # Welcome page - full screen with animations
    if not has_data:
        welcome_screen()
    else:
        dashboard_screen()

def welcome_screen():
    # Welcome container
    st.markdown('<div class="welcome-container page-transition">', unsafe_allow_html=True)
    
    # Glass card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Hero title and subtitle
    st.markdown('<h1 class="hero-title">Welcome to Sales Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your file to unlock powerful insights</p>', unsafe_allow_html=True)
    
    # Lottie animation
    if not st.session_state.animation_loaded:
        lottie_data = load_lottieurl(data_animation_url)
        if lottie_data:
            st.session_state.animation_loaded = True
            st.session_state.lottie_data = lottie_data
    
    if st.session_state.animation_loaded:
        st_lottie(st.session_state.lottie_data, height=200, key="initial_animation")
    
    # Upload zone
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your file here or click to browse",
        type=['xlsx', 'csv'],
        key="file_uploader",
        label_visibility="collapsed"
    )
    st.markdown("""
        <div style="font-size: 0.9rem; opacity: 0.7; margin-top: -1rem;">
            Supports .xlsx, .csv, or Google Sheets URL
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Google Sheets URL option
    sheet_url = st.text_input(
        "Or enter a Google Sheets URL",
        key="sheet_url",
        placeholder="Paste your Google Sheets URL here"
    )
    
    # AI Query Box
    st.markdown('<div class="query-box">', unsafe_allow_html=True)
    st.markdown('<div class="query-title">🧠 AI-Powered Insights</div>', unsafe_allow_html=True)
    
    # Animated placeholder for query input
    query_placeholders = [
        "Which practice has the highest pipeline?",
        "Show me Q1 opportunities",
        "Compare sales by region",
        "What's my win rate for Q2?",
        "Show top 5 deals by value",
        "Which sales owner has best conversion?"
    ]
    
    # Create the placeholder container
    placeholder_html = """
    <div style="position: relative; height: 24px; margin-bottom: 8px;">
    """
    for i, placeholder in enumerate(query_placeholders):
        placeholder_html += f'<div class="placeholder-text" style="animation-delay: {i*4}s;">{placeholder}</div>'
    placeholder_html += "</div>"
    st.markdown(placeholder_html, unsafe_allow_html=True)
    
    # Actual query input
    query = st.text_input(
        "Ask your data anything...",
        key="ai_query",
        label_visibility="collapsed",
        placeholder=""
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process file if uploaded
    if uploaded_file is not None or sheet_url:
        with st.spinner("Processing your data..."):
            try:
                if uploaded_file is not None:
                    # Handle Excel/CSV file
                    if uploaded_file.name.endswith('.xlsx'):
                        excel_file = pd.ExcelFile(uploaded_file)
                        sheet_names = excel_file.sheet_names
                        
                        # Sheet selection
                        selected_sheet = st.selectbox(
                            "Select Sheet",
                            options=sheet_names,
                            key="sheet_selector"
                        )
                        
                        # Load data from selected sheet
                        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                        st.session_state.sheet_name = selected_sheet
                    else:
                        # Handle CSV
                        df = pd.read_csv(uploaded_file)
                        st.session_state.sheet_name = "CSV Data"
                    
                    # Store filename in session state
                    st.session_state.file_name = uploaded_file.name
                else:
                    # Handle Google Sheets URL
                    csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
                    df = pd.read_csv(csv_url)
                    st.session_state.file_name = "Google Sheet"
                    st.session_state.sheet_name = "Sheet Data"
                
                # Store data in session state
                st.session_state.df = df
                st.session_state.upload_time = datetime.now()
                st.session_state.data_uploaded = True
                
                # Show success message
                st_lottie(load_lottieurl(success_animation_url), height=150, key="success_animation")
                st.success(f"Data loaded successfully! {len(df)} rows from {st.session_state.file_name}")
                
                # Data preview
                st.markdown("<h3>Data Preview</h3>", unsafe_allow_html=True)
                st.dataframe(df.head(5), use_container_width=True)
                
                # View Dashboard button
                if st.button("🔍 View Dashboard", key="view_dashboard", type="primary", use_container_width=True):
                    st.session_state.dashboard_view = 'overview'
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    # Close glass card and welcome container
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard_screen():
    # Dashboard views
    views = {
        'overview': {'label': '🌐 Overview', 'function': show_overview},
        'trends': {'label': '📈 Trends', 'function': show_trends},
        'funnel': {'label': '🔄 Sales Funnel', 'function': show_funnel},
        'strategy': {'label': '🎯 Strategy Map', 'function': show_strategy},
        'leaderboard': {'label': '🏆 Leaderboard', 'function': show_leaderboard},
        'geo': {'label': '🌍 Geography', 'function': show_geo},
        'detailed': {'label': '🧾 Details', 'function': show_detailed},
        'editor': {'label': '✏️ Editor', 'function': show_editor}
    }
    
    # Dashboard navigation
    st.markdown('<div class="dashboard-nav">', unsafe_allow_html=True)
    cols = st.columns(len(views))
    
    for i, (view_id, view_info) in enumerate(views.items()):
        with cols[i]:
            active_class = "active" if st.session_state.dashboard_view == view_id else ""
            if st.button(view_info['label'], key=f"nav_{view_id}", 
                         use_container_width=True, 
                         help=f"View {view_id} dashboard"):
                st.session_state.dashboard_view = view_id
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current view
    st.markdown(f'<div class="dashboard-section page-transition" id="{st.session_state.dashboard_view}">', 
               unsafe_allow_html=True)
    
    # Display current dashboard view
    current_view = st.session_state.dashboard_view
    if current_view in views:
        views[current_view]['function']()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Define dashboard view functions
def show_overview():
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🎯 Key Performance Indicators</h2>
            </div>
    """, unsafe_allow_html=True)
    
    # Dynamic KPI display
    filtered_df = st.session_state.df.copy()
    
    # Create a nice layout for KPIs with modern styling
    kpi_cols = st.columns(3)
    
    # Total Amount
    with kpi_cols[0]:
        try:
            total_amount = filtered_df['Amount'].sum() / 100000
            st.metric(
                "Total Pipeline",
                format_lakhs(total_amount * 100000),
                delta=None,
                delta_color="normal"
            )
        except:
            st.metric("Total Pipeline", "N/A", delta=None)
    
    # Closed Won Amount
    with kpi_cols[1]:
        try:
            won_amount = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
            st.metric(
                "Closed Won",
                format_lakhs(won_amount * 100000),
                delta=None,
                delta_color="normal"
            )
        except:
            st.metric("Closed Won", "N/A", delta=None)
            
    # Win Rate
    with kpi_cols[2]:
        try:
            win_rate = (filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])].shape[0] / 
                       filtered_df.shape[0] * 100)
            st.metric(
                "Win Rate",
                f"{win_rate:.1f}%",
                delta=None,
                delta_color="normal"
            )
        except:
            st.metric("Win Rate", "N/A", delta=None)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Financial Year Analysis
    if 'Expected Close Date' in filtered_df.columns:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">💰 Financial Year Analysis</h2>
                </div>
        """, unsafe_allow_html=True)
        
        try:
            # Convert Expected Close Date to datetime if it's not already
            filtered_df['Date'] = pd.to_datetime(filtered_df['Expected Close Date'], errors='coerce')
            
            # Add Financial Year column
            filtered_df['Financial Year'] = filtered_df['Date'].apply(
                lambda x: f"FY{str(x.year)[2:]}-{str(x.year + 1)[2:]}" if x.month >= 4 
                else f"FY{str(x.year - 1)[2:]}-{str(x.year)[2:]}" if pd.notnull(x) else "Unknown"
            )
            
            # Calculate metrics by Financial Year
            fy_metrics = filtered_df.groupby('Financial Year').agg({
                'Amount': ['sum', 'count'],
                'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
            }).reset_index()
            
            fy_metrics.columns = ['Financial Year', 'Total Amount', 'Deal Count', 'Won Deals']
            fy_metrics['Win Rate'] = (fy_metrics['Won Deals'] / fy_metrics['Deal Count'] * 100).round(1)
            fy_metrics['Total Amount'] = fy_metrics['Total Amount'] / 100000  # Convert to Lakhs
            
            # Remove "Unknown" FY and sort by Financial Year
            fy_metrics = fy_metrics[fy_metrics['Financial Year'] != "Unknown"].sort_values('Financial Year')
            
            if not fy_metrics.empty:
                # Create a combined bar and line chart
                fig = go.Figure()
                
                # Add bar chart for Total Amount
                fig.add_trace(go.Bar(
                    x=fy_metrics['Financial Year'],
                    y=fy_metrics['Total Amount'],
                    name='Total Amount',
                    marker_color=colors['primary'],
                    text=fy_metrics['Total Amount'].apply(lambda x: f'₹{x:.2f}L'),
                    textposition='outside'
                ))
                
                # Add line chart for Win Rate
                fig.add_trace(go.Scatter(
                    x=fy_metrics['Financial Year'],
                    y=fy_metrics['Win Rate'],
                    name='Win Rate',
                    yaxis='y2',
                    line=dict(color=colors['success'], width=2),
                    mode='lines+markers+text',
                    text=fy_metrics['Win Rate'].apply(lambda x: f'{x:.1f}%'),
                    textposition='top center'
                ))
                
                # Apply theme
                fig = apply_theme_to_plot(fig)
                
                # Update layout with simplified configuration
                fig.update_layout(
                    title='Financial Year Performance Overview',
                    xaxis_title='Financial Year',
                    yaxis_title='Total Amount (Lakhs)',
                    yaxis2=dict(
                        title='Win Rate (%)',
                        overlaying='y',
                        side='right',
                        range=[0, 100]
                    ),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, key="financial_year")
                
                # Display metrics table with formatting
                st.dataframe(
                    fy_metrics.style.format({
                        'Total Amount': '₹{:.2f}L',
                        'Deal Count': '{:,.0f}',
                        'Won Deals': '{:,.0f}',
                        'Win Rate': '{:.1f}%'
                    }),
                    use_container_width=True
                )
            else:
                st.info("No financial year data available for the selected filters.")
            
        except Exception as e:
            st.error(f"Error in Financial Year Analysis: {str(e)}")
            st.info("Please check if the Expected Close Date column contains valid dates.")
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Quarter-wise Breakdown
    if 'Quarter' in filtered_df.columns:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">🏢 Quarter-wise Breakdown</h2>
                </div>
        """, unsafe_allow_html=True)
        
        try:
            quarter_metrics = filtered_df.groupby('Quarter').agg({
                'Amount': ['sum', 'count'],
            }).reset_index()
            
            quarter_metrics.columns = ['Quarter', 'Total Amount (Lakhs)', 'Number of Deals']
            quarter_metrics['Total Amount (Lakhs)'] = quarter_metrics['Total Amount (Lakhs)'] / 100000
            
            fig = px.bar(
                quarter_metrics,
                x='Quarter',
                y='Total Amount (Lakhs)',
                title='Quarter-wise Pipeline Distribution',
                text='Total Amount (Lakhs)',
                labels={'Total Amount (Lakhs)': 'Amount (Lakhs)'}
            )
            
            fig = apply_theme_to_plot(fig)
            fig.update_traces(
                texttemplate='₹%{text:.2f}L',
                textposition='outside',
                marker_color=colors['primary']
            )
            
            st.plotly_chart(fig, use_container_width=True, key="quarter_breakdown")
            
            # Display metrics table
            st.dataframe(
                quarter_metrics.style.format({
                    'Total Amount (Lakhs)': '₹{:.2f}L'
                }),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error in Quarter Analysis: {str(e)}")
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_trends():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">📈 Monthly Pipeline Trend</h2>
            </div>
    """, unsafe_allow_html=True)
    
    try:
        if 'Expected Close Date' in filtered_df.columns:
            filtered_df['Date'] = pd.to_datetime(filtered_df['Expected Close Date'], errors='coerce')
            monthly_metrics = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).agg({
                'Amount': 'sum',
                'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
            }).reset_index()
            
            monthly_metrics['Date'] = monthly_metrics['Date'].astype(str)
            monthly_metrics['Amount'] = monthly_metrics['Amount'] / 100000
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=monthly_metrics['Date'],
                y=monthly_metrics['Amount'],
                name='Pipeline',
                line=dict(color=colors['primary'], width=2),
                mode='lines+markers'
            ))
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                title='Monthly Pipeline Trend',
                xaxis_title='Month',
                yaxis_title='Amount (Lakhs)',
                showlegend=True
            )
            
            fig.update_traces(texttemplate='₹%{y:.2f}L', textposition='top center')
            
            st.plotly_chart(fig, use_container_width=True, key="monthly_trend")
            
            st.dataframe(
                monthly_metrics.style.format({
                    'Amount': '₹{:.2f}L'
                }),
                use_container_width=True
            )
        else:
            st.info("Expected Close Date column is required for monthly trend analysis.")
    except Exception as e:
        st.error(f"Error in Monthly Trend Analysis: {str(e)}")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Practice-wise Trend
    if 'Practice' in filtered_df.columns and 'Expected Close Date' in filtered_df.columns:
        st.markdown("""
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">📊 Practice-wise Trend</h2>
                </div>
        """, unsafe_allow_html=True)
        
        try:
            # Group by practice and month
            filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
            practice_monthly = filtered_df.groupby(['Practice', 'Month']).agg({
                'Amount': 'sum'
            }).reset_index()
            
            practice_monthly['Month'] = practice_monthly['Month'].astype(str)
            practice_monthly['Amount'] = practice_monthly['Amount'] / 100000
            
            fig = px.line(
                practice_monthly,
                x='Month',
                y='Amount',
                color='Practice',
                title='Practice-wise Monthly Trend',
                labels={'Amount': 'Amount (Lakhs)', 'Month': 'Month', 'Practice': 'Practice'},
                line_shape='spline'
            )
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Amount (Lakhs)',
                legend_title='Practice',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True, key="practice_trend")
            
        except Exception as e:
            st.error(f"Error in Practice Trend Analysis: {str(e)}")
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_funnel():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🔄 Sales Stage Funnel</h2>
            </div>
    """, unsafe_allow_html=True)
    
    try:
        if 'Sales Stage' in filtered_df.columns:
            stage_metrics = filtered_df.groupby('Sales Stage').agg({
                'Amount': 'sum',
            }).reset_index()
            
            if 'Opportunity Number' in filtered_df.columns:
                opp_counts = filtered_df.groupby('Sales Stage')['Opportunity Number'].count().reset_index()
                stage_metrics = stage_metrics.merge(opp_counts, on='Sales Stage')
            else:
                stage_metrics['Opportunity Count'] = filtered_df.groupby('Sales Stage').size().values
            
            stage_metrics['Amount'] = stage_metrics['Amount'] / 100000
            
            # Sort by typical sales stages
            stage_order = [
                'Prospect', 'Lead', 'Initial Contact', 'Qualified', 'Proposal', 
                'Negotiation', 'Closed Won', 'Won', 'Closed Lost', 'Lost'
            ]
            
            # Create a numerical order for known stages
            stage_metrics['order'] = stage_metrics['Sales Stage'].apply(
                lambda x: stage_order.index(x) if x in stage_order else 999
            )
            
            # Sort by that order
            stage_metrics = stage_metrics.sort_values('order')
            
            fig = go.Figure(go.Funnel(
                y=stage_metrics['Sales Stage'],
                x=stage_metrics['Amount'],
                textinfo='value+percent initial',
                texttemplate='₹%{value:.2f}L',
                textposition='inside',
                marker=dict(color=colors['primary'])
            ))
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                title='Sales Stage Funnel',
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sales_funnel")
            
            # Display metrics table
            display_cols = ['Sales Stage', 'Amount']
            if 'Opportunity Number' in stage_metrics.columns:
                display_cols.append('Opportunity Number')
            elif 'Opportunity Count' in stage_metrics.columns:
                display_cols.append('Opportunity Count')
                
            st.dataframe(
                stage_metrics[display_cols].style.format({
                    'Amount': '₹{:.2f}L'
                }),
                use_container_width=True
            )
        else:
            st.info("Sales Stage column is required for funnel analysis.")
    except Exception as e:
        st.error(f"Error in Sales Funnel Analysis: {str(e)}")
        
    st.markdown("</div>", unsafe_allow_html=True)

def show_strategy():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🎯 Strategy View</h2>
            </div>
    """, unsafe_allow_html=True)
    
    try:
        if 'Amount' in filtered_df.columns and 'Probability' in filtered_df.columns:
            fig = px.scatter(
                filtered_df,
                x='Amount',
                y='Probability',
                size='Amount',
                color='Practice' if 'Practice' in filtered_df.columns else None,
                hover_data=['Organization Name'] if 'Organization Name' in filtered_df.columns else None,
                title='Deal Value vs Probability',
                labels={
                    'Amount': 'Deal Value',
                    'Probability': 'Probability (%)',
                    'Practice': 'Practice'
                }
            )
            
            fig = apply_theme_to_plot(fig)
            
            st.plotly_chart(fig, use_container_width=True, key="strategy_view")
            
            # Strategy metrics
            if 'Practice' in filtered_df.columns:
                strategy_metrics = filtered_df.groupby('Practice').agg({
                    'Amount': 'sum',
                    'Probability': 'mean'
                }).reset_index()
                
                # Add count if opportunity number exists
                if 'Opportunity Number' in filtered_df.columns:
                    opp_counts = filtered_df.groupby('Practice')['Opportunity Number'].count().reset_index()
                    strategy_metrics = strategy_metrics.merge(opp_counts, on='Practice')
                else:
                    strategy_metrics['Deal Count'] = filtered_df.groupby('Practice').size().values
                
                strategy_metrics['Amount'] = strategy_metrics['Amount'] / 100000
                
                # Format table
                format_dict = {
                    'Amount': '₹{:.2f}L',
                    'Probability': '{:.1f}%'
                }
                
                st.dataframe(
                    strategy_metrics.style.format(format_dict),
                    use_container_width=True
                )
            else:
                st.info("Practice column is recommended for strategy view analysis.")
        else:
            st.info("Amount and Probability columns are required for strategy view.")
    except Exception as e:
        st.error(f"Error in Strategy View Analysis: {str(e)}")
        
    st.markdown("</div>", unsafe_allow_html=True)

def show_leaderboard():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🏆 Sales Leaderboard</h2>
            </div>
    """, unsafe_allow_html=True)
    
    # Check which owner field is available
    owner_field = None
    for field in ['Sales Owner', 'Owner', 'Opportunities Assigned to', 'Assigned To']:
        if field in filtered_df.columns:
            owner_field = field
            break
    
    if owner_field:
        try:
            # Calculate metrics by owner
            owner_metrics = filtered_df.groupby(owner_field).agg({
                'Amount': 'sum'
            }).reset_index()
            
            # Add won deals if Sales Stage exists
            if 'Sales Stage' in filtered_df.columns:
                won_deals = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]
                if not won_deals.empty:
                    won_by_owner = won_deals.groupby(owner_field)['Amount'].sum().reset_index()
                    won_by_owner.columns = [owner_field, 'Won Amount']
                    owner_metrics = owner_metrics.merge(won_by_owner, on=owner_field, how='left')
                    owner_metrics['Won Amount'] = owner_metrics['Won Amount'].fillna(0)
                    owner_metrics['Win Rate'] = (owner_metrics['Won Amount'] / owner_metrics['Amount'] * 100).round(1)
            
            # Convert to lakhs
            owner_metrics['Amount'] = owner_metrics['Amount'] / 100000
            if 'Won Amount' in owner_metrics.columns:
                owner_metrics['Won Amount'] = owner_metrics['Won Amount'] / 100000
            
            # Sort by total pipeline
            owner_metrics = owner_metrics.sort_values('Amount', ascending=False)
            
            # Create visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=owner_metrics[owner_field],
                x=owner_metrics['Amount'],
                name='Total Pipeline',
                orientation='h',
                marker_color=colors['primary']
            ))
            
            if 'Won Amount' in owner_metrics.columns:
                fig.add_trace(go.Bar(
                    y=owner_metrics[owner_field],
                    x=owner_metrics['Won Amount'],
                    name='Won Amount',
                    orientation='h',
                    marker_color=colors['success']
                ))
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                title=f'Performance by {owner_field}',
                barmode='overlay',
                xaxis_title='Amount (Lakhs)',
                yaxis_title=owner_field,
                showlegend=True
            )
            
            fig.update_traces(texttemplate='₹%{x:.2f}L', textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True, key="leaderboard")
            
            # Format the dataframe
            format_dict = {'Amount': '₹{:.2f}L'}
            if 'Won Amount' in owner_metrics.columns:
                format_dict['Won Amount'] = '₹{:.2f}L'
            if 'Win Rate' in owner_metrics.columns:
                format_dict['Win Rate'] = '{:.1f}%'
                
            st.dataframe(
                owner_metrics.style.format(format_dict),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error in Leaderboard Analysis: {str(e)}")
    else:
        st.info("Sales Owner or similar field is required for leaderboard analysis.")
        
    st.markdown("</div>", unsafe_allow_html=True)

def show_geo():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🌍 Geography View</h2>
            </div>
    """, unsafe_allow_html=True)
    
    # Check which geography field is available
    geo_field = None
    for field in ['Region', 'Country', 'Geography', 'Location']:
        if field in filtered_df.columns:
            geo_field = field
            break
    
    if geo_field:
        try:
            # Calculate metrics by geography
            geo_metrics = filtered_df.groupby(geo_field).agg({
                'Amount': 'sum'
            }).reset_index()
            
            # Add opportunity count if field exists
            if 'Opportunity Number' in filtered_df.columns:
                opp_counts = filtered_df.groupby(geo_field)['Opportunity Number'].count().reset_index()
                geo_metrics = geo_metrics.merge(opp_counts, on=geo_field)
            else:
                geo_metrics['Deal Count'] = filtered_df.groupby(geo_field).size().values
            
            # Convert to lakhs
            geo_metrics['Amount'] = geo_metrics['Amount'] / 100000
            
            # Create choropleth if Country/Region, otherwise bar chart
            if geo_field in ['Country', 'Geography']:
                try:
                    fig = px.choropleth(
                        geo_metrics,
                        locations=geo_field,
                        locationmode='country names',
                        color='Amount',
                        hover_data=['Deal Count'] if 'Deal Count' in geo_metrics.columns else None,
                        title=f'Amount by {geo_field}',
                        color_continuous_scale='Viridis'
                    )
                    
                    fig = apply_theme_to_plot(fig)
                    fig.update_layout(
                        geo=dict(
                            showframe=False,
                            showcoastlines=True,
                            projection_type='equirectangular'
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="geo_map")
                except:
                    # Fallback to bar chart if choropleth fails
                    create_geo_bar_chart(geo_metrics, geo_field)
            else:
                create_geo_bar_chart(geo_metrics, geo_field)
                
            # Format the dataframe
            format_dict = {'Amount': '₹{:.2f}L'}
            
            st.dataframe(
                geo_metrics.style.format(format_dict),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error in Geography Analysis: {str(e)}")
    else:
        st.info("Region, Country, Geography, or similar field is required for geography analysis.")
        
    st.markdown("</div>", unsafe_allow_html=True)

def create_geo_bar_chart(geo_metrics, geo_field):
    # Create bar chart for regions
    fig = px.bar(
        geo_metrics.sort_values('Amount', ascending=False),
        x=geo_field,
        y='Amount',
        title=f'Amount by {geo_field}',
        text='Amount',
        color='Amount',
        color_continuous_scale='Viridis'
    )
    
    fig = apply_theme_to_plot(fig)
    fig.update_traces(
        texttemplate='₹%{text:.2f}L',
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True, key="geo_bar")

def show_detailed():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">🧾 Detailed Opportunities</h2>
            </div>
    """, unsafe_allow_html=True)
    
    try:
        # Add weighted revenue if probability exists
        if 'Amount' in filtered_df.columns and 'Probability' in filtered_df.columns:
            filtered_df['Weighted Revenue'] = filtered_df['Amount'] * filtered_df['Probability'] / 100
        
        # Define potential columns for display
        potential_columns = [
            'Organization Name', 'Opportunity Number', 'Amount', 'Probability', 
            'Weighted Revenue', 'Sales Stage', 'Expected Close Date', 'Quarter',
            'Practice', 'Sales Owner', 'Owner', 'Opportunities Assigned to', 
            'Region', 'Country', 'Geography', 'Hunting/Farming', 'Industry'
        ]
        
        # Filter columns that exist in the dataframe
        columns_to_show = [col for col in potential_columns if col in filtered_df.columns]
        
        # Ensure we have at least one column
        if not columns_to_show:
            columns_to_show = filtered_df.columns.tolist()
        
        # Search filter
        search_query = st.text_input("🔍 Search opportunities", placeholder="Type to search...")
        
        # Filter data based on search
        if search_query:
            search_mask = pd.Series(False, index=filtered_df.index)
            for col in filtered_df.columns:
                if filtered_df[col].dtype == object:  # Only search text columns
                    search_mask = search_mask | filtered_df[col].astype(str).str.contains(search_query, case=False, na=False)
            filtered_df = filtered_df[search_mask]
        
        # Add filters for key columns
        filter_cols = st.columns(3)
        
        # Dynamic filters based on available columns
        for i, filter_col in enumerate(['Practice', 'Sales Stage', 'Quarter']):
            if filter_col in filtered_df.columns:
                with filter_cols[i % 3]:
                    selected_values = st.multiselect(
                        f"Filter by {filter_col}",
                        options=safe_sort_unique(filtered_df[filter_col]),
                        key=f"filter_{filter_col}"
                    )
                    if selected_values:
                        filtered_df = filtered_df[filtered_df[filter_col].astype(str).isin(selected_values)]
        
        # Format Amount and Weighted Revenue to lakhs for display
        display_df = filtered_df.copy()
        if 'Amount' in display_df.columns:
            display_df['Amount'] = display_df['Amount'] / 100000
        if 'Weighted Revenue' in display_df.columns:
            display_df['Weighted Revenue'] = display_df['Weighted Revenue'] / 100000
        
        # Display the filtered dataframe
        st.dataframe(display_df[columns_to_show], use_container_width=True)
        
        # Summary metrics
        metric_cols = st.columns(3)
        
        with metric_cols[0]:
            if 'Amount' in filtered_df.columns:
                st.metric(
                    "Total Amount",
                    format_lakhs(filtered_df['Amount'].sum()),
                    delta=None
                )
        
        with metric_cols[1]:
            if 'Weighted Revenue' in filtered_df.columns:
                st.metric(
                    "Weighted Revenue",
                    format_lakhs(filtered_df['Weighted Revenue'].sum()),
                    delta=None
                )
                
        with metric_cols[2]:
            st.metric(
                "Number of Deals",
                f"{len(filtered_df):,}",
                delta=None
            )
            
        # Export options
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            # Export to CSV
            csv = display_df[columns_to_show].to_csv(index=False)
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name="opportunities.csv",
                mime="text/csv"
            )
        
        with exp_col2:
            # Export to Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                display_df[columns_to_show].to_excel(writer, index=False, sheet_name='Opportunities')
            buffer.seek(0)
            
            st.download_button(
                label="📊 Export to Excel",
                data=buffer,
                file_name="opportunities.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        st.error(f"Error in Detailed View: {str(e)}")
        
    st.markdown("</div>", unsafe_allow_html=True)

def show_editor():
    filtered_df = st.session_state.df.copy()
    
    st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <h2 class="card-title">✏️ Data Editor</h2>
            </div>
    """, unsafe_allow_html=True)
    
    try:
        # Define column configurations
        column_configs = {}
        
        # Setup column types for numeric columns
        for col in filtered_df.columns:
            if filtered_df[col].dtype in [np.float64, np.int64]:
                if col == 'Amount':
                    column_configs[col] = st.column_config.NumberColumn(
                        "Amount",
                        format="₹%.2f",
                        min_value=0
                    )
                elif col == 'Probability':
                    column_configs[col] = st.column_config.NumberColumn(
                        "Probability",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100
                    )
            elif filtered_df[col].dtype == np.dtype('datetime64[ns]'):
                column_configs[col] = st.column_config.DateColumn(
                    col,
                    format="DD-MM-YYYY"
                )
        
        # Use data editor
        edited_df = st.data_editor(
            filtered_df,
            column_config=column_configs,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor"
        )
        
        # Export options
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            # Export to CSV
            csv = edited_df.to_csv(index=False)
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name="edited_data.csv",
                mime="text/csv"
            )
        
        with exp_col2:
            # Export to Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                edited_df.to_excel(writer, index=False, sheet_name='Edited Data')
            buffer.seek(0)
            
            st.download_button(
                label="📊 Export to Excel",
                data=buffer,
                file_name="edited_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Show differences
        if not edited_df.equals(filtered_df):
            st.success("Changes detected! Use the export buttons to save your edited data.")
            
    except Exception as e:
        st.error(f"Error in Data Editor: {str(e)}")
        
    st.markdown("</div>", unsafe_allow_html=True)

# Run the main application
if __name__ == "__main__":
    main() 
