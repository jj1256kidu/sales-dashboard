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
            'sidebar_text': '#F8FAFC'    # Bright sidebar text
        }
    else:
        return {
            'background': '#F2F6FF',  # Soft pastel background
            'text': '#1A1A1A',        # Dark text
            'card_bg': '#FFFFFF',     # White cards
            'border': '#E5E7EB',      # Light border
            'primary': '#60A5FA',     # Sky blue accent
            'secondary': '#6B7280',   # Muted gray
            'success': '#3DD598',     # Mint green
            'hover': '#F3F4F6',       # Hover state
            'header': '#FFFFFF',      # Header background
            'metric_bg': '#FFFFFF',   # Metric card background
            'metric_border': '#E5E7EB', # Metric card border
            'accent1': '#A78BFA',     # Lavender accent
            'accent2': '#3DD598',     # Mint green accent
            'warning': '#F59E0B',     # Amber warning
            'error': '#EF4444',       # Red error
            'input_bg': '#FFFFFF',    # Input background
            'input_border': '#E5E7EB', # Input border
            'input_text': '#1A1A1A',  # Input text
            'select_bg': '#FFFFFF',   # Select background
            'select_border': '#E5E7EB', # Select border
            'select_text': '#1A1A1A', # Select text
            'radio_bg': '#FFFFFF',    # Radio background
            'radio_border': '#E5E7EB', # Radio border
            'radio_text': '#1A1A1A',  # Radio text
            'table_header': '#F8FAFC', # Table header background
            'table_row': '#FFFFFF',   # Table row background
            'table_hover': '#F3F4F6', # Table row hover
            'table_border': '#E5E7EB', # Table border
            'table_text': '#1A1A1A',  # Table text
            'sidebar_bg': '#FFFFFF',  # Sidebar background
            'sidebar_text': '#1A1A1A' # Sidebar text
        }

# Set page config with full page mode and theme
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation if not exists
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'data_input'

# Create the vertical sidebar
with st.sidebar:
    # Navigation options with icons
    pages = {
        "📁 Data Input": "data_input",
        "🌍 Overview": "overview",
        "📈 Trends": "trends",
        "🔄 Funnel": "funnel",
        "🎯 Strategy": "strategy",
        "👥 Leaderboard": "leaderboard",
        "🌐 Geography": "geo",
        "🧾 Detailed View": "detailed",
        "✏️ Editor": "editor"
    }
    
    st.markdown("## 📊 Navigation")
    selected_page = st.radio("Go to", list(pages.keys()))
    
    # Save selected page
    st.session_state.current_view = pages[selected_page]
    
    # Theme selector at the bottom of sidebar
    st.markdown("<div style='margin-top: auto; padding: 1rem;'>", unsafe_allow_html=True)
    theme_options = {
        "Dark": "dark",
        "Light": "light"
    }
    selected_theme = st.selectbox(
        "Theme",
        options=list(theme_options.keys()),
        index=0 if st.session_state.theme == 'dark' else 1,
        key='theme_selector_sidebar'
    )
    
    if theme_options[selected_theme] != st.session_state.theme:
        st.session_state.theme = theme_options[selected_theme]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
            family="Inter",
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

# Custom CSS for modern corporate styling
st.markdown(f"""
    <style>
    /* Base Theme */
    :root {{
        --background-color: {colors['background']};
        --text-color: {colors['text']};
        --card-bg-color: {colors['card_bg']};
        --border-color: {colors['border']};
        --primary-color: {colors['primary']};
    }}
    
    /* Main Layout */
    .main {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }}
    
    .stApp {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }}
    
    /* Streamlit Elements Override */
    div[data-testid="stToolbar"] {{
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
    }}
    
    /* Improve text visibility in dark theme */
    .element-container, .stMarkdown, .stText {{
        color: var(--text-color) !important;
    }}
    
    /* Make metric values more visible */
    [data-testid="stMetricValue"] {{
        color: {colors['primary']} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: var(--text-color) !important;
    }}
    
    /* Improve table text visibility */
    .dataframe {{
        color: var(--text-color) !important;
    }}
    
    .dataframe th {{
        background-color: {colors['card_bg']} !important;
        color: var(--text-color) !important;
        font-weight: 600 !important;
    }}
    
    .dataframe td {{
        color: var(--text-color) !important;
    }}
    
    /* Improve select box text visibility */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: var(--card-bg-color) !important;
        border-color: var(--border-color) !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: var(--text-color) !important;
    }}
    
    /* Improve button text visibility */
    .stButton button {{
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }}
    
    .stButton button:hover {{
        border-color: var(--primary-color) !important;
        color: var(--primary-color) !important;
    }}
    
    /* Improve checkbox text visibility */
    .stCheckbox label {{
        color: var(--text-color) !important;
    }}
    
    /* Improve radio button text visibility */
    .stRadio label {{
        color: var(--text-color) !important;
    }}
    
    /* Improve text input visibility */
    .stTextInput input {{
        background-color: var(--card-bg-color) !important;
        border-color: var(--border-color) !important;
        color: var(--text-color) !important;
    }}
    
    /* Improve number input visibility */
    .stNumberInput input {{
        background-color: var(--card-bg-color) !important;
        border-color: var(--border-color) !important;
        color: var(--text-color) !important;
    }}
    
    /* Main Layout */
    .main {{
        padding: 0;
        background-color: {colors['background']} !important;
        color: {colors['text']} !important;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header Styling */
    .stApp header {{
        background-color: {colors['header']};
        border-bottom: 1px solid {colors['border']};
        padding: 1rem 2rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* Title Styling */
    .stTitle {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: {colors['text']};
        margin-bottom: 2rem;
        letter-spacing: -0.025em;
    }}
    
    /* Navigation Menu */
    .nav-menu {{
        background-color: {colors['header']};
        padding: 1rem;
        border-bottom: 1px solid {colors['border']};
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .nav-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    .nav-group {{
        flex: 1;
        min-width: 200px;
    }}
    
    .nav-item {{
        display: block;
        padding: 1rem;
        background-color: {colors['card_bg']};
        color: {colors['text']};
        text-decoration: none;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    .nav-item:hover {{
        background-color: {colors['hover']};
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.025em;
    }}
    
    /* Metric Cards */
    .stMetric {{
        background-color: {colors['metric_bg']};
        border: 1px solid {colors['metric_border']};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['primary']};
    }}
    
    .stMetric [data-testid="stMetricLabel"] {{
        font-size: 0.875rem;
        color: {colors['secondary']};
    }}
    
    /* Data Editor Styling */
    .data-editor {{
        background-color: {colors['card_bg']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* Filter Panel */
    .filter-panel {{
        position: fixed;
        top: 0;
        right: 0;
        width: 300px;
        height: 100vh;
        background-color: {colors['card_bg']};
        border-left: 1px solid {colors['border']};
        padding: 1.5rem;
        overflow-y: auto;
        z-index: 1000;
        box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
    }}
    
    .filter-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 1001;
        background-color: {colors['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    .filter-toggle:hover {{
        opacity: 0.9;
    }}
    
    .filter-section {{
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    .filter-section:last-child {{
        border-bottom: none;
    }}
    
    .filter-section h4 {{
        margin: 0 0 1rem 0;
        color: {colors['text']};
        font-size: 1rem;
        font-weight: 600;
    }}
    
    .filter-actions {{
        position: sticky;
        bottom: 0;
        background-color: {colors['card_bg']};
        padding: 1rem 0;
        border-top: 1px solid {colors['border']};
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
    }}
    
    .filter-actions button {{
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .filter-actions .apply {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    .filter-actions .reset {{
        background-color: {colors['secondary']};
        color: white;
    }}
    
    .filter-actions button:hover {{
        opacity: 0.9;
    }}
    
    /* Full Page Layout */
    .full-page {{
        padding: 2rem;
        max-width: 1400px;
        margin: 0 auto;
        background-color: {colors['background']};
    }}
    
    .page-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }}
    
    .page-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['text']};
        margin: 0;
    }}
    
    .page-actions {{
        display: flex;
        gap: 1rem;
    }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['border']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['secondary']};
    }}
    
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    
    /* Vertical Sidebar Styling */
    .sidebar .sidebar-content {{
        background-color: {colors['card_bg']} !important;
        padding: 1rem 0.5rem !important;
    }}
    
    .sidebar-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        margin: 0.5rem auto;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
    }}
    
    .sidebar-icon:hover {{
        background-color: {colors['hover']};
        transform: translateY(-2px);
    }}
    
    .sidebar-icon.active {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    .sidebar-icon::after {{
        content: attr(data-tooltip);
        position: absolute;
        left: 100%;
        top: 50%;
        transform: translateY(-50%);
        background-color: {colors['card_bg']};
        color: {colors['text']};
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-size: 0.875rem;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }}
    
    .sidebar-icon:hover::after {{
        opacity: 1;
        visibility: visible;
    }}
    
    /* Adjust main content area */
    .main .block-container {{
        padding-left: 5rem !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Render the correct page based on selection
if st.session_state.current_view == "data_input":
    st.title("📁 Data Input")
    input_method = st.radio("Choose data input method:", ["Excel File", "Google Sheet URL"])
    
    df = None
    if input_method == "Excel File":
        uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file, sheet_name='Raw_Data')
                if 'Amount' in df.columns:
                    df['Amount'] = df['Amount'].apply(safe_float)
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
            except Exception as e:
                st.error(f"Error reading Google Sheet: {str(e)}")
    
    if df is not None:
        st.success("Data loaded successfully!")
        st.dataframe(df.head(), use_container_width=True)
else:
    # Check if data is loaded
    if 'df' not in locals() or df is None:
        st.warning("Please go to the Data Input page and upload your data first.")
    else:
        # Initialize filtered_df with the original dataframe
        filtered_df = df.copy()
        
        # Show the selected view
        view_functions = {
            'overview': show_overview,
            'trends': show_trends,
            'funnel': show_funnel,
            'strategy': show_strategy,
            'leaderboard': show_leaderboard,
            'geo': show_geo,
            'detailed': show_detailed,
            'editor': show_editor
        }
        
        if st.session_state.current_view in view_functions:
            view_functions[st.session_state.current_view]()
        else:
            st.info("Please select a view from the sidebar.")

# Title and Theme Selection
col1, col2 = st.columns([6, 1])
with col1:
    st.title("📊 Sales Dashboard")
with col2:
    # Theme selector with proper state management
    theme_options = {
        "Dark": "dark",
        "Light": "light"
    }
    selected_theme = st.selectbox(
        "Theme",
        options=list(theme_options.keys()),
        index=0 if st.session_state.theme == 'dark' else 1,
        key='theme_selector_main'
    )
    
    # Update theme state if changed
    new_theme = theme_options[selected_theme]
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

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
            family="Inter",
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

# Initialize session state for navigation and filters
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'overview'
if 'filters' not in st.session_state:
    st.session_state.filters = {}

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
        except Exception as e:
            st.error(f"Error reading Google Sheet: {str(e)}")

if df is not None:
    # Initialize filtered_df with the original dataframe
    filtered_df = df.copy()
    
    # Define view functions first
    def show_overview():
        if not st.session_state.dashboard_config['show_kpis']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Key Performance Indicators</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Dynamic KPI display
        num_cols = min(3, len(filtered_df.columns))
        kpi_cols = st.columns(num_cols)
        
        # Total Amount
        with kpi_cols[0]:
            total_amount = filtered_df['Amount'].sum() / 100000
            st.metric(
                "Total Amount",
                format_lakhs(total_amount * 100000),
                delta=None,
                delta_color="normal"
            )
        
        # Closed Won Amount
        with kpi_cols[1]:
            won_amount = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
            st.metric(
                "Closed Won",
                format_lakhs(won_amount * 100000),
                delta=None,
                delta_color="normal"
            )
        
        if st.session_state.dashboard_config['show_financial_year']:
            st.markdown("""
                <div class="section-header">
                    <h3>💰 Financial Year Analysis</h3>
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
        
        if st.session_state.dashboard_config['show_quarter_breakdown']:
            st.markdown("""
                <div class="section-header">
                    <h3>🏢 Quarter-wise Breakdown</h3>
                </div>
            """, unsafe_allow_html=True)
            
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
        
        if st.session_state.dashboard_config['show_hunting_farming'] and 'Hunting/Farming' in filtered_df.columns:
            st.markdown("""
                <div class="section-header">
                    <h3>🎯 Hunting vs Farming Distribution</h3>
                </div>
            """, unsafe_allow_html=True)
            
            hunting_farming = filtered_df.groupby('Hunting/Farming')['Amount'].sum().reset_index()
            total_amount = hunting_farming['Amount'].sum()
            
            if total_amount > 0:
                hunting_farming['Percentage'] = (hunting_farming['Amount'] / total_amount * 100).round(1)
                
                fig = go.Figure(data=[go.Pie(
                    labels=hunting_farming['Hunting/Farming'],
                    values=hunting_farming['Amount'] / 100000,
                    hole=.4,
                    textinfo='label+percent',
                    textposition='outside',
                    marker=dict(
                        colors=[colors['accent1'], colors['accent2']],
                        line=dict(color=colors['card_bg'], width=2)
                    )
                )])
                
                fig = apply_theme_to_plot(fig)
                fig.update_layout(
                    title="Distribution of Hunting vs Farming (in Lakhs)",
                    showlegend=True,
                    annotations=[dict(
                        text='Hunting/Farming',
                        x=0.5,
                        y=0.5,
                        font_size=20,
                        showarrow=False,
                        font_color=colors['text']
                    )],
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, key="hunting_farming")
                
                # Display metrics table
                hunting_farming_metrics = hunting_farming.copy()
                hunting_farming_metrics['Amount'] = hunting_farming_metrics['Amount'] / 100000
                
                table_html = f"""
                <div class="custom-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Amount (Lakhs)</th>
                                <th>Percentage</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                
                for _, row in hunting_farming_metrics.iterrows():
                    table_html += f"""
                            <tr>
                                <td>{row['Hunting/Farming']}</td>
                                <td>₹{row['Amount']:.2f}L</td>
                                <td>{row['Percentage']:.1f}%</td>
                            </tr>
                    """
                
                table_html += """
                        </tbody>
                    </table>
                </div>
                """
                
                st.markdown(table_html, unsafe_allow_html=True)

    def show_trends():
        if not st.session_state.dashboard_config['show_monthly_trend']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>📈 Monthly Pipeline Trend</h3>
            </div>
        """, unsafe_allow_html=True)
        
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

    def show_funnel():
        if not st.session_state.dashboard_config['show_sales_funnel']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🔄 Sales Stage Funnel</h3>
            </div>
        """, unsafe_allow_html=True)
        
        stage_metrics = filtered_df.groupby('Sales Stage').agg({
            'Amount': 'sum',
            'Opportunity Number': 'count'
        }).reset_index()
        
        stage_metrics['Amount'] = stage_metrics['Amount'] / 100000
        
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
        
        st.dataframe(
            stage_metrics.style.format({
                'Amount': '₹{:.2f}L'
            }),
            use_container_width=True
        )

    def show_strategy():
        if not st.session_state.dashboard_config['show_strategy_view']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Strategy View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        fig = px.scatter(
            filtered_df,
            x='Amount',
            y='Probability',
            size='Amount',
            color='Practice',
            hover_data=['Organization Name', 'Sales Stage'],
            title='Deal Value vs Probability by Practice',
            labels={
                'Amount': 'Deal Value (Lakhs)',
                'Probability': 'Probability (%)',
                'Practice': 'Practice'
            }
        )
        
        fig = apply_theme_to_plot(fig)
        fig.update_traces(
            texttemplate='₹%{y:.2f}L',
            textposition='top center'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="strategy_view")
        
        strategy_metrics = filtered_df.groupby('Practice').agg({
            'Amount': 'sum',
            'Probability': 'mean',
            'Opportunity Number': 'count'
        }).reset_index()
        
        strategy_metrics['Amount'] = strategy_metrics['Amount'] / 100000
        
        st.dataframe(
            strategy_metrics.style.format({
                'Amount': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

    def show_leaderboard():
        if not st.session_state.dashboard_config['show_leaderboard']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🏆 Sales Leaderboard</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if 'Sales Owner' in filtered_df.columns:
            owner_metrics = filtered_df.groupby('Sales Owner').agg({
                'Amount': 'sum',
                'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
            }).reset_index()
            
            owner_metrics.columns = ['Sales Owner', 'Total Pipeline', 'Closed Won']
            owner_metrics['Total Pipeline'] = owner_metrics['Total Pipeline'] / 100000
            owner_metrics['Closed Won'] = owner_metrics['Closed Won'] / 100000
            owner_metrics['Win Rate'] = (owner_metrics['Closed Won'] / owner_metrics['Total Pipeline'] * 100).round(1)
            
            owner_metrics = owner_metrics.sort_values('Total Pipeline', ascending=False)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=owner_metrics['Sales Owner'],
                x=owner_metrics['Total Pipeline'],
                name='Total Pipeline',
                orientation='h',
                marker_color=colors['primary']
            ))
            
            fig.add_trace(go.Bar(
                y=owner_metrics['Sales Owner'],
                x=owner_metrics['Closed Won'],
                name='Closed Won',
                orientation='h',
                marker_color=colors['success']
            ))
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                title='Sales Owner Performance',
                barmode='overlay',
                xaxis_title='Amount (Lakhs)',
                yaxis_title='Sales Owner',
                showlegend=True
            )
            
            fig.update_traces(texttemplate='₹%{x:.2f}L', textposition='auto')
            
            st.plotly_chart(fig, use_container_width=True, key="sales_leaderboard")
            
            st.dataframe(
                owner_metrics.style.format({
                    'Total Pipeline': '₹{:.2f}L',
                    'Closed Won': '₹{:.2f}L',
                    'Win Rate': '{:.1f}%'
                }),
                use_container_width=True
            )
            
            if st.session_state.dashboard_config['show_win_rate'] and 'Sales Owner' in filtered_df.columns:
                st.markdown("""
                    <div class="section-header">
                        <h3>🎯 Win Rate Analysis</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                win_rate_metrics = filtered_df.groupby('Sales Owner').agg({
                    'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum() / len(x) * 100
                }).reset_index()
                
                win_rate_metrics.columns = ['Sales Owner', 'Win Rate']
                win_rate_metrics = win_rate_metrics.sort_values('Win Rate', ascending=False)
                
                fig = px.bar(
                    win_rate_metrics,
                    x='Sales Owner',
                    y='Win Rate',
                    title='Win Rate by Sales Owner',
                    text='Win Rate'
                )
                
                fig = apply_theme_to_plot(fig)
                fig.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    marker_color=colors['success']
                )
                
                st.plotly_chart(fig, use_container_width=True, key="win_rate")
                
                st.dataframe(
                    win_rate_metrics.style.format({
                        'Win Rate': '{:.1f}%'
                    }),
                    use_container_width=True
                )
        else:
            st.info("Sales Owner data is not available in the dataset.")

    def show_geo():
        if not st.session_state.dashboard_config['show_geo_view']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🌍 Geography View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        geography_columns = ['Region', 'Country', 'Geography']
        available_geo_column = next((col for col in geography_columns if col in filtered_df.columns), None)
        
        if available_geo_column:
            geo_metrics = filtered_df.groupby(available_geo_column).agg({
                'Amount': 'sum',
                'Opportunity Number': 'count'
            }).reset_index()
            
            geo_metrics['Amount'] = geo_metrics['Amount'] / 100000
            
            fig = px.choropleth(
                geo_metrics,
                locations=available_geo_column,
                locationmode='country names' if available_geo_column in ['Country', 'Geography'] else None,
                color='Amount',
                hover_data=['Opportunity Number'],
                title=f'{available_geo_column}-wise Pipeline Distribution',
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
            
            st.plotly_chart(fig, use_container_width=True, key="geo_view")
            
            st.dataframe(
                geo_metrics.style.format({
                    'Amount': '₹{:.2f}L',
                    'Opportunity Number': '{:,.0f}'
                }),
                use_container_width=True
            )
        else:
            st.info("No geography data (Region, Country, or Geography) is available in the dataset.")

    def show_detailed():
        if not st.session_state.dashboard_config['show_detailed_view']:
            return
        
        st.markdown("""
            <div class="section-header">
                <h3>🧾 Detailed Deals</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Add Weighted Revenue column if configured
        if st.session_state.dashboard_config['show_weighted_revenue']:
            filtered_df['Weighted Revenue'] = filtered_df['Amount'] * filtered_df['Probability'] / 100
        
        # Define columns for display
        columns_to_show = [
            'Opportunity Number',
            'Organization Name',
            'Amount',
            'Probability',
            'Weighted Revenue',
            'Quarter',
            'Practice',
            'Sales Stage',
            'Tech Owner',
            'Sales Owner',
            'Expected Close Date'
        ]
        
        # Filter columns that exist in the dataframe
        available_columns = [col for col in columns_to_show if col in filtered_df.columns]
        
        # Table filters
        st.markdown('<div class="table-filters">', unsafe_allow_html=True)
        
        # Search filter
        search_term = st.text_input("🔍 Search", key="table_search")
        
        # Column filters in two rows
        col1, col2, col3 = st.columns(3)
        with col1:
            practice_filter = st.multiselect(
                "Practice",
                options=safe_sort_unique(filtered_df['Practice']),
                default=[]
            )
        with col2:
            stage_filter = st.multiselect(
                "Sales Stage",
                options=safe_sort_unique(filtered_df['Sales Stage']),
                default=[]
            )
        with col3:
            quarter_filter = st.multiselect(
                "Quarter",
                options=safe_sort_unique(filtered_df['Quarter']),
                default=[]
            )
        
        # Add probability range filter in a new row
        if 'Probability' in filtered_df.columns:
            prob_col1, prob_col2 = st.columns(2)
            with prob_col1:
                min_prob = st.number_input(
                    "Min Probability (%)",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=5
                )
            with prob_col2:
                max_prob = st.number_input(
                    "Max Probability (%)",
                    min_value=0,
                    max_value=100,
                    value=100,
                    step=5
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_table_df = filtered_df.copy()
        
        # Text search filter
        if search_term:
            filtered_table_df = filtered_table_df[
                filtered_table_df['Organization Name'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_table_df['Opportunity Number'].astype(str).str.contains(search_term, case=False, na=False)
            ]
        
        # Apply column filters
        if practice_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Practice'].astype(str).isin(practice_filter)]
        if stage_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Sales Stage'].astype(str).isin(stage_filter)]
        if quarter_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Quarter'].astype(str).isin(quarter_filter)]
        
        # Apply probability range filter
        if 'Probability' in filtered_df.columns:
            filtered_table_df = filtered_table_df[
                (filtered_table_df['Probability'] >= min_prob) &
                (filtered_table_df['Probability'] <= max_prob)
            ]
        
        # Display table with formatting and column configuration
        st.dataframe(
            filtered_table_df[available_columns].style.format({
                'Amount': '₹{:.2f}L',
                'Weighted Revenue': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True,
            height=600
        )
        
        # Add summary metrics for filtered data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Amount (Filtered)",
                format_lakhs(filtered_table_df['Amount'].sum()),
                delta=None
            )
        with col2:
            if 'Probability' in filtered_table_df.columns:
                st.metric(
                    "Average Probability (Filtered)",
                    f"{filtered_table_df['Probability'].mean():.1f}%",
                    delta=None
                )
        with col3:
            st.metric(
                "Number of Deals (Filtered)",
                f"{len(filtered_table_df):,}",
                delta=None
            )
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            # Export to CSV
            csv = filtered_table_df[available_columns].to_csv(index=False)
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name="filtered_deals.csv",
                mime="text/csv"
            )
        with col2:
            # Export to Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                filtered_table_df[available_columns].to_excel(writer, index=False, sheet_name='Deals')
            excel_buffer.seek(0)
            st.download_button(
                label="📊 Export to Excel",
                data=excel_buffer,
                file_name="filtered_deals.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    def show_editor():
        st.markdown("""
            <div class="section-header">
                <h3>✏️ Data Editor</h3>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            # Create a copy of the dataframe to avoid modifying the original
            editor_df = filtered_df.copy()
            
            # Ensure all columns are properly formatted
            for col in editor_df.columns:
                if editor_df[col].dtype == 'float64':
                    editor_df[col] = editor_df[col].fillna(0)
                elif editor_df[col].dtype == 'object':
                    editor_df[col] = editor_df[col].fillna('')
            
            # Define column types for the editor
            column_types = {
                'Amount': st.column_config.NumberColumn(
                    'Amount',
                    format="₹%.2f",
                    min_value=0,
                    step=1000
                ),
                'Probability': st.column_config.NumberColumn(
                    'Probability',
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                    step=5
                ),
                'Expected Close Date': st.column_config.DateColumn(
                    'Expected Close Date',
                    format="YYYY-MM-DD"
                ),
                'Quarter': st.column_config.SelectboxColumn(
                    'Quarter',
                    options=safe_sort_unique(editor_df['Quarter'])
                ),
                'Practice': st.column_config.SelectboxColumn(
                    'Practice',
                    options=safe_sort_unique(editor_df['Practice'])
                ),
                'Sales Stage': st.column_config.SelectboxColumn(
                    'Sales Stage',
                    options=safe_sort_unique(editor_df['Sales Stage'])
                ),
                'Hunting/Farming': st.column_config.SelectboxColumn(
                    'Hunting/Farming',
                    options=safe_sort_unique(editor_df['Hunting/Farming'])
                )
            }
            
            # Filter column types to only include columns that exist in the dataframe
            available_column_types = {
                col: config for col, config in column_types.items() 
                if col in editor_df.columns
            }
            
            # Display the data editor with proper configuration
            edited_df = st.data_editor(
                editor_df,
                column_config=available_column_types,
                num_rows="dynamic",
                use_container_width=True,
                key="data_editor"
            )
            
            # Add export buttons
            col1, col2 = st.columns(2)
            with col1:
                # Export to CSV
                csv = edited_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv,
                    file_name="edited_deals.csv",
                    mime="text/csv"
                )
            with col2:
                # Export to Excel
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    edited_df.to_excel(writer, index=False, sheet_name='Deals')
                excel_buffer.seek(0)
                st.download_button(
                    label="📊 Export to Excel",
                    data=excel_buffer,
                    file_name="edited_deals.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
        except Exception as e:
            st.error(f"Error in Data Editor: {str(e)}")
            st.info("Please try refreshing the page or check if the data is properly formatted.")

    # Main content area
    st.title("📊 Sales Dashboard")

    # Show the selected view
    view_functions = {
        'overview': show_overview,
        'trends': show_trends,
        'funnel': show_funnel,
        'strategy': show_strategy,
        'leaderboard': show_leaderboard,
        'geo': show_geo,
        'detailed': show_detailed,
        'editor': show_editor
    }

    if st.session_state.current_view in view_functions:
        view_functions[st.session_state.current_view]()
    else:
        st.info("Please select a view from the sidebar.") 
