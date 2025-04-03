import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import after st.set_page_config
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from auth import show_login_page, is_authenticated, get_current_user, logout

# Check authentication
if not is_authenticated():
    show_login_page()
    st.stop()

# Initialize session state for dashboard
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "data_input"
if "df" not in st.session_state:
    st.session_state.df = None
if "date_filter" not in st.session_state:
    st.session_state.date_filter = None
if "selected_practice" not in st.session_state:
    st.session_state.selected_practice = "All"
if "selected_stage" not in st.session_state:
    st.session_state.selected_stage = "All"
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False
if "selected_team_member" not in st.session_state:
    st.session_state.selected_team_member = None
if "sales_target" not in st.session_state:
    st.session_state.sales_target = 0.0

# Format helper functions
def format_amount(x):
    try:
        if pd.isna(x) or x == 0:
            return "₹0L"
        value = float(str(x).replace('₹', '').replace('L', '').replace(',', ''))
        return f"₹{int(value)}L"
    except:
        return "₹0L"

def format_percentage(x):
    try:
        if pd.isna(x) or x == 0:
            return "0%"
        if isinstance(x, str):
            value = float(x.rstrip('%'))
        else:
            value = float(x)
        return f"{int(value)}%"
    except:
        return "0%"

def format_number(x):
    try:
        if pd.isna(x) or x == 0:
            return "0"
        value = float(str(x).replace(',', ''))
        return f"{int(value):,}"
    except:
        return "0"

# Cache data processing functions
@st.cache_data
def process_data(df):
    """Process and prepare data for the dashboard"""
    df = df.copy()
    
    # Convert dates and calculate time-based columns at once
    df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
    df['Month'] = df['Expected Close Date'].dt.strftime('%B')
    df['Year'] = df['Expected Close Date'].dt.year
    df['Quarter'] = df['Expected Close Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    
    # Convert probability and calculate numeric values at once with safe null handling
    def convert_probability(x):
        try:
            if pd.isna(x):
                return 0
            if isinstance(x, str):
                x = x.rstrip('%')
            return float(x)
        except:
            return 0
    
    df['Probability_Num'] = df['Probability'].apply(convert_probability)
    
    # Pre-calculate common flags and metrics with safe null handling
    df['Is_Won'] = df['Sales Stage'].str.contains('Won', case=False, na=False)
    df['Amount_Lacs'] = df['Amount'].fillna(0).div(100000).round(0).astype(int)
    df['Weighted_Amount'] = (df['Amount_Lacs'] * df['Probability_Num'] / 100).round(0).astype(int)
    
    return df

@st.cache_data
def calculate_team_metrics(df):
    """Calculate all team-related metrics at once"""
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': lambda x: int(x[df['Is_Won'] & x.notna()].sum() / 100000) if len(x[df['Is_Won'] & x.notna()]) > 0 else 0,
        'Is_Won': 'sum',
        'Amount_Lacs': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0,
        'Weighted_Amount': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0
    }).reset_index()
    
    team_metrics.columns = ['Sales Owner', 'Closed Won', 'Closed Deals', 'Current Pipeline', 'Weighted Projections']
    
    team_metrics = team_metrics.fillna(0)
    
    # Calculate Pipeline Deals
    pipeline_deals = df[~df['Is_Won']].groupby('Sales Owner').size()
    team_metrics['Pipeline Deals'] = team_metrics['Sales Owner'].map(pipeline_deals).fillna(0).astype(int)
    
    # Win Rate
    total_deals = team_metrics['Closed Deals'] + team_metrics['Pipeline Deals']
    team_metrics['Win Rate'] = np.where(
        total_deals > 0,
        (team_metrics['Closed Deals'] / total_deals * 100).round(0),
        0
    ).astype(int)
    
    return team_metrics

@st.cache_data
def filter_dataframe(df, filters):
    """Apply filters to dataframe efficiently"""
    mask = pd.Series(True, index=df.index)
    
    if filters.get('selected_member') != "All Team Members":
        mask &= df['Sales Owner'] == filters['selected_member']
    
    if filters.get('search'):
        search_mask = pd.Series(False, index=df.index)
        search = filters['search'].lower()
        for col in ['Organization Name', 'Opportunity Name', 'Sales Owner', 'Sales Stage']:
            search_mask |= df[col].astype(str).str.lower().str.contains(search, na=False)
        mask &= search_mask
    
    if filters.get('month_filter') != "All Months":
        mask &= df['Month'] == filters['month_filter']
    
    if filters.get('quarter_filter') != "All Quarters":
        mask &= df['Quarter'] == filters['quarter_filter']
    
    if filters.get('year_filter') != "All Years":
        mask &= df['Year'] == filters['year_filter']
    
    if filters.get('probability_filter') != "All Probability":
        if filters['probability_filter'] == "Custom Range":
            prob_range = filters['custom_prob_range'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        else:
            prob_range = filters['probability_filter'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        mask &= (df['Probability_Num'] >= min_prob) & (df['Probability_Num'] <= max_prob)
    
    if filters.get('status_filter') != "All Status":
        if filters['status_filter'] == "Committed for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'] > 75)
        elif filters['status_filter'] == "Upsides for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'].between(25, 75))
        else:
            mask &= df['Sales Stage'] == filters['status_filter']
    
    if filters.get('focus_filter') != "All Focus":
        mask &= df['KritiKal Focus Areas'] == filters['focus_filter']
    
    return df[mask]

# Sidebar
with st.sidebar:
    st.title("Navigation")
    selected_view = st.radio(
        "Select View",
        ["Data Input", "Overview", "Sales Team", "Detailed Data"],
        key="view_selector"
    )
    st.session_state["current_view"] = selected_view.lower().replace(" ", "_")
    
    # Logout button at the bottom of sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

# Main content
st.title(f"Sales Dashboard - {selected_view}")
st.markdown(f"Welcome back, {get_current_user()}!")

# Apply custom styling
st.markdown("""
    <style>
        /* Modern theme colors */
        :root {
            --primary-color: #4A90E2;
            --background-color: #1E1E1E;
            --secondary-background-color: #252526;
            --text-color: #FFFFFF;
            --font-family: 'Segoe UI', sans-serif;
        }

        /* Main container styling */
        .main {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: var(--font-family);
        }

        /* Card styling */
        .stCard {
            background-color: var(--secondary-background-color);
            border-radius: 10px;
            padding: 15px;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Number formatting */
        .big-number {
            font-size: 2.8em;
            font-weight: 700;
            color: #2ecc71;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            letter-spacing: -1px;
        }

        .metric-value {
            font-size: 2em;
            font-weight: 600;
            color: #4A90E2;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }

        .metric-label {
            font-size: 1.2em;
            color: #333;
            margin-bottom: 5px;
            font-weight: 500;
        }

        /* Section headers */
        .section-header {
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            margin: 30px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }

        /* Chart text styling */
        .js-plotly-plot .plotly .main-svg {
            font-size: 14px;
            font-weight: 500;
        }

        /* Table styling */
        .dataframe {
            font-size: 1.2em;
            background-color: white;
            border-radius: 8px;
            padding: 15px;
        }

        .dataframe th {
            background-color: #4A90E2;
            color: white;
            font-weight: 700;
            padding: 15px;
            font-size: 1.1em;
        }

        .dataframe td {
            padding: 12px;
            border-bottom: 1px solid #eee;
            font-weight: 500;
        }

        /* Upload container styling */
        .upload-container {
            background-color: rgba(74, 144, 226, 0.1);
            border-radius: 10px;
            padding: 30px;
            margin: 20px 0;
            border: 2px dashed rgba(74, 144, 226, 0.3);
            text-align: center;
        }

        /* Button styling */
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #357ABD;
            transform: translateY(-2px);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Custom header */
        .custom-header {
            background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white;
            text-align: center;
        }

        /* Info box */
        .info-box {
            background-color: rgba(74, 144, 226, 0.1);
            border-left: 4px solid #4A90E2;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
        }

        /* Container styling */
        .container {
            margin: 30px 0;
            padding: 15px;
        }

        /* Graph container */
        .graph-container {
            margin: 30px 0;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Metric container */
        .metric-container {
            margin: 30px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        /* Section divider */
        .section-divider {
            margin: 30px 0;
            border-top: 1px solid #eee;
        }

        /* Custom styling for number input */
        [data-testid="stNumberInput"] {
            position: relative;
            background: transparent !important;
        }
        [data-testid="stNumberInput"] > div > div > input {
            color: white !important;
            font-size: 1.8em !important;
            font-weight: 800 !important;
            text-align: center !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        /* Hide the increment/decrement buttons */
        [data-testid="stNumberInput"] > div > div > div {
            display: none !important;
        }
        /* Container styling */
        div[data-testid="column"] > div > div > div > div > div {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }

        /* Hide increment buttons */
        [data-testid="stNumberInput"] input[type="number"] {
            -moz-appearance: textfield;
        }
        [data-testid="stNumberInput"] input[type="number"]::-webkit-outer-spin-button,
        [data-testid="stNumberInput"] input[type="number"]::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        
        /* Style the input field */
        [data-testid="stNumberInput"] {
            background: transparent;
        }
        
        /* Style the display value */
        .target-value {
            font-family: 'Segoe UI', sans-serif;
            font-size: 2.5em;
            font-weight: 800;
            color: #FF6B6B;
            text-align: center;
            padding: 20px;
            margin: 10px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Main view logic
if st.session_state["current_view"] == "data_input":
    show_data_input()
elif st.session_state["current_view"] == "overview":
    show_overview()
elif st.session_state["current_view"] == "sales_team":
    show_sales_team()
elif st.session_state["current_view"] == "detailed_data":
    show_detailed()
