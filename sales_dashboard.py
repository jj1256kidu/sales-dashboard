import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'background': '#1a1a1a',
            'text': '#ffffff',
            'card_bg': '#2d2d2d',
            'border': '#404040',
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'hover': '#3d3d3d'
        }
    else:
        return {
            'background': '#f8fafc',
            'text': '#1e293b',
            'card_bg': '#ffffff',
            'border': '#e2e8f0',
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'hover': '#f1f5f9'
        }

# Set page config with full page mode
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar
)

# Get current theme colors
colors = get_theme_colors()

# Custom CSS for modern styling
st.markdown(f"""
    <style>
    /* Main Layout */
    .main {{
        padding: 0;
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    
    /* Sticky Navigation */
    .stTabs [data-baseweb="tab-list"] {{
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: {colors['background']};
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: transparent;
        padding: 0.5rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        white-space: pre-wrap;
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 0 1.5rem;
        color: {colors['secondary']};
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid {colors['border']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 200px;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        background-color: {colors['hover']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {colors['primary']};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        border: none;
        font-weight: 600;
    }}
    
    /* Tab Content Styling */
    .stTabs [data-baseweb="tab-panel"] {{
        padding: 2rem 0;
    }}
    
    /* Section Headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    .section-header h3 {{
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['text']};
    }}
    
    /* Detailed View Table */
    .stDataFrame {{
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
        margin-top: 1rem;
    }}
    
    .stDataFrame thead th {{
        background-color: {colors['hover']};
        color: {colors['text']};
        font-weight: 600;
        padding: 1rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    .stDataFrame tbody td {{
        padding: 1rem;
        border-bottom: 1px solid {colors['border']};
        color: {colors['text']};
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: {colors['hover']};
    }}
    
    /* Table Filters */
    .table-filters {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }}
    
    .table-filter-item {{
        flex: 1;
        min-width: 200px;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .stTabs [data-baseweb="tab"] {{
            min-width: 100%;
            margin-bottom: 0.5rem;
        }}
        
        .table-filters {{
            flex-direction: column;
        }}
        
        .table-filter-item {{
            width: 100%;
        }}
    }}
    
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    </style>
""", unsafe_allow_html=True)

# Title and Header with theme toggle
col1, col2 = st.columns([6, 1])
with col1:
    st.title("📊 Sales Dashboard")
with col2:
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        key='theme_selector'
    )
    st.session_state.theme = theme.lower()

# Data Input Section
st.markdown("""
    <div class="section-header">
        <h3>📁 Data Input</h3>
    </div>
""", unsafe_allow_html=True)

input_method = st.radio("Choose data input method:", ["Excel File", "Google Sheet URL"])

df = None
if input_method == "Excel File":
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Raw_Data')
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
else:
    sheet_url = st.text_input("Paste Google Sheet URL")
    if sheet_url:
        try:
            csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(csv_url)
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Google Sheet: {str(e)}")

if df is not None:
    # Sidebar Filters
    with st.sidebar:
        st.markdown("""
            <div class="section-header">
                <h3>⚙️ Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Sales Target Input
        sales_target = st.number_input(
            "Enter Sales Target (in Lakhs)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )
        
        st.markdown("""
            <div class="section-header">
                <h3>🔍 Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Practice filter
        practices = ['All'] + safe_sort_unique(df['Practice'])
        selected_practice = st.selectbox("Practice", practices)
        
        # Quarter filter
        quarters = ['All'] + safe_sort_unique(df['Quarter'])
        selected_quarter = st.selectbox("Quarter", quarters)
        
        # Hunting/Farming filter
        deal_types = ['All'] + safe_sort_unique(df['Hunting/Farming'])
        selected_deal_type = st.selectbox("Hunting/Farming", deal_types)
        
        # Sales Owner filter (if available)
        if 'Sales Owner' in df.columns:
            sales_owners = ['All'] + safe_sort_unique(df['Sales Owner'])
            selected_sales_owner = st.selectbox("Sales Owner", sales_owners)
        
        # Tech Owner filter (if available)
        if 'Tech Owner' in df.columns:
            tech_owners = ['All'] + safe_sort_unique(df['Tech Owner'])
            selected_tech_owner = st.selectbox("Tech Owner", tech_owners)

    # Apply filters
    filtered_df = df.copy()
    if selected_practice != 'All':
        filtered_df = filtered_df[filtered_df['Practice'].astype(str) == selected_practice]
    if selected_quarter != 'All':
        filtered_df = filtered_df[filtered_df['Quarter'].astype(str) == selected_quarter]
    if selected_deal_type != 'All':
        filtered_df = filtered_df[filtered_df['Hunting/Farming'].astype(str) == selected_deal_type]
    if 'Sales Owner' in df.columns and selected_sales_owner != 'All':
        filtered_df = filtered_df[filtered_df['Sales Owner'].astype(str) == selected_sales_owner]
    if 'Tech Owner' in df.columns and selected_tech_owner != 'All':
        filtered_df = filtered_df[filtered_df['Tech Owner'].astype(str) == selected_tech_owner]

    # Calculate KPIs (in Lakhs)
    current_pipeline = filtered_df['Amount'].sum() / 100000
    amount = filtered_df['Amount'].sum() / 100000
    closed_won = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Create tabs with improved styling
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", 
        "👤 Sales Leaderboard", 
        "📈 Trend View", 
        "🔄 Funnel View", 
        "🎯 Strategy View", 
        "🌍 Geo View", 
        "🧾 Detailed View"
    ])

    # Rest of the code remains the same...
    # [Previous tab content code remains unchanged]

else:
    st.info("Please upload data to view the dashboard.")
