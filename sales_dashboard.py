import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from functools import lru_cache

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'data_input'
if 'date_filter' not in st.session_state:
    st.session_state.date_filter = None
if 'selected_practice' not in st.session_state:
    st.session_state.selected_practice = 'All'
if 'selected_stage' not in st.session_state:
    st.session_state.selected_stage = 'All'
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False
if 'selected_team_member' not in st.session_state:
    st.session_state.selected_team_member = None
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'previousweek_raw_data' not in st.session_state:
    st.session_state.previousweek_raw_data = None
if 'selected_sheet' not in st.session_state:
    st.session_state.selected_sheet = None

# Keep a single "sales_target" in session state
if 'sales_target' not in st.session_state:
    st.session_state.sales_target = 0.0  # Default target in Lakhs

# Custom CSS for modern styling
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

# Cache data processing functions
@st.cache_data
def process_data(df):
    """Process and prepare data for the dashboard"""
    df = df.copy()
    
    # Convert dates and calculate time-based columns at once
    df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], format='%d-%m-%Y', errors='coerce')
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
    
    # Practice filter
    if filters.get('practices'):
        mask &= df['Practice'].isin(filters['practices'])
            
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

def show_data_input():
    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h3 style='color: #2a5298; margin: 0; font-size: 1.2em; font-weight: 600;'>📤 Upload Data</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for current and previous week data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Week Data")
        uploaded_file = st.file_uploader(
            "Upload Current Week Data", 
            type=['xlsx', 'xls'],
            key="current_week_uploader"  # Added unique key
        )
        if uploaded_file is not None:
            try:
                # Read all sheets from the Excel file
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # Show sheet selection dropdown
                selected_sheet = st.selectbox(
                    "Select Current Week Sheet",
                    options=sheet_names,
                    key="current_sheet_select"
                )
                
                # Load the selected sheet
                df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                st.session_state.df = df
                st.session_state.raw_data = {sheet: pd.read_excel(uploaded_file, sheet_name=sheet) for sheet in sheet_names}
                st.session_state.selected_sheet = selected_sheet
                st.success(f"Successfully loaded current week sheet '{selected_sheet}' with {len(df):,} records")
                
            except Exception as e:
                st.error(f"Error reading current week file: {str(e)}")
    
    with col2:
        st.markdown("### Previous Week Data")
        previous_week_file = st.file_uploader(
            "Upload Previous Week Data", 
            type=['xlsx', 'xls'],
            key="previous_week_uploader"  # Added unique key
        )
        if previous_week_file is not None:
            try:
                # Read all sheets from the previous week Excel file
                previous_excel_file = pd.ExcelFile(previous_week_file)
                previous_sheet_names = previous_excel_file.sheet_names
                
                # Show sheet selection dropdown for previous week
                selected_previous_sheet = st.selectbox(
                    "Select Previous Week Sheet",
                    options=previous_sheet_names,
                    key="previous_sheet_select"
                )
                
                # Load the selected sheet
                previous_df = pd.read_excel(previous_week_file, sheet_name=selected_previous_sheet)
                st.session_state.previousweek_raw_data = {sheet: pd.read_excel(previous_week_file, sheet_name=sheet) for sheet in previous_sheet_names}
                st.success(f"Successfully loaded previous week sheet '{selected_previous_sheet}' with {len(previous_df):,} records")
                
            except Exception as e:
                st.error(f"Error reading previous week file: {str(e)}")

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
        <div style='margin-top: 30px; padding: 20px; background: #f0f2f6; border-radius: 12px;'>
            <h3 style='margin: 0; color: #2ecc71; font-size: 1.2em; font-weight: 500;'>Closed Won</h3>
            <h2 style='margin: 5px 0; color: #2ecc71; font-size: 2.8em; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                ₹{won_amount_lacs:,.2f}L
            </h2>
            <div style='text-align: right; margin-bottom: 10px;'>
                <span style='color: #e74c3c; font-size: 1em; font-weight: 500;'>Target: ₹{st.session_state.sales_target:,.0f}L</span>
            </div>
            <div style='background: #e74c3c; height: 40px; border-radius: 20px; overflow: hidden; position: relative; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);'>
                <div style='background: #2ecc71; height: 100%; width: {min(achievement_pct, 100)}%; transition: width 0.5s ease-in-out;'></div>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 600; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                    {int(achievement_pct)}% Complete
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- The rest of your existing Overview code remains below ----

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
    
    col1, col2, col3, col4 = st.columns(4)
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
            <div style='{metric_style.format(gradient="#2193b0 0%, #6dd5ed 100%")}'>
                <div style='{label_style}'>Pipeline Value</div>
                <div style='{metric_text_style}'>₹{int(total_pipeline)}L</div>
                <div style='{sublabel_style}'>Active opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#11998e 0%, #38ef7d 100%")}'>
                <div style='{label_style}'>Closed Won</div>
                <div style='{metric_text_style}'>₹{int(total_closed)}L</div>
                <div style='{sublabel_style}'>Won opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = round((total_closed_deals / (total_closed_deals + total_pipeline_deals) * 100), 1) if (total_closed_deals + total_pipeline_deals) > 0 else 0
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#4e54c8 0%, #8f94fb 100%")}'>
                <div style='{label_style}'>Win Rate</div>
                <div style='{metric_text_style}'>{int(win_rate)}%</div>
                <div style='{sublabel_style}'>{int(total_closed_deals)} won</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_deal_size = round(total_closed / total_closed_deals, 1) if total_closed_deals > 0 else 0
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#f12711 0%, #f5af19 100%")}'>
                <div style='{label_style}'>Avg Deal Size</div>
                <div style='{metric_text_style}'>₹{int(avg_deal_size)}L</div>
                <div style='{sublabel_style}'>Per won deal</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h4 style='color: #2a5298; margin: 0; font-size: 1.1em; font-weight: 600;'>🔍 Filters</h4>
        </div>
    """, unsafe_allow_html=True)

    # Create a single row with all filters using adjusted column sizes
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.2, 1.2, 1.2, 1, 1, 1, 1.2, 1.2])
    
    with col1:
        filters = {
            'selected_member': st.selectbox(
                "👤 Sales Owner",
                options=["All Team Members"] + team_members,
                key="team_member_filter"
            )
        }
    
    with col2:
        filters['search'] = st.text_input("🔍 Search", placeholder="Search...")
    
    with col3:
        if 'Practice' in df.columns:
            practices = sorted(df['Practice'].dropna().unique())
            selected_practices = st.multiselect(
                "🏢 Practice",
                options=practices,
                default=[],
                key="practice_filter"
            )
            filters['practices'] = selected_practices
        else:
            st.error("Practice column not found in the data")
            filters['practices'] = []
    
    with col4:
        fiscal_order = ['April', 'May', 'June', 'July', 'August', 'September', 
                       'October', 'November', 'December', 'January', 'February', 'March']
        available_months = df['Month'].dropna().unique().tolist()
        available_months.sort(key=lambda x: fiscal_order.index(x) if x in fiscal_order else len(fiscal_order))
        filters['month_filter'] = st.selectbox("📅 Month", options=["All Months"] + available_months)
    
    with col5:
        filters['quarter_filter'] = st.selectbox("📊 Quarter", options=["All Quarters", "Q1", "Q2", "Q3", "Q4"])
    
    with col6:
        filters['year_filter'] = st.selectbox("📅 Year", options=["All Years"] + sorted(df['Expected Close Date'].dt.year.unique().tolist()))
    
    with col7:
        probability_options = ["All Probability", "0-25%", "26-50%", "51-75%", "76-100%", "Custom Range"]
        filters['probability_filter'] = st.selectbox("📈 Probability", options=probability_options)
        if filters['probability_filter'] == "Custom Range":
            col7a, col7b = st.columns(2)
            with col7a:
                min_prob_input = st.text_input("Min %", value="0", key="custom_min_prob_input")
            with col7b:
                max_prob_input = st.text_input("Max %", value="100", key="custom_max_prob_input")
            try:
                min_prob = int(min_prob_input)
                max_prob = int(max_prob_input)
                filters['min_prob'] = min_prob
                filters['max_prob'] = max_prob
                filters['custom_prob_range'] = f"{min_prob}-{max_prob}%"
            except ValueError:
                filters['min_prob'] = 0
                filters['max_prob'] = 100
                filters['custom_prob_range'] = "0-100%"
    
    with col8:
        status_options = ["All Status", "Committed for the Month", "Upsides for the Month"]
        filters['status_filter'] = st.selectbox("🎯 Status", options=status_options)
        if filters['status_filter'] == "Committed for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask = (df['Month'] == current_month) & (df['Probability_Num'] > 75)
            filtered_df = df[mask]
        elif filters['status_filter'] == "Upsides for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask = (df['Month'] == current_month) & (df['Probability_Num'].between(25, 75))
            filtered_df = df[mask]
    
    with col8:
        filters['focus_filter'] = st.selectbox("🎯 Focus", options=["All Focus"] + sorted(df['KritiKal Focus Areas'].dropna().unique().tolist()))

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

    # First show Detailed Opportunities
    st.markdown("""### Detailed Opportunities""", unsafe_allow_html=True)
    
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

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # Then show Team Member Performance
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
    
    # Calculate team metrics
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

def show_week_over_week_delta():
    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h3 style='color: #2a5298; margin: 0; font-size: 1.2em; font-weight: 600;'>📊 Week-over-Week Delta Analysis</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'raw_data' not in st.session_state or 'previousweek_raw_data' not in st.session_state:
        st.warning("Please upload both current week and previous week data to view delta analysis")
        return
    
    current_df = st.session_state.raw_data
    previous_df = st.session_state.previousweek_raw_data
    
    # Get sheet names from both files
    current_sheets = list(current_df.keys()) if isinstance(current_df, dict) else ['Sheet1']
    previous_sheets = list(previous_df.keys()) if isinstance(previous_df, dict) else ['Sheet1']
    
    # Create sheet selection dropdowns
    col1, col2 = st.columns(2)
    with col1:
        current_sheet = st.selectbox("Select Current Week Sheet", options=current_sheets)
    with col2:
        previous_sheet = st.selectbox("Select Previous Week Sheet", options=previous_sheets)
    
    # Get the selected sheets
    current_data = current_df[current_sheet] if isinstance(current_df, dict) else current_df
    previous_data = previous_df[previous_sheet] if isinstance(previous_df, dict) else previous_df
    
    # Ensure both dataframes have the same structure
    required_columns = ['Organization Name', 'Opportunity Name', 'Deal Value', 'Status', 'Sales Team Member', 'Practice']
    for col in required_columns:
        if col not in current_data.columns or col not in previous_data.columns:
            st.error(f"Required column '{col}' not found in one or both datasets")
            return
    
    # Calculate metrics for current week
    current_metrics = {
        'Total Pipeline': current_data['Deal Value'].sum(),
        'Total Deals': len(current_data),
        'Closed Won': current_data[current_data['Status'] == 'Closed Won']['Deal Value'].sum(),
        'Total Deals Count': len(current_data),
        'Closed Won Count': len(current_data[current_data['Status'] == 'Closed Won'])
    }
    
    # Calculate metrics for previous week
    previous_metrics = {
        'Total Pipeline': previous_data['Deal Value'].sum(),
        'Total Deals': len(previous_data),
        'Closed Won': previous_data[previous_data['Status'] == 'Closed Won']['Deal Value'].sum(),
        'Total Deals Count': len(previous_data),
        'Closed Won Count': len(previous_data[previous_data['Status'] == 'Closed Won'])
    }
    
    # Calculate deltas
    delta_metrics = {
        'Total Pipeline': current_metrics['Total Pipeline'] - previous_metrics['Total Pipeline'],
        'Total Deals': current_metrics['Total Deals'] - previous_metrics['Total Deals'],
        'Closed Won': current_metrics['Closed Won'] - previous_metrics['Closed Won'],
        'Total Deals Count': current_metrics['Total Deals Count'] - previous_metrics['Total Deals Count'],
        'Closed Won Count': current_metrics['Closed Won Count'] - previous_metrics['Closed Won Count']
    }
    
    # Display metrics in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Pipeline",
            f"₹{current_metrics['Total Pipeline']/100000:,.0f}L",
            f"₹{delta_metrics['Total Pipeline']/100000:,.0f}L",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Total Deals",
            f"{current_metrics['Total Deals']:,}",
            f"{delta_metrics['Total Deals']:,}",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Closed Won",
            f"₹{current_metrics['Closed Won']/100000:,.0f}L",
            f"₹{delta_metrics['Closed Won']/100000:,.0f}L",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Total Deals Count",
            f"{current_metrics['Total Deals Count']:,}",
            f"{delta_metrics['Total Deals Count']:,}",
            delta_color="normal"
        )
    
    with col5:
        st.metric(
            "Closed Won Count",
            f"{current_metrics['Closed Won Count']:,}",
            f"{delta_metrics['Closed Won Count']:,}",
            delta_color="normal"
        )
    
    # Team-wise comparison
    st.subheader("Team-wise Comparison")
    current_team = current_data.groupby('Sales Team Member').agg({
        'Deal Value': 'sum',
        'Status': lambda x: (x == 'Closed Won').sum()
    }).reset_index()
    
    previous_team = previous_data.groupby('Sales Team Member').agg({
        'Deal Value': 'sum',
        'Status': lambda x: (x == 'Closed Won').sum()
    }).reset_index()
    
    # Merge current and previous data
    team_comparison = pd.merge(
        current_team,
        previous_team,
        on='Sales Team Member',
        suffixes=('_current', '_previous')
    )
    
    # Calculate deltas
    team_comparison['Pipeline Delta'] = team_comparison['Deal Value_current'] - team_comparison['Deal Value_previous']
    team_comparison['Closed Won Delta'] = team_comparison['Status_current'] - team_comparison['Status_previous']
    
    # Display team comparison
    st.dataframe(
        team_comparison.style.format({
            'Deal Value_current': '₹{:,.2f}',
            'Deal Value_previous': '₹{:,.2f}',
            'Pipeline Delta': '₹{:,.2f}',
            'Status_current': '{:,.0f}',
            'Status_previous': '{:,.0f}',
            'Closed Won Delta': '{:,.0f}'
        })
    )
    
    # Practice-wise comparison
    st.subheader("Practice-wise Comparison")
    current_practice = current_data.groupby('Practice').agg({
        'Deal Value': 'sum',
        'Status': lambda x: (x == 'Closed Won').sum()
    }).reset_index()
    
    previous_practice = previous_data.groupby('Practice').agg({
        'Deal Value': 'sum',
        'Status': lambda x: (x == 'Closed Won').sum()
    }).reset_index()
    
    # Merge current and previous data
    practice_comparison = pd.merge(
        current_practice,
        previous_practice,
        on='Practice',
        suffixes=('_current', '_previous')
    )
    
    # Calculate deltas
    practice_comparison['Pipeline Delta'] = practice_comparison['Deal Value_current'] - practice_comparison['Deal Value_previous']
    practice_comparison['Closed Won Delta'] = practice_comparison['Status_current'] - practice_comparison['Status_previous']
    
    # Display practice comparison
    st.dataframe(
        practice_comparison.style.format({
            'Deal Value_current': '₹{:,.2f}',
            'Deal Value_previous': '₹{:,.2f}',
            'Pipeline Delta': '₹{:,.2f}',
            'Status_current': '{:,.0f}',
            'Status_previous': '{:,.0f}',
            'Closed Won Delta': '{:,.0f}'
        })
    )

def main():
    # Initialize session state variables
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'raw_data' not in st.session_state:
        st.session_state.raw_data = None
    if 'previousweek_raw_data' not in st.session_state:
        st.session_state.previousweek_raw_data = None
    if 'selected_sheet' not in st.session_state:
        st.session_state.selected_sheet = None
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'data_input'
    if 'date_filter' not in st.session_state:
        st.session_state.date_filter = None
    if 'selected_practice' not in st.session_state:
        st.session_state.selected_practice = 'All'
    if 'selected_stage' not in st.session_state:
        st.session_state.selected_stage = 'All'
    if 'reset_triggered' not in st.session_state:
        st.session_state.reset_triggered = False
    if 'selected_team_member' not in st.session_state:
        st.session_state.selected_team_member = None
    
    # Keep a single "sales_target" in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0.0  # Default target in Lakhs
    
    # Sidebar for file uploads and navigation
    with st.sidebar:
        st.title("Navigation")
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Sales Team", "Detailed Data", "Week-over-Week Delta"],
            key="navigation"
        )
        st.session_state.current_view = selected.lower().replace(" ", "_")
        
        # Single data input area
        st.markdown("""
            <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
                <h3 style='color: #2a5298; margin: 0; font-size: 1.2em; font-weight: 600;'>📤 Upload Data</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Current week data upload
        uploaded_file = st.file_uploader("Upload Current Week Data", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            try:
                # Read all sheets from the Excel file
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # Show sheet selection dropdown
                selected_sheet = st.selectbox(
                    "Select Current Week Sheet",
                    options=sheet_names,
                    key="current_sheet_select"
                )
                
                # Load the selected sheet
                df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                st.session_state.df = df
                st.session_state.raw_data = {sheet: pd.read_excel(uploaded_file, sheet_name=sheet) for sheet in sheet_names}
                st.session_state.selected_sheet = selected_sheet
                st.success(f"Successfully loaded current week sheet '{selected_sheet}' with {len(df):,} records")
                
            except Exception as e:
                st.error(f"Error reading current week file: {str(e)}")
        
        # Previous week data upload
        previous_week_file = st.file_uploader("Upload Previous Week Data", type=['xlsx', 'xls'])
        if previous_week_file is not None:
            try:
                # Read all sheets from the previous week Excel file
                previous_excel_file = pd.ExcelFile(previous_week_file)
                previous_sheet_names = previous_excel_file.sheet_names
                
                # Show sheet selection dropdown for previous week
                selected_previous_sheet = st.selectbox(
                    "Select Previous Week Sheet",
                    options=previous_sheet_names,
                    key="previous_sheet_select"
                )
                
                # Load the selected sheet
                previous_df = pd.read_excel(previous_week_file, sheet_name=selected_previous_sheet)
                st.session_state.previousweek_raw_data = {sheet: pd.read_excel(previous_week_file, sheet_name=sheet) for sheet in previous_sheet_names}
                st.success(f"Successfully loaded previous week sheet '{selected_previous_sheet}' with {len(previous_df):,} records")
                
            except Exception as e:
                st.error(f"Error reading previous week file: {str(e)}")
    
    # Main content based on selected view
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "sales_team":
        show_sales_team()
    elif st.session_state.current_view == "detailed_data":
        show_detailed()
    elif st.session_state.current_view == "week_over_week_delta":
        show_week_over_week_delta()

if __name__ == "__main__":
    main()
