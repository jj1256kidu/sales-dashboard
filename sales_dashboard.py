import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import other libraries after page config
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from functools import lru_cache
import hashlib
from auth import is_authenticated, get_current_user, show_login_page, logout, init_session_state

# Initialize session state with persistence
if "persistent_state" not in st.session_state:
    st.session_state.persistent_state = {
        "authenticated": False,
        "username": None,
        "current_view": "data_input",
        "df": None,
        "date_filter": None,
        "selected_practice": "All",
        "selected_stage": "All",
        "reset_triggered": False,
        "selected_team_member": None,
        "sales_target": 0.0
    }

# Use persistent state for all session variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = st.session_state.persistent_state["authenticated"]
if "username" not in st.session_state:
    st.session_state.username = st.session_state.persistent_state["username"]
if "current_view" not in st.session_state:
    st.session_state.current_view = st.session_state.persistent_state["current_view"]
if "df" not in st.session_state:
    st.session_state.df = st.session_state.persistent_state["df"]
if "date_filter" not in st.session_state:
    st.session_state.date_filter = st.session_state.persistent_state["date_filter"]
if "selected_practice" not in st.session_state:
    st.session_state.selected_practice = st.session_state.persistent_state["selected_practice"]
if "selected_stage" not in st.session_state:
    st.session_state.selected_stage = st.session_state.persistent_state["selected_stage"]
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = st.session_state.persistent_state["reset_triggered"]
if "selected_team_member" not in st.session_state:
    st.session_state.selected_team_member = st.session_state.persistent_state["selected_team_member"]
if "sales_target" not in st.session_state:
    st.session_state.sales_target = st.session_state.persistent_state["sales_target"]

# Update persistent state whenever session state changes
def update_persistent_state():
    st.session_state.persistent_state.update({
        "authenticated": st.session_state.authenticated,
        "username": st.session_state.username,
        "current_view": st.session_state.current_view,
        "df": st.session_state.df,
        "date_filter": st.session_state.date_filter,
        "selected_practice": st.session_state.selected_practice,
        "selected_stage": st.session_state.selected_stage,
        "reset_triggered": st.session_state.reset_triggered,
        "selected_team_member": st.session_state.selected_team_member,
        "sales_target": st.session_state.sales_target
    })

# Modified logout function to properly clear persistent state
def logout():
    st.session_state.persistent_state = {
        "authenticated": False,
        "username": None,
        "current_view": "data_input",
        "df": None,
        "date_filter": None,
        "selected_practice": "All",
        "selected_stage": "All",
        "reset_triggered": False,
        "selected_team_member": None,
        "sales_target": 0.0
    }
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Format helper functions
def format_amount(x):
    try:
        if pd.isna(x) or x == 0:
            return "₹0L"
        # Convert to float first to handle string inputs, then to int
        value = float(str(x).replace('₹', '').replace('L', '').replace(',', ''))
        return f"₹{int(value)}L"
    except:
        return "₹0L"

def format_percentage(x):
    try:
        if pd.isna(x) or x == 0:
            return "0%"
        # Handle string percentage inputs
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
        # Convert to float first to handle string inputs, then to int
        value = float(str(x).replace(',', ''))
        return f"{int(value):,}"
    except:
        return "0"

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Modern theme colors */
    :root {
        --primary-color: #00b8d4;
        --secondary-color: #006064;
        --accent-color: #84ffff;
        --background-color: #003340;
        --card-background: rgba(0, 184, 212, 0.1);
        --text-color: #ffffff;
        --text-light: rgba(255, 255, 255, 0.9);
        --text-muted: rgba(255, 255, 255, 0.7);
        --border-color: rgba(255, 255, 255, 0.1);
        --shadow-color: rgba(0, 0, 0, 0.2);
        --success-color: #00e676;
        --warning-color: #ffd740;
        --danger-color: #ff5252;
    }

    /* Main container and background */
    .stApp {
        background: linear-gradient(135deg, var(--background-color), var(--secondary-color)) !important;
        color: var(--text-color);
        font-family: 'Segoe UI', sans-serif;
        line-height: 1.6;
        position: relative;
        overflow: hidden;
    }

    /* Abstract wave background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1000 1000' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M 0 1000 Q 250 750 500 1000 T 1000 1000 V 1000 H 0' fill='rgba(0, 184, 212, 0.05)'/%3E%3Cpath d='M 0 1000 Q 250 850 500 1000 T 1000 1000 V 1000 H 0' fill='rgba(0, 184, 212, 0.03)'/%3E%3C/svg%3E") no-repeat center center fixed;
        background-size: cover;
        opacity: 0.1;
        z-index: 0;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 184, 212, 0.2), rgba(0, 96, 100, 0.2));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.2);
    }

    .metric-label {
        color: var(--text-light) !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: var(--accent-color) !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .metric-sublabel {
        color: var(--text-muted) !important;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Progress bar container */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 20px 0;
    }

    /* Progress bar */
    .progress-bar {
        background: linear-gradient(90deg, var(--success-color), var(--accent-color));
        height: 40px;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--text-color);
        font-weight: 700;
        font-size: 1.2em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        z-index: 1;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, rgba(0, 184, 212, 0.2), rgba(0, 96, 100, 0.2));
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .section-header h2 {
        color: var(--text-color) !important;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }

    /* Data tables */
    .dataframe, .stDataFrame {
        background: rgba(0, 184, 212, 0.1) !important;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
    }

    .dataframe th, .stDataFrame th {
        background: rgba(0, 184, 212, 0.2) !important;
        color: var(--text-color) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }

    .dataframe td, .stDataFrame td {
        color: var(--text-light) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem !important;
    }

    /* Form elements */
    .stSelectbox [data-baseweb="select"],
    .stTextInput > div > div > input {
        background: rgba(0, 184, 212, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: var(--text-color) !important;
        border-radius: 8px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .stSelectbox [data-baseweb="select"]:hover,
    .stTextInput > div > div > input:hover {
        border-color: var(--accent-color) !important;
    }

    /* Labels */
    .stSelectbox label, 
    .stTextInput label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-color);
    }
</style>
""", unsafe_allow_html=True)

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
        for col in ['Organization Name', 'Opportunity Name', 'Sales Owner', 'Sales Stage', 'KritiKal Focus Areas']:
            if col in df.columns:
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
            mask &= (df['Probability_Num'] >= min_prob) & (df['Probability_Num'] <= max_prob)
        else:
            prob_range = filters['probability_filter'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
            mask &= (df['Probability_Num'] >= min_prob) & (df['Probability_Num'] <= max_prob)
    
    if filters.get('status_filter') != "All Status":
        current_month = pd.Timestamp.now().strftime('%B')
        if filters['status_filter'] == "Committed for the Month":
            mask &= (df['Month'] == current_month) & (df['Probability_Num'] > 75)
        elif filters['status_filter'] == "Upsides for the Month":
            mask &= (df['Month'] == current_month) & (df['Probability_Num'].between(25, 75))
    
    if filters.get('focus_filter') != "All Focus":
        mask &= df['KritiKal Focus Areas'] == filters['focus_filter']
    
    return df[mask]

def show_data_input():
    # Custom header
    st.markdown("""
        <div class="custom-header">
            <h1>Sales Performance Dashboard</h1>
            <p style="font-size: 1.2em; margin: 0;">Upload your sales data to begin analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Main upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        
        # Only show file uploader if no data is loaded
        if st.session_state.df is None:
            uploaded_file = st.file_uploader(
                "Upload Sales Data",
                type=['xlsx', 'csv'],
                help="Upload your sales data file in Excel or CSV format"
            )
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.xlsx'):
                        excel_file = pd.ExcelFile(uploaded_file)
                        sheet_name = st.selectbox("Select Worksheet", excel_file.sheet_names)
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    else:
                        df = pd.read_csv(uploaded_file)
                    
                    st.session_state.df = df
                    st.session_state.persistent_state["df"] = df
                    update_persistent_state()
                    st.success(f"Successfully loaded {len(df):,} records")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            # Show current data info and clear button
            st.info(f"Currently loaded: {len(st.session_state.df):,} records")
            if st.button("Clear Data", type="secondary"):
                st.session_state.df = None
                st.session_state.persistent_state["df"] = None
                update_persistent_state()
                st.rerun()
        
        # Preview the data if available
        if st.session_state.df is not None:
            st.subheader("Data Preview")
            st.dataframe(st.session_state.df.head(), use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Required Data Fields</h4>
            <ul>
                <li>Amount</li>
                <li>Sales Stage</li>
                <li>Expected Close Date</li>
                <li>Practice/Region</li>
            </ul>
            <h4>File Formats</h4>
            <ul>
                <li>Excel (.xlsx)</li>
                <li>CSV (.csv)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_overview():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Performance Overview")
    df = st.session_state.df.copy()

    # --------------------------------------------------------
    # (1) Let user edit the target as an integer
    # --------------------------------------------------------
    #st.markdown("### Enter Your Sales Target (Optional)")
    #user_target = st.number_input(
     #   "Sales Target (in Lakhs)",
      #   value=float(st.session_state.sales_target),  # existing value or 0
       #  step=0.1,  # or 1.0 if you want full numbers
        # format="%.1f"
    #)
    #try:
     #   user_target = float(user_target_input)
    #except ValueError:
    #    user_target = 0 
    st.markdown("### Enter Your Sales Target (Optional)")

# Get existing value from session state or default to "0"
    default_target = str(int(st.session_state.get("sales_target", 0)))

# Input as string (no steppers)
    user_target_input = st.text_input("Sales Target (in Lakhs)", value=default_target)

# Try to convert it to int
    try:
        user_target = int(user_target_input)
    except ValueError:
        user_target = 0  # fallback value if user input is invalid

    st.write("You entered:", user_target)

    # Store as float if you like, or keep it integer
    st.session_state.sales_target = float(user_target)

    # Calculate total "Closed Won"
    won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
    won_amount_lacs = won_deals['Amount'].sum() / 100000  # convert to Lakhs

    # Show "Target vs Closed Won" progress
    if st.session_state.sales_target > 0:
        achievement_pct = (won_amount_lacs / st.session_state.sales_target) * 100
    else:
        achievement_pct = 0

    st.markdown(
        f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div>
                    <h3 style="color: var(--text-light); margin: 0; font-size: 1.4em; font-weight: 600;">
                        Closed Won
                    </h3>
                    <div style="color: var(--accent-color); font-size: 2.2em; font-weight: 700; margin-top: 5px;">
                        ₹{int(won_amount_lacs):,}L
                    </div>
                </div>
                <div style="color: var(--text-muted); font-size: 1.1em; text-align: right;">
                    Target: ₹{int(st.session_state.sales_target):,}L
                </div>
            </div>
            <div class="progress-bar" style="width: 100%;">
                <div style="background: linear-gradient(90deg, var(--success-color), var(--accent-color)); height: 100%; width: {min(achievement_pct, 100)}%; transition: width 0.5s ease-in-out;"></div>
                <div class="progress-text">
                    {int(achievement_pct)}% Complete
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # II. Practice
    st.markdown("""
        <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Practice</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Practice' in df.columns:
        # Add practice filter
        practices = ['All'] + sorted(df['Practice'].dropna().unique().tolist())
        selected_practice = st.selectbox(
            "Select Practice",
            options=practices,
            key="practice_filter"
        )
        
        # Filter data based on selected practice
        df_practice = df.copy()
        if selected_practice != 'All':
            df_practice = df_practice[df_practice['Practice'] == selected_practice]
        
        # Calculate practice metrics
        practice_metrics = df_practice.groupby('Practice').agg({
            'Amount': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
            'Sales Stage': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
        
        # Pipeline by practice
        pipeline_df = df_practice[~df_practice['Sales Stage'].str.contains('Won', case=False, na=False)]
        total_pipeline = pipeline_df.groupby('Practice')['Amount'].sum() / 100000
        practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
        
        # Pipeline deal counts
        total_deals = pipeline_df.groupby('Practice').size()
        practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals)
        
        # Sort by pipeline
        practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pipeline = go.Figure()
            fig_pipeline.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Total Pipeline'],
                name='Pipeline',
                text=practice_metrics['Total Pipeline'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_pipeline.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Closed Amount'],
                name='Closed Won',
                text=practice_metrics['Closed Amount'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_pipeline.update_layout(
                title=dict(
                    text="Practice-wise Pipeline vs Closed Won",
                    font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top'
                ),
                height=500,
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1,
                xaxis_title=dict(
                    text="Practice",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                yaxis_title=dict(
                    text="Amount (Lakhs)",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                ),
                font=dict(size=14, family='Segoe UI'),
                xaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=80, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_pipeline, use_container_width=True)
        
        with col2:
            fig_deals = go.Figure()
            fig_deals.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Pipeline Deals'],
                name='Pipeline Deals',
                text=practice_metrics['Pipeline Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_deals.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Closed Deals'],
                name='Closed Deals',
                text=practice_metrics['Closed Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_deals.update_layout(
                title=dict(
                    text="Practice-wise Pipeline vs Closed Deals",
                    font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top'
                ),
                height=500,
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1,
                xaxis_title=dict(
                    text="Practice",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                yaxis_title=dict(
                    text="Number of Deals",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                ),
                font=dict(size=14, family='Segoe UI'),
                xaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=80, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_deals, use_container_width=True)
        
        # Practice summary
        st.markdown("### Practice Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pipeline_val = practice_metrics['Total Pipeline'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Pipeline</div>
                    <div class='metric-value'>₹{int(total_pipeline_val)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_deals_count = practice_metrics['Pipeline Deals'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Pipeline Deals</div>
                    <div class='metric-value'>{int(total_deals_count)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Active opportunities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_won = practice_metrics['Closed Deals'].sum()
            win_rate = (total_won / (total_won + total_deals_count) * 100) if (total_won + total_deals_count) > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Win Rate</div>
                    <div class='metric-value'>{int(win_rate)}%</div>
                    <div style='color: #666; font-size: 0.9em;'>{int(total_won)} won</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_deal_size = practice_metrics['Closed Amount'].sum() / total_won if total_won > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Avg Deal Size</div>
                    <div class='metric-value'>₹{int(avg_deal_size)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Practice-wise table
        st.markdown("### Practice-wise Details")
        summary_data = practice_metrics.copy()
        summary_data['Win Rate'] = (summary_data['Closed Deals'] / (summary_data['Closed Deals'] + summary_data['Pipeline Deals']) * 100).round(1)
        summary_data['Closed Amount'] = summary_data['Closed Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Total Pipeline'] = summary_data['Total Pipeline'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{int(x)}%")
        
        st.dataframe(
            summary_data[['Practice', 'Closed Amount', 'Total Pipeline', 'Closed Deals', 'Pipeline Deals', 'Win Rate']],
            use_container_width=True
        )
    else:
        st.error("Practice column not found in the dataset")

    # KritiKal Focus Areas
    st.markdown("""
        <div style='background: linear-gradient(90deg, #9b59b6 0%, #8e44ad 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>KritiKal Focus Areas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'KritiKal Focus Areas' in df.columns:
        focus_metrics = df.groupby('KritiKal Focus Areas').agg({
            'Amount': 'sum',
            'Sales Stage': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        focus_metrics['KritiKal Focus Areas'] = focus_metrics['KritiKal Focus Areas'].fillna('Uncategorized')
        
        focus_metrics.columns = ['Focus Area', 'Total Amount', 'Closed Deals']
        focus_metrics['Total Amount'] = focus_metrics['Total Amount'] / 100000
        
        total_deals_focus = df.groupby('KritiKal Focus Areas').size().reset_index()
        total_deals_focus.columns = ['Focus Area', 'Total Deals']
        focus_metrics = focus_metrics.merge(total_deals_focus, on='Focus Area', how='left')
        
        total_amount_focus = focus_metrics['Total Amount'].sum()
        focus_metrics['Share %'] = (focus_metrics['Total Amount'] / total_amount_focus * 100).round(1)
        
        focus_metrics = focus_metrics.sort_values('Total Amount', ascending=False)
        
        st.markdown("### Focus Areas Summary")
        summary_data = focus_metrics.copy()
        summary_data['Total Amount'] = summary_data['Total Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Share %'] = summary_data['Share %'].apply(lambda x: f"{int(x)}%")
        
        summary_data = summary_data.reset_index(drop=True)
        summary_data.index = summary_data.index + 1
        
        st.dataframe(
            summary_data[['Focus Area', 'Total Amount', 'Share %', 'Total Deals', 'Closed Deals']],
            use_container_width=True
        )
        
        st.markdown("### Focus Areas Distribution")
        fig_focus = go.Figure(data=[go.Pie(
            labels=focus_metrics['Focus Area'],
            values=focus_metrics['Total Amount'],
            hole=.4,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>' + format_amount('%{value}'),
            textfont=dict(size=14, family='Segoe UI', weight='bold')
        )])
        
        fig_focus.update_layout(
            title=dict(
                text="Focus Areas Distribution",
                font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            height=500,
            showlegend=True,
            legend=dict(
                font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            ),
            annotations=[dict(
                text=f"Total: ₹{int(total_amount_focus)}L",
                font=dict(size=16, family='Segoe UI', weight='bold'),
                showarrow=False,
                x=0.5,
                y=0.5
            )]
        )
        
        st.plotly_chart(fig_focus, use_container_width=True)
    else:
        st.info("KritiKal Focus Areas column not found in the dataset")

    # Monthly Pipeline Trend
    st.markdown("""
        <div style='background: linear-gradient(90deg, #00b4db 0%, #0083b0 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Monthly Pipeline Trend</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Expected Close Date' in df.columns and 'Amount' in df.columns and 'Sales Stage' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
        
        deal_type = st.selectbox(
            "Select Deal Type",
            ["🌊 Pipeline", "🟢 Closed Won", "📦 All Deals"],
            index=0
        )
        
        if deal_type == "🌊 Pipeline":
            filtered_df = df[~df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#00b4db'
        elif deal_type == "🟢 Closed Won":
            filtered_df = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#2ecc71'
        else:
            filtered_df = df
            color = '#9b59b6'
        
        monthly_data = filtered_df.groupby(filtered_df['Expected Close Date'].dt.to_period('M')).agg({
            'Amount': 'sum',
            'Sales Stage': 'count'
        }).reset_index()
        
        monthly_data['Expected Close Date'] = monthly_data['Expected Close Date'].astype(str)
        monthly_data['Amount'] = monthly_data['Amount'] / 100000
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_data['Expected Close Date'],
            y=monthly_data['Amount'],
            mode='lines+markers',
            name=deal_type,
            line=dict(width=3, color=color),
            marker=dict(size=8, color=color),
            text=monthly_data['Amount'].apply(lambda x: f"₹{int(x)}L"),
            textposition='top center',
            textfont=dict(size=12, family='Segoe UI', weight='bold')
        ))
        
        fig_trend.update_layout(
            title=dict(
                text=f"{deal_type} Trend",
                font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            height=500,
            showlegend=False,
            xaxis_title=dict(
                text="Month",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
            ),
            yaxis_title=dict(
                text="Amount (Lakhs)",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
            ),
            font=dict(size=14, family='Segoe UI'),
            xaxis=dict(
                tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            yaxis=dict(
                tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_value = monthly_data['Amount'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Value</div>
                    <div class='metric-value'>₹{int(total_value)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Overall</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            avg_monthly = monthly_data['Amount'].mean()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Monthly Average</div>
                    <div class='metric-value'>₹{int(avg_monthly)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per month</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            total_deals = monthly_data['Sales Stage'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Deals</div>
                    <div class='metric-value'>{int(total_deals)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Number of deals</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Required columns (Expected Close Date, Amount, Sales Stage) not found in the dataset")

def show_sales_team():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view team information")
        return
    
    # Process data once with caching
    df = process_data(st.session_state.df)
    
    # Team members
    team_members = sorted(df['Sales Owner'].dropna().unique().tolist())
    
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        '>
            <h2 style='
                color: white;
                margin: 0;
                text-align: center;
                font-size: 2em;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            '>Sales Team Data</h2>
        </div>
    """, unsafe_allow_html=True)

    metrics = calculate_team_metrics(df)
    
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    metric_style = """
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, {gradient});
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 10px 5px;
    """
    metric_text_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.6em;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        margin: 15px 0;
        letter-spacing: 0.5px;
        -webkit-font-smoothing: antialiased;
    """
    label_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        -webkit-font-smoothing: antialiased;
    """
    sublabel_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.2em;
        font-weight: 700;
        margin-top: 8px;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        -webkit-font-smoothing: antialiased;
    """
    
    total_pipeline = metrics['Current Pipeline'].sum()
    total_closed = metrics['Closed Won'].sum()
    total_closed_deals = metrics['Closed Deals'].sum()
    total_pipeline_deals = metrics['Pipeline Deals'].sum()
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Pipeline Value</div>
                <div class="metric-value">₹{int(total_pipeline)}L</div>
                <div class="metric-sublabel">Active opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Closed Won</div>
                <div class="metric-value">₹{int(total_closed)}L</div>
                <div class="metric-sublabel">Won opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = round((total_closed_deals / (total_closed_deals + total_pipeline_deals) * 100), 1) if (total_closed_deals + total_pipeline_deals) > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Win Rate</div>
                <div class="metric-value">{int(win_rate)}%</div>
                <div class="metric-sublabel">{int(total_closed_deals)} won</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_deal_size = round(total_closed / total_closed_deals, 1) if total_closed_deals > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Deal Size</div>
                <div class="metric-value">₹{int(avg_deal_size)}L</div>
                <div class="metric-sublabel">Per won deal</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h4 style='color: #2a5298; margin: 0; font-size: 1.1em; font-weight: 600;'>🔍 Team Filters</h4>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        filters = {
            'selected_member': st.selectbox(
                "👤 Sales Owner",
                options=["All Team Members"] + team_members,
                key="team_view_member_filter"
            )
        }
    with col2:
        filters['search'] = st.text_input("🔍 Search", placeholder="Search...", key="team_view_search_filter")
    with col3:
        fiscal_order = ['April', 'May', 'June', 'July', 'August', 'September', 
                       'October', 'November', 'December', 'January', 'February', 'March']
        available_months = df['Month'].dropna().unique().tolist()
        available_months.sort(key=lambda x: fiscal_order.index(x) if x in fiscal_order else len(fiscal_order))
        filters['month_filter'] = st.selectbox("📅 Month", options=["All Months"] + available_months, key="team_view_month_filter")
    with col4:
        filters['quarter_filter'] = st.selectbox("📊 Quarter", options=["All Quarters", "Q1", "Q2", "Q3", "Q4"], key="team_view_quarter_filter")
    with col5:
        filters['year_filter'] = st.selectbox("📅 Year", options=["All Years"] + sorted(df['Expected Close Date'].dt.year.unique().tolist()), key="team_view_year_filter")
    with col6:
        probability_options = ["All Probability", "0-25%", "26-50%", "51-75%", "76-100%", "Custom Range"]
        filters['probability_filter'] = st.selectbox("📈 Probability", options=probability_options, key="team_view_probability_filter")
        if filters['probability_filter'] == "Custom Range":
            col6a, col6b = st.columns(2)
            with col6a:
                min_prob = st.text_input("Min %", value="0", key="team_view_prob_min_filter")
            with col6b:
                max_prob = st.text_input("Max %", value="100", key="team_view_prob_max_filter")
            try:
                min_prob = int(min_prob)
                max_prob = int(max_prob)
                filters['custom_prob_range'] = f"{min_prob}-{max_prob}%"
            except ValueError:
                st.warning("Please enter valid numbers for probability range")
                filters['custom_prob_range'] = "0-100%"
    with col7:
        status_options = ["All Status", "Committed for the Month", "Upsides for the Month"]
        filters['status_filter'] = st.selectbox("🎯 Status", options=status_options, key="team_view_status_filter")
    with col8:
        if 'KritiKal Focus Areas' in df.columns:
            focus_areas = ["All Focus"] + sorted(df['KritiKal Focus Areas'].dropna().unique().tolist())
            filters['focus_filter'] = st.selectbox("🎯 Focus", options=focus_areas, key="team_view_focus_filter")

    filtered_df = filter_dataframe(df, filters)
    
    st.markdown("""
        <div style='margin-bottom: 20px;'>
            <h3 style='color: #2a5298; margin: 0; font-size: 1.4em; font-weight: 600;'>Performance Metrics</h3>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    current_pipeline = filtered_df[~filtered_df['Is_Won']]['Amount_Lacs'].sum()
    weighted_projections = filtered_df[~filtered_df['Is_Won']]['Weighted_Amount'].sum()
    closed_won = filtered_df[filtered_df['Is_Won']]['Amount_Lacs'].sum()

    with m1:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
                height: 100%;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    🌊 Current Pipeline
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(current_pipeline)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #6B5B95 0%, #846EA9 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    ⚖️ Weighted Projections
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(weighted_projections)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    💰 Closed Won
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(closed_won)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style='
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 15px;
            margin: 25px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        '>
            <h3 style='
                color: #2a5298;
                margin: 0;
                font-size: 1.4em;
                font-weight: 600;
                font-family: "Segoe UI", sans-serif;
            '>Team Member Performance</h3>
        </div>
    """, unsafe_allow_html=True)
    
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index = filtered_df.index + 1
    
    display_df = filtered_df[['Organization Name', 'Opportunity Name', 'Geography', 
                            'Expected Close Date', 'Probability', 'Amount', 
                            'Sales Owner', 'Pre-sales Technical Lead', 'Business Owner', 
                            'Type', 'KritiKal Focus Areas']].copy()
    
    display_df = display_df.rename(columns={
        'Amount': 'Amount (In Lacs)',
        'Pre-sales Technical Lead': 'Tech Owner',
        'Type': 'Hunting /farming'
    })
    
    display_df['Amount (In Lacs)'] = display_df['Amount (In Lacs)'].apply(lambda x: int(x/100000) if pd.notnull(x) else 0)
    display_df['Probability'] = display_df['Probability'].apply(format_percentage)
    display_df['Weighted Revenue (In Lacs)'] = display_df.apply(
        lambda row: int((row['Amount (In Lacs)']) * float(str(row['Probability']).rstrip('%'))/100) if pd.notnull(row['Amount (In Lacs)']) else 0, 
        axis=1
    )
    
    display_df['Expected Close Date'] = pd.to_datetime(display_df['Expected Close Date']).dt.strftime('%d-%b-%Y')
    display_df = display_df.sort_values('Amount (In Lacs)', ascending=False)
    
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = 'S.No'
    
    st.dataframe(
        display_df,
        column_config={
            'Amount (In Lacs)': st.column_config.NumberColumn(
                'Amount (In Lacs)',
                format="₹%d L",
                help="Amount in Lakhs"
            ),
            'Weighted Revenue (In Lacs)': st.column_config.NumberColumn(
                'Weighted Revenue (In Lacs)',
                format="₹%d L",
                help="Weighted Revenue in Lakhs"
            ),
            'Probability': st.column_config.TextColumn(
                'Probability',
                help="Probability of winning the deal"
            ),
            'Expected Close Date': st.column_config.TextColumn(
                'Expected Close Date',
                help="Expected closing date"
            )
        }
    )
    
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 15px;
            margin: 25px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        '>
            <h3 style='
                color: #2a5298;
                margin: 0;
                font-size: 1.4em;
                font-weight: 600;
                font-family: "Segoe UI", sans-serif;
            '>Team Member Performance</h3>
        </div>
    """, unsafe_allow_html=True)
    
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': lambda x: round(x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000, 1),
        'Sales Stage': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count()
    }).reset_index()
    team_metrics.columns = ['Sales Owner', 'Closed Won', 'Closed Deals']
    
    pipeline_df = df[~df['Sales Stage'].str.contains('Won', case=False, na=False)]
    total_pipeline = round(pipeline_df.groupby('Sales Owner')['Amount'].sum() / 100000, 1)
    team_metrics['Current Pipeline'] = team_metrics['Sales Owner'].map(total_pipeline)
    
    def calculate_weighted_projection(owner):
        owner_pipeline = pipeline_df[pipeline_df['Sales Owner'] == owner]
        weighted_sum = sum((amt * pr / 100) 
                           for amt, pr in zip(owner_pipeline['Amount'], owner_pipeline['Probability_Num']))
        return round(weighted_sum / 100000, 1)
    
    team_metrics['Weighted Projections'] = team_metrics['Sales Owner'].apply(calculate_weighted_projection)
    
    total_deals_owner = pipeline_df.groupby('Sales Owner').size()
    team_metrics['Pipeline Deals'] = team_metrics['Sales Owner'].map(total_deals_owner)
    team_metrics['Win Rate'] = round((team_metrics['Closed Deals'] / (team_metrics['Closed Deals'] + team_metrics['Pipeline Deals']) * 100), 1)
    team_metrics = team_metrics.sort_values('Current Pipeline', ascending=False)
    
    summary_data = team_metrics.copy()
    summary_data['Current Pipeline'] = summary_data['Current Pipeline'].apply(lambda x: f"₹{x:,}L")
    summary_data['Weighted Projections'] = summary_data['Weighted Projections'].apply(lambda x: f"₹{x:,}L")
    summary_data['Closed Won'] = summary_data['Closed Won'].apply(lambda x: f"₹{x:,}L")
    summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        summary_data[[
            'Sales Owner',
            'Current Pipeline',
            'Weighted Projections',
            'Closed Won',
            'Pipeline Deals',
            'Closed Deals',
            'Win Rate'
        ]],
        use_container_width=True
    )

def show_detailed():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view detailed information")
        return
    
    st.title("Detailed Sales Data")
    df = st.session_state.df
    search = st.text_input("Search", placeholder="Search in any field...")
    
    if search:
        mask = np.column_stack([df[col].astype(str).str.contains(search, case=False, na=False) 
                                for col in df.columns])
        df = df[mask.any(axis=1)]
    
    st.dataframe(df, use_container_width=True)

def show_navigation():
    """Show navigation sidebar with user info and logout"""
    with st.sidebar:
        st.title("Navigation")
        
        # Welcome message and user info
        if st.session_state.authenticated:
            st.markdown(f"""
                <div style='padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; margin-bottom: 15px;'>
                    <h3 style='color: white; margin: 0;'>Welcome, {st.session_state.username}</h3>
                </div>
            """, unsafe_allow_html=True)
        
        # Navigation options
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Sales Team", "Detailed Data"],
            key="nav_view_selector"
        )
        st.session_state.current_view = selected.lower().replace(" ", "_")
        
        # Logout button
        if st.button("Logout", key="nav_logout_button"):
            logout()
            st.rerun()

def show_filters():
    """Show global filters for the dashboard"""
    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, rgba(74, 144, 226, 0.1), rgba(108, 99, 255, 0.1));
                    border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: white; margin: 0;'>Filters</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    filters = {}
    
    with col1:
        if 'Sales Owner' in st.session_state.df.columns:
            team_members = ["All Team Members"] + sorted(st.session_state.df['Sales Owner'].dropna().unique().tolist())
            filters['selected_member'] = st.selectbox(
                "👤 Sales Owner",
                options=team_members,
                key="global_team_member_filter"
            )
    
    with col2:
        filters['search'] = st.text_input(
            "🔍 Search",
            placeholder="Search...",
            key="global_search_filter"
        )
    
    with col3:
        if 'Month' in st.session_state.df.columns:
            fiscal_order = ['April', 'May', 'June', 'July', 'August', 'September', 
                          'October', 'November', 'December', 'January', 'February', 'March']
            available_months = st.session_state.df['Month'].dropna().unique().tolist()
            available_months.sort(key=lambda x: fiscal_order.index(x) if x in fiscal_order else len(fiscal_order))
            filters['month_filter'] = st.selectbox(
                "📅 Month",
                options=["All Months"] + available_months,
                key="global_month_filter"
            )
    
    with col4:
        filters['quarter_filter'] = st.selectbox(
            "📊 Quarter",
            options=["All Quarters", "Q1", "Q2", "Q3", "Q4"],
            key="global_quarter_filter"
        )
    
    with col5:
        if 'Year' in st.session_state.df.columns:
            years = ["All Years"] + sorted(st.session_state.df['Expected Close Date'].dt.year.unique().tolist())
            filters['year_filter'] = st.selectbox(
                "📅 Year",
                options=years,
                key="global_year_filter"
            )
    
    with col6:
        probability_options = ["All Probability", "0-25%", "26-50%", "51-75%", "76-100%", "Custom Range"]
        filters['probability_filter'] = st.selectbox(
            "📈 Probability",
            options=probability_options,
            key="global_probability_filter"
        )
        
        if filters['probability_filter'] == "Custom Range":
            col6a, col6b = st.columns(2)
            with col6a:
                min_prob = st.text_input(
                    "Min %",
                    value="0",
                    key="global_prob_min_filter"
                )
            with col6b:
                max_prob = st.text_input(
                    "Max %",
                    value="100",
                    key="global_prob_max_filter"
                )
            
            try:
                min_prob = int(min_prob)
                max_prob = int(max_prob)
                filters['custom_prob_range'] = f"{min_prob}-{max_prob}%"
            except ValueError:
                st.warning("Please enter valid numbers for probability range")
                filters['custom_prob_range'] = "0-100%"
    
    with col7:
        status_options = ["All Status", "Committed for the Month", "Upsides for the Month"]
        filters['status_filter'] = st.selectbox(
            "🎯 Status",
            options=status_options,
            key="global_status_filter"
        )
    
    with col8:
        if 'KritiKal Focus Areas' in st.session_state.df.columns:
            focus_areas = ["All Focus"] + sorted(st.session_state.df['KritiKal Focus Areas'].dropna().unique().tolist())
            filters['focus_filter'] = st.selectbox(
                "🎯 Focus",
                options=focus_areas,
                key="global_focus_filter"
            )
    
    return filters

def main():
    """Main function to run the dashboard"""
    # Check authentication
    if not is_authenticated():
        show_login_page()
        return
    
    # Get current user
    current_user = get_current_user()
    if not current_user:
        show_login_page()
        return
    
    # Show navigation
    show_navigation()
    
    # Show filters if data is loaded and not in overview or sales_team tab
    if st.session_state.df is not None and st.session_state.current_view not in ["overview", "data_input", "sales_team"]:
        show_filters()
    
    # Display current view
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "sales_team":
        show_sales_team()
    elif st.session_state.current_view == "detailed_data":
        show_detailed()

if __name__ == "__main__":
    main()
