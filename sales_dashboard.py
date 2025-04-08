import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from functools import lru_cache

# This must be the first Streamlit command
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

# Keep a single "sales_target" in session state
if 'sales_target' not in st.session_state:
    st.session_state.sales_target = 0.0  # Default target in Lakhs

# Custom CSS for modern styling
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    @keyframes bgGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    :root {
        --card-bg: rgba(255, 255, 255, 0.65);
        --text-main: #1e1e2f;
        --text-muted: #6b7280;
        --green-glow: #00c896;
        --red-glow: #ff5b5b;
        --blue-accent: #3b82f6;
        --border-glow: rgba(59, 130, 246, 0.3);
    }

    /* Main container styling */
    .main {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(-45deg, #ff6ec4, #7873f5, #2afadf, #4c83ff, #0f2027, #203a43) !important;
        background-size: 1000% 1000% !important;
        animation: bgGradient 30s ease infinite !important;
        position: relative;
        min-height: 100vh;
        padding: 2rem;
    }

    /* Card styling with glassmorphism */
    .stCard, div.element-container, div.block-container {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        transition: all 0.3s ease !important;
    }

    /* Metric cards with enhanced styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }

    .metric-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25) !important;
    }

    /* Typography */
    h1, h2, h3, .metric-title {
        font-family: 'Poppins', sans-serif !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
    }

    /* Buttons and interactive elements */
    .stButton>button {
        background: rgba(59, 130, 246, 0.8) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        background: rgba(59, 130, 246, 0.9) !important;
        transform: translateY(-2px) !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }

    /* Charts and graphs */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }

    /* Particle background */
    #tsparticles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
</style>

<div id="tsparticles"></div>

<script>
    const themes = {
        default: {
            particles: {
                number: { value: 100, density: { enable: true, value_area: 800 } },
                color: { value: ["#00ffc3", "#00bfff", "#ffffff", "#39ff14"] },
                shape: { type: ["circle", "triangle", "star", "edge"] },
                opacity: {
                    value: 0.7,
                    anim: { enable: true, speed: 1, opacity_min: 0.3, sync: false }
                },
                size: {
                    value: 4,
                    random: true,
                    anim: { enable: true, speed: 2, size_min: 1, sync: false }
                },
                move: {
                    enable: true,
                    speed: 0.6,
                    direction: "none",
                    straight: false,
                    out_mode: "out",
                    attract: { enable: true, rotateX: 300, rotateY: 600 },
                    angle: { value: 90, offset: 0 },
                    gravity: { enable: false },
                    trail: { enable: true, length: 5, fillColor: "transparent" },
                    spin: { enable: true, acceleration: 0.05 }
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: ["grab", "bubble"] },
                    onclick: { enable: true, mode: "repulse" },
                    resize: true
                },
                modes: {
                    grab: { distance: 150, line_linked: { opacity: 0.5 } },
                    bubble: { distance: 200, size: 6, duration: 2, opacity: 0.8 },
                    repulse: { distance: 120, duration: 0.4 }
                }
            },
            retina_detect: true
        }
    };

    // Initialize particles when the document is ready
    document.addEventListener("DOMContentLoaded", function() {
        tsParticles.load("tsparticles", themes.default);
    });
</script>
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
        uploaded_file = st.file_uploader(
            "Upload Sales Data",
            type=['xlsx', 'csv'],
            help="Upload your sales data file in Excel or CSV format"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheet_name = st.selectbox("Select Worksheet", excel_file.sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
                    df = pd.read_csv(uploaded_file)
                
                st.session_state.df = df
                st.success(f"Successfully loaded {len(df):,} records")
                
                # Preview the data
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
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
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload data first.")
        return
    
    # Use current week data by default
    df = st.session_state.df_current
    st.session_state.df = df  # Set the current df in session state for compatibility
    
    st.title("Sales Performance Overview")

    # --------------------------------------------------------
    # (1) Let user edit the target as an integer
    # --------------------------------------------------------
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

def show_ytd_dashboard():
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload data first.")
        return
    
    df_current = st.session_state.df_current
    df_previous = st.session_state.df_previous
    
    # Modern header with glassmorphism effect
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(30, 60, 114, 0.95) 0%, rgba(42, 82, 152, 0.95) 100%);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 2rem;
        '>
            <h1 style='
                color: white;
                margin: 0;
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                letter-spacing: 1px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            '>YTD Performance Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Enhanced filters section with 6 columns
    st.markdown("### 🎯 Filters")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        sales_owners = ["All"] + sorted(df_current['Sales Owner'].dropna().unique().tolist()) if 'Sales Owner' in df_current.columns else ["All"]
        selected_owner = st.selectbox("Sales Owner", sales_owners)
    
    with col2:
        # Try different possible column names for P&L Centre/Practice
        practice_column = next((col for col in ['P&L Centre', 'Practice', 'Business Unit', 'Department'] 
                              if col in df_current.columns), None)
        if practice_column:
            practices = ["All"] + sorted(df_current[practice_column].dropna().unique().tolist())
            selected_practice = st.selectbox(practice_column, practices)
        else:
            selected_practice = "All"
            st.warning("Practice/P&L Centre column not found")
    
    with col3:
        types = ["All"] + sorted(df_current['Type'].dropna().unique().tolist()) if 'Type' in df_current.columns else ["All"]
        selected_type = st.selectbox("Type", types)
    
    with col4:
        # Try different possible column names for Status
        status_column = next((col for col in ['Status', 'Sales Stage', 'Stage'] 
                            if col in df_current.columns), None)
        if status_column:
            statuses = ["All"] + sorted(df_current[status_column].dropna().unique().tolist())
            selected_status = st.selectbox(status_column, statuses)
        else:
            selected_status = "All"
            st.warning("Status column not found")
    
    with col5:
        geographies = ["All"] + sorted(df_current['Geography'].dropna().unique().tolist()) if 'Geography' in df_current.columns else ["All"]
        selected_geography = st.selectbox("Geography", geographies)
    
    with col6:
        years = ["All"]
        if 'Year' in df_current.columns:
            years.extend(sorted(df_current['Year'].dropna().unique().tolist()))
        elif 'Expected Close Date' in df_current.columns:
            df_current['Year'] = pd.to_datetime(df_current['Expected Close Date'], dayfirst=True).dt.year
            years.extend(sorted(df_current['Year'].dropna().unique().tolist()))
        selected_year = st.selectbox("Fiscal Year", years)
    
    # Filter data based on selections
    def filter_data(df):
        filtered_df = df.copy()
        
        if 'Sales Owner' in df.columns and selected_owner != "All":
            filtered_df = filtered_df[filtered_df['Sales Owner'] == selected_owner]
        
        if practice_column and selected_practice != "All":
            filtered_df = filtered_df[filtered_df[practice_column] == selected_practice]
        
        if 'Type' in df.columns and selected_type != "All":
            filtered_df = filtered_df[filtered_df['Type'] == selected_type]
        
        if status_column and selected_status != "All":
            filtered_df = filtered_df[filtered_df[status_column] == selected_status]
        
        if 'Geography' in df.columns and selected_geography != "All":
            filtered_df = filtered_df[filtered_df['Geography'] == selected_geography]
        
        if selected_year != "All":
            if 'Year' in df.columns:
                filtered_df = filtered_df[filtered_df['Year'] == selected_year]
            elif 'Expected Close Date' in df.columns:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['Expected Close Date'], dayfirst=True).dt.year == selected_year]
            
        return filtered_df
    
    df_current_filtered = filter_data(df_current)
    df_previous_filtered = filter_data(df_previous)
    
    # Define metrics dictionary with enhanced styling and animations
    metrics = {
        'Total Pipeline': {
            'icon': '📈',
            'current': df_current_filtered['Amount'].sum() / 100000,
            'previous': df_previous_filtered['Amount'].sum() / 100000,
            'description': 'Total pipeline value across all stages',
            'gradient': 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
            'trend_icon': '↗️' if (df_current_filtered['Amount'].sum() / 100000) > (df_previous_filtered['Amount'].sum() / 100000) else '↘️'
        },
        'Closed Won': {
            'icon': '🎯',
            'current': df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000 if status_column else 0,
            'previous': df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000 if status_column else 0,
            'description': 'Successfully closed deals',
            'gradient': 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
            'trend_icon': '↗️' if (df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000) > (df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000) else '↘️' if status_column else '➖'
        },
        'Win Rate': {
            'icon': '🏆',
            'current': (len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]) / len(df_current_filtered) * 100) if status_column and len(df_current_filtered) > 0 else 0,
            'previous': (len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]) / len(df_previous_filtered) * 100) if status_column and len(df_previous_filtered) > 0 else 0,
            'description': 'Deal success rate',
            'gradient': 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
            'trend_icon': '↗️' if ((len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]) / len(df_current_filtered) * 100) if status_column and len(df_current_filtered) > 0 else 0) > ((len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]) / len(df_previous_filtered) * 100) if status_column and len(df_previous_filtered) > 0 else 0) else '↘️'
        },
        'Average Deal Size': {
            'icon': '💰',
            'current': (df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)])) / 100000 if status_column and len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]) > 0 else 0,
            'previous': (df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)])) / 100000 if status_column and len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]) > 0 else 0,
            'description': 'Average value per won deal',
            'gradient': 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
            'trend_icon': '↗️' if ((df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)])) / 100000 if status_column and len(df_current_filtered[df_current_filtered[status_column].str.contains('Won', case=False, na=False)]) > 0 else 0) > ((df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]['Amount'].sum() / len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)])) / 100000 if status_column and len(df_previous_filtered[df_previous_filtered[status_column].str.contains('Won', case=False, na=False)]) > 0 else 0) else '↘️'
        }
    }

    # Key Metrics Section with ultra-modern design
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(17, 25, 40, 0.95) 0%, rgba(28, 41, 66, 0.95) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 2rem;
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 1.5rem 0 2.5rem 0;
            position: relative;
            overflow: hidden;
        '>
            <div class='glow-effect' style='
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
                animation: glow 8s linear infinite;
            '></div>
            <h2 style='
                color: white;
                margin-bottom: 0;
                text-align: center;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: 1.2px;
                background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                position: relative;
            '>📊 Key Performance Metrics</h2>
        </div>
        <style>
            @keyframes glow {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .metric-card {
                animation: fadeIn 0.6s ease-out forwards;
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.2);
            }
            .trend-icon {
                transition: all 0.3s ease;
            }
            .metric-card:hover .trend-icon {
                transform: scale(1.2);
            }
            .pulse-animation {
                animation: pulse 2s infinite;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Display enhanced metric cards with modern design
    metric_cols = st.columns(len(metrics))
    for col, (metric_name, data) in zip(metric_cols, metrics.items()):
        with col:
            delta = data['current'] - data['previous']
            delta_color = "normal" if delta >= 0 else "inverse"
            
            st.markdown(f"""
                <div class='metric-card' style='
                    background: {data['gradient']};
                    border-radius: 20px;
                    padding: 2rem;
                    height: 100%;
                    position: relative;
                    overflow: hidden;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                '>
                    <div class='trend-icon' style='
                        position: absolute;
                        top: 15px;
                        right: 15px;
                        font-size: 1.8rem;
                        opacity: 0.9;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    '>{data['trend_icon']}</div>
                    <div style='
                        font-size: 2.2rem;
                        margin-bottom: 1rem;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    '>{data['icon']}</div>
                    <h3 style='
                        color: white;
                        font-size: 1.3rem;
                        margin-bottom: 0.8rem;
                        font-weight: 700;
                        letter-spacing: 0.5px;
                    '>{metric_name}</h3>
                    <div class='pulse-animation' style='
                        color: white;
                        font-size: 2.2rem;
                        font-weight: 800;
                        margin: 1rem 0;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        letter-spacing: 0.5px;
                    '>{format_metric(data['current'], metric_name)}</div>
                    <div style='
                        color: {'#4ADE80' if delta >= 0 else '#F87171'};
                        font-size: 1.1rem;
                        font-weight: 600;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        margin: 0.8rem 0;
                    '>
                        <span style='
                            background: rgba(255,255,255,0.1);
                            padding: 0.4rem 0.8rem;
                            border-radius: 12px;
                            backdrop-filter: blur(5px);
                            -webkit-backdrop-filter: blur(5px);
                        '>
                            {format_metric(abs(delta), metric_name)}
                            <span style='margin-left: 4px;'>{' ⬆️' if delta >= 0 else ' ⬇️'}</span>
                        </span>
                    </div>
                    <div style='
                        color: rgba(255, 255, 255, 0.9);
                        font-size: 1rem;
                        font-weight: 500;
                        margin-top: 0.8rem;
                        letter-spacing: 0.3px;
                        line-height: 1.4;
                    '>{data['description']}</div>
                    <div class='sparkline-container' style='
                        margin-top: 1.5rem;
                        padding: 0.8rem;
                        background: rgba(255,255,255,0.1);
                        border-radius: 12px;
                        backdrop-filter: blur(5px);
                        -webkit-backdrop-filter: blur(5px);
                    '>
                </div>
            """, unsafe_allow_html=True)
            
            # Add enhanced sparkline charts
            if metric_name in ['Total Pipeline', 'Closed Won']:
                values = [data['previous'], data['current']]
                trend_chart = go.Figure(go.Scatter(
                    y=values,
                    mode='lines+markers',
                    line=dict(
                        color='white',
                        width=3,
                        shape='spline',
                        smoothing=1.3
                    ),
                    marker=dict(
                        color='white',
                        size=8,
                        symbol='diamond',
                        line=dict(
                            color='rgba(255,255,255,0.5)',
                            width=2
                        )
                    ),
                    fill='tonexty',
                    fillcolor='rgba(255,255,255,0.1)'
                ))
                trend_chart.update_layout(
                    height=80,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    xaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        showline=False,
                        zeroline=False
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        showline=False,
                        zeroline=False
                    ),
                    hovermode=False
                )
                st.plotly_chart(trend_chart, use_container_width=True, config={'displayModeBar': False})

def format_metric(value, metric_type):
    """Helper function to format metric values"""
    if metric_type in ['Total Pipeline', 'Closed Won', 'Avg Deal Size']:
        return f"₹{abs(value):.0f}L"
    elif metric_type == 'Win Rate':
        return f"{abs(value):.1f}%"
    return f"{abs(value):.0f}"

def display_dashboard():
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload the data first!")
        return

    df_current = st.session_state.df_current
    df_previous = st.session_state.df_previous

    # Modern Header with Gradient
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        '>
            <h1 style='
                color: white;
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            '>Sales Performance Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)

    # Enhanced Filter Section
    st.markdown("""
        <div style='
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        '>
            <h3 style='
                color: #1e3c72;
                margin: 0 0 1rem 0;
                font-size: 1.3rem;
                font-weight: 600;
            '>📊 Filter Dashboard</h3>
        </div>
    """, unsafe_allow_html=True)

    # Organized Filters in Two Rows
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        sales_owners = sorted(df_current['Sales Owner'].dropna().unique().tolist())
        selected_sales_owner = st.selectbox("👤 Sales Owner", ["All Sales Owners"] + sales_owners)

    with col2:
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        selected_quarter = st.selectbox("📅 Quarter", ["All Quarters"] + quarters)

    with col3:
        practices = sorted(df_current['Practice'].dropna().unique().tolist())
        selected_practice = st.selectbox("🏢 Practice", ["All Practices"] + practices)

    # Apply Filters
    if selected_sales_owner != "All Sales Owners":
        df_current = df_current[df_current['Sales Owner'] == selected_sales_owner]
        df_previous = df_previous[df_previous['Sales Owner'] == selected_sales_owner]

    if selected_quarter != "All Quarters":
        df_current = df_current[df_current['Quarter'] == selected_quarter]
        df_previous = df_previous[df_previous['Quarter'] == selected_quarter]

    if selected_practice != "All Practices":
        df_current = df_current[df_current['Practice'] == selected_practice]
        df_previous = df_previous[df_previous['Practice'] == selected_practice]

    # Calculate Metrics
    metrics = {
        'Committed': {
            'current': df_current[df_current['Status'] == "Committed for the Month"]['Amount'].sum() / 100000,
            'previous': df_previous[df_previous['Status'] == "Committed for the Month"]['Amount'].sum() / 100000,
            'icon': '🎯',
            'color': '#4CAF50'
        },
        'Upside': {
            'current': df_current[df_current['Status'] == "Upside for the Month"]['Amount'].sum() / 100000,
            'previous': df_previous[df_previous['Status'] == "Upside for the Month"]['Amount'].sum() / 100000,
            'icon': '📈',
            'color': '#2196F3'
        },
        'Closed Won': {
            'current': df_current[df_current['Status'] == "Closed Won"]['Amount'].sum() / 100000,
            'previous': df_previous[df_previous['Status'] == "Closed Won"]['Amount'].sum() / 100000,
            'icon': '💰',
            'color': '#9C27B0'
        }
    }

    # Calculate Overall Metrics
    overall_current = metrics['Committed']['current'] + metrics['Closed Won']['current']
    overall_previous = metrics['Committed']['previous'] + metrics['Closed Won']['previous']
    overall_delta = overall_current - overall_previous

    # Display Metrics in Modern Cards
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    for metric_name, data in metrics.items():
        delta = data['current'] - data['previous']
        delta_percent = (delta / data['previous'] * 100) if data['previous'] != 0 else 0

        st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-bottom: 1.5rem;
                border: 1px solid rgba(0,0,0,0.05);
            '>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='
                            font-size: 1.8rem;
                            margin-bottom: 0.5rem;
                        '>{data['icon']} {metric_name}</div>
                        <div style='
                            font-size: 2.2rem;
                            font-weight: 700;
                            color: {data['color']};
                        '>₹{data['current']:,.0f}L</div>
                        <div style='
                            color: #666;
                            font-size: 1.1rem;
                            margin-top: 0.5rem;
                        '>Previous: ₹{data['previous']:,.0f}L</div>
                    </div>
                    <div style='
                        background: {'rgba(76, 175, 80, 0.1)' if delta >= 0 else 'rgba(244, 67, 54, 0.1)'};
                        padding: 1rem;
                        border-radius: 12px;
                        text-align: center;
                        min-width: 120px;
                    '>
                        <div style='
                            font-size: 1.4rem;
                            font-weight: 600;
                            color: {'#4CAF50' if delta >= 0 else '#F44336'};
                        '>{'+' if delta >= 0 else ''}{delta:,.0f}L</div>
                        <div style='
                            font-size: 1rem;
                            color: {'#4CAF50' if delta >= 0 else '#F44336'};
                        '>{'+' if delta_percent >= 0 else ''}{delta_percent:.1f}%</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Overall Metrics Card
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin-top: 2rem;
            color: white;
        '>
            <div style='text-align: center;'>
                <div style='font-size: 1.8rem; margin-bottom: 1rem;'>📊 Overall Performance</div>
                <div style='font-size: 2.5rem; font-weight: 700;'>₹{overall_current:,.0f}L</div>
                <div style='
                    display: inline-block;
                    margin-top: 1rem;
                    padding: 0.5rem 1rem;
                    background: {'rgba(76, 175, 80, 0.2)' if overall_delta >= 0 else 'rgba(244, 67, 54, 0.2)'};
                    border-radius: 8px;
                    font-weight: 600;
                '>
                    {'+' if overall_delta >= 0 else ''}{overall_delta:,.0f}L from previous
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add Pipeline Trend Chart
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Pipeline Trend Analysis")

    # Prepare data for trend chart
    trend_data = pd.DataFrame({
        'Category': ['Committed', 'Upside', 'Closed Won'] * 2,
        'Period': ['Previous'] * 3 + ['Current'] * 3,
        'Amount': [
            metrics['Committed']['previous'],
            metrics['Upside']['previous'],
            metrics['Closed Won']['previous'],
            metrics['Committed']['current'],
            metrics['Upside']['current'],
            metrics['Closed Won']['current']
        ]
    })

    fig = px.bar(
        trend_data,
        x='Category',
        y='Amount',
        color='Period',
        barmode='group',
        title='Pipeline Comparison',
        color_discrete_map={'Current': '#1e3c72', 'Previous': '#2a5298'},
        labels={'Amount': 'Amount (Lakhs)', 'Category': ''}
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

def display_data_input():
    st.title("Data Input")
    st.write("Please upload your Excel file containing both current and previous week data in different sheets.")

    # Single file upload for Excel
    uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx'], key='excel_file')

    if uploaded_file is not None:
        try:
            # Read the Excel file and get sheet names
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names

            # Sheet selection for current week
            current_week_sheet = st.selectbox(
                "Select Current Week Sheet",
                options=sheet_names,
                key="current_week_sheet"
            )

            # Sheet selection for previous week
            previous_week_sheet = st.selectbox(
                "Select Previous Week Sheet",
                options=sheet_names,
                key="previous_week_sheet"
            )

            if current_week_sheet == previous_week_sheet:
                st.warning("Please select different sheets for current and previous week data.")
                return

            # Read the selected sheets
            df_current = pd.read_excel(uploaded_file, sheet_name=current_week_sheet)
            df_previous = pd.read_excel(uploaded_file, sheet_name=previous_week_sheet)

            # Store the dataframes in session state
            st.session_state.df_current = df_current
            st.session_state.df_previous = df_previous

            # Show success message
            st.success("Data uploaded successfully!")

            # Preview the data
            st.subheader("Current Week Data Preview")
            st.dataframe(df_current.head(), use_container_width=True)

            st.subheader("Previous Week Data Preview")
            st.dataframe(df_previous.head(), use_container_width=True)

        except Exception as e:
            st.error(f"Error reading the files: {str(e)}")
    else:
        st.info("Please upload both current and previous week data files to proceed.")

def show_pipeline_analysis():
    """Advanced Pipeline Analysis View"""
    if 'df_current' not in st.session_state:
        st.warning("Please upload data first.")
        return

    df = st.session_state.df_current

    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        '>
            <h2 style='
                color: white;
                text-align: center;
                font-size: 2.2rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            '>Pipeline Analysis</h2>
        </div>
    """, unsafe_allow_html=True)

    # Advanced Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        probability_range = st.slider("Probability Range", 0, 100, (0, 100), 5)
    with col2:
        amount_range = st.slider("Deal Size (Lakhs)", 
                               int(df['Amount'].min()/100000), 
                               int(df['Amount'].max()/100000), 
                               (int(df['Amount'].min()/100000), int(df['Amount'].max()/100000)))
    with col3:
        timeline = st.selectbox("Timeline", ["Next Quarter", "Next 6 Months", "Next Year", "All"])

    # Filter data
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['Probability'].between(probability_range[0], probability_range[1])) &
        (filtered_df['Amount'].between(amount_range[0]*100000, amount_range[1]*100000))
    ]

    # Pipeline Funnel
    stages = filtered_df['Sales Stage'].value_counts()
    fig_funnel = go.Figure(go.Funnel(
        y=stages.index,
        x=stages.values,
        textinfo="value+percent initial",
        textposition="inside",
        textfont=dict(size=16, color="white"),
        marker=dict(
            color=["#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#F44336"]
        )
    ))
    fig_funnel.update_layout(
        title="Pipeline Funnel Analysis",
        height=500,
        showlegend=False
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    # Probability Distribution
    col1, col2 = st.columns(2)
    with col1:
        prob_dist = filtered_df.groupby(pd.cut(filtered_df['Probability'], 
                                             bins=[0, 25, 50, 75, 100]))['Amount'].sum()/100000
        fig_prob = px.bar(
            x=["0-25%", "26-50%", "51-75%", "76-100%"],
            y=prob_dist.values,
            title="Pipeline by Probability",
            labels={"x": "Probability Range", "y": "Amount (Lakhs)"}
        )
        fig_prob.update_traces(marker_color='#2196F3')
        st.plotly_chart(fig_prob, use_container_width=True)

    with col2:
        timeline_dist = filtered_df.groupby(pd.Grouper(key='Expected Close Date', freq='M'))['Amount'].sum()/100000
        fig_timeline = px.line(
            x=timeline_dist.index,
            y=timeline_dist.values,
            title="Pipeline Timeline",
            labels={"x": "Month", "y": "Amount (Lakhs)"}
        )
        fig_timeline.update_traces(line_color='#4CAF50')
        st.plotly_chart(fig_timeline, use_container_width=True)

def main():
    # Initialize session state for navigation if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Data Input"

    # Sidebar navigation with new views
    st.sidebar.title("Navigation")
    
    # First check if data is uploaded
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.session_state.current_page = "Data Input"
    else:
        st.session_state.current_page = st.sidebar.radio(
            "Select a page",
            ["Data Input", "Dashboard", "Overview", "Sales Team", "Pipeline Analysis", 
             "YTD Dashboard", "Detailed Data"]
        )

    # Display the selected page
    if st.session_state.current_page == "Data Input":
        display_data_input()
    elif st.session_state.current_page == "Dashboard":
        display_dashboard()
    elif st.session_state.current_page == "Overview":
        show_overview()
    elif st.session_state.current_page == "Sales Team":
        show_sales_team()
    elif st.session_state.current_page == "Pipeline Analysis":
        show_pipeline_analysis()
    elif st.session_state.current_page == "YTD Dashboard":
        show_ytd_dashboard()
    elif st.session_state.current_page == "Detailed Data":
        show_detailed()

if __name__ == "__main__":
    main()
