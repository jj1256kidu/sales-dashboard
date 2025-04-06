import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from auth import check_password, init_session_state, show_login_page
from functools import lru_cache
import time

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

# Custom CSS for the dashboard
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

def show_data_input_view():
    """Display the data input view"""
    st.title("Data Input")
    
    # File upload section
    st.markdown("### Upload Data File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Manual input section
    st.markdown("### Manual Data Input")
    with st.form("manual_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            practice = st.text_input("Practice")
            team = st.text_input("Team")
            sales_stage = st.selectbox(
                "Sales Stage",
                options=["Prospecting", "Qualification", "Needs Analysis", "Value Proposition", "Negotiation", "Closed Won", "Closed Lost"]
            )
            amount = st.number_input("Amount", min_value=0)
        
        with col2:
            expected_close_date = st.date_input("Expected Close Date")
            probability = st.slider("Probability (%)", min_value=0, max_value=100, value=50)
            notes = st.text_area("Notes")
        
        submit_button = st.form_submit_button("Add Data")
    
    if submit_button:
        # Create new row
        new_row = {
            "Practice": practice,
            "Team": team,
            "Sales Stage": sales_stage,
            "Amount": amount,
            "Expected Close Date": expected_close_date,
            "Probability": probability,
            "Notes": notes
        }
        
        # Add to dataframe
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame(columns=new_row.keys())
        
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Data added successfully!")
    
    # Display current data
    if 'df' in st.session_state and not st.session_state.df.empty:
        st.markdown("### Current Data")
        st.dataframe(st.session_state.df, use_container_width=True)
        
        # Download button
        csv = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="Download Data",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )

def show_overview_view(df):
    """Display the overview view"""
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Overview")
    df = process_data(df)

    # Sales Target Section
    st.markdown("### Enter Your Sales Target (Optional)")
    default_target = str(int(st.session_state.get("sales_target", 0)))
    user_target_input = st.text_input("Sales Target (in Lakhs)", value=default_target)
    
    try:
        user_target = int(user_target_input)
    except ValueError:
        user_target = 0
    
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

    # Practice Section
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

def show_sales_team_view(df):
    """Display the sales team performance view"""
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Team Performance")
    df = process_data(df)

    # Team Selection
    if 'Team' in df.columns:
        teams = ['All'] + sorted(df['Team'].dropna().unique().tolist())
        selected_team = st.selectbox(
            "Select Team",
            options=teams,
            key="team_filter"
        )
        
        # Filter data based on selected team
        df_team = df.copy()
        if selected_team != 'All':
            df_team = df_team[df_team['Team'] == selected_team]
        
        # Calculate team metrics
        team_metrics = df_team.groupby('Team').agg({
            'Amount': lambda x: x[df_team['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
            'Sales Stage': lambda x: x[df_team['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        team_metrics.columns = ['Team', 'Closed Amount', 'Closed Deals']
        
        # Pipeline by team
        pipeline_df = df_team[~df_team['Sales Stage'].str.contains('Won', case=False, na=False)]
        total_pipeline = pipeline_df.groupby('Team')['Amount'].sum() / 100000
        team_metrics['Total Pipeline'] = team_metrics['Team'].map(total_pipeline)
        
        # Pipeline deal counts
        total_deals = pipeline_df.groupby('Team').size()
        team_metrics['Pipeline Deals'] = team_metrics['Team'].map(total_deals)
        
        # Sort by pipeline
        team_metrics = team_metrics.sort_values('Total Pipeline', ascending=False)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pipeline = go.Figure()
            fig_pipeline.add_trace(go.Bar(
                x=team_metrics['Team'],
                y=team_metrics['Total Pipeline'],
                name='Pipeline',
                text=team_metrics['Total Pipeline'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_pipeline.add_trace(go.Bar(
                x=team_metrics['Team'],
                y=team_metrics['Closed Amount'],
                name='Closed Won',
                text=team_metrics['Closed Amount'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_pipeline.update_layout(
                title=dict(
                    text="Team-wise Pipeline vs Closed Won",
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
                    text="Team",
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
                x=team_metrics['Team'],
                y=team_metrics['Pipeline Deals'],
                name='Pipeline Deals',
                text=team_metrics['Pipeline Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_deals.add_trace(go.Bar(
                x=team_metrics['Team'],
                y=team_metrics['Closed Deals'],
                name='Closed Deals',
                text=team_metrics['Closed Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_deals.update_layout(
                title=dict(
                    text="Team-wise Pipeline vs Closed Deals",
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
                    text="Team",
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
        
        # Team summary
        st.markdown("### Team Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pipeline_val = team_metrics['Total Pipeline'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Pipeline</div>
                    <div class='metric-value'>₹{int(total_pipeline_val)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_deals_count = team_metrics['Pipeline Deals'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Pipeline Deals</div>
                    <div class='metric-value'>{int(total_deals_count)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Active opportunities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_won = team_metrics['Closed Deals'].sum()
            win_rate = (total_won / (total_won + total_deals_count) * 100) if (total_won + total_deals_count) > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Win Rate</div>
                    <div class='metric-value'>{int(win_rate)}%</div>
                    <div style='color: #666; font-size: 0.9em;'>{int(total_won)} won</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_deal_size = team_metrics['Closed Amount'].sum() / total_won if total_won > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Avg Deal Size</div>
                    <div class='metric-value'>₹{int(avg_deal_size)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Team-wise table
        st.markdown("### Team-wise Details")
        summary_data = team_metrics.copy()
        summary_data['Win Rate'] = (summary_data['Closed Deals'] / (summary_data['Closed Deals'] + summary_data['Pipeline Deals']) * 100).round(1)
        summary_data['Closed Amount'] = summary_data['Closed Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Total Pipeline'] = summary_data['Total Pipeline'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{int(x)}%")
        
        st.dataframe(
            summary_data[['Team', 'Closed Amount', 'Total Pipeline', 'Closed Deals', 'Pipeline Deals', 'Win Rate']],
            use_container_width=True
        )
    else:
        st.error("Team column not found in the dataset")

def show_detailed_data_view(df):
    """Display the detailed data view with filters and data table"""
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Detailed Data View")
    df = process_data(df)

    # Filters
    st.markdown("### Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        practice_filter = st.multiselect(
            "Practice",
            options=['All'] + sorted(df['Practice'].dropna().unique().tolist()),
            default=['All']
        )
    
    with col2:
        team_filter = st.multiselect(
            "Team",
            options=['All'] + sorted(df['Sales Owner'].dropna().unique().tolist()),
            default=['All']
        )
    
    with col3:
        stage_filter = st.multiselect(
            "Sales Stage",
            options=['All'] + sorted(df['Sales Stage'].dropna().unique().tolist()),
            default=['All']
        )
    
    # Apply filters
    filtered_df = df.copy()
    if 'All' not in practice_filter:
        filtered_df = filtered_df[filtered_df['Practice'].isin(practice_filter)]
    if 'All' not in team_filter:
        filtered_df = filtered_df[filtered_df['Sales Owner'].isin(team_filter)]
    if 'All' not in stage_filter:
        filtered_df = filtered_df[filtered_df['Sales Stage'].isin(stage_filter)]
    
    # Summary metrics
    st.markdown("### Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pipeline = filtered_df[~filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Total Pipeline</div>
                <div class='metric-value'>₹{int(total_pipeline)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_deals = len(filtered_df[~filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)])
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Pipeline Deals</div>
                <div class='metric-value'>{int(total_deals)}</div>
                <div style='color: #666; font-size: 0.9em;'>Active opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_won = len(filtered_df[filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)])
        win_rate = (total_won / (total_won + total_deals) * 100) if (total_won + total_deals) > 0 else 0
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Win Rate</div>
                <div class='metric-value'>{int(win_rate)}%</div>
                <div style='color: #666; font-size: 0.9em;'>{int(total_won)} won</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_deal_size = filtered_df[filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / (100000 * total_won) if total_won > 0 else 0
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Avg Deal Size</div>
                <div class='metric-value'>₹{int(avg_deal_size)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Data table
    st.markdown("### Detailed Data")
    display_df = filtered_df.copy()
    display_df['Amount'] = display_df['Amount'].apply(lambda x: f"₹{int(x/100000)}L")
    display_df['Probability'] = display_df['Probability'].apply(lambda x: f"{int(x)}%")
    
    st.dataframe(
        display_df,
        use_container_width=True
    )

def show_quarterly_summary(df):
    """Display the quarterly summary view"""
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Quarterly Summary")
    df = process_data(df)

    # Quarter selection
    current_year = pd.Timestamp.now().year
    quarters = [f"Q{i} {current_year}" for i in range(1, 5)]
    selected_quarter = st.selectbox(
        "Select Quarter",
        options=quarters,
        key="quarter_filter"
    )
    
    # Extract quarter and year
    quarter = int(selected_quarter.split()[0][1])
    year = int(selected_quarter.split()[1])
    
    # Filter data for selected quarter
    start_date = pd.Timestamp(year=year, month=(quarter-1)*3+1, day=1)
    end_date = start_date + pd.DateOffset(months=3) - pd.DateOffset(days=1)
    
    quarter_data = df[
        (df['Expected Close Date'] >= start_date) & 
        (df['Expected Close Date'] <= end_date)
    ]
    
    # Calculate metrics
    total_pipeline = quarter_data[~quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
    closed_won = quarter_data[quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
    total_deals = len(quarter_data)
    win_rate = (len(quarter_data[quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)]) / total_deals * 100) if total_deals > 0 else 0
    
    # Display metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Total Pipeline</div>
                <div class='metric-value'>₹{int(total_pipeline)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Closed Won</div>
                <div class='metric-value'>₹{int(closed_won)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Won deals value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Total Deals</div>
                <div class='metric-value'>{int(total_deals)}</div>
                <div style='color: #666; font-size: 0.9em;'>Number of deals</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Win Rate</div>
                <div class='metric-value'>{int(win_rate)}%</div>
                <div style='color: #666; font-size: 0.9em;'>Success rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Practice-wise summary
    st.markdown("### Practice-wise Summary")
    practice_metrics = quarter_data.groupby('Practice').agg({
        'Amount': lambda x: x[quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
        'Sales Stage': lambda x: x[quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)].count()
    }).reset_index()
    
    practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
    
    # Pipeline by practice
    pipeline_df = quarter_data[~quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)]
    total_pipeline = pipeline_df.groupby('Practice')['Amount'].sum() / 100000
    practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
    
    # Pipeline deal counts
    total_deals = pipeline_df.groupby('Practice').size()
    practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals)
    
    # Sort by pipeline
    practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
    
    # Display practice metrics
    st.dataframe(
        practice_metrics,
        use_container_width=True
    )
    
    # Monthly trend
    st.markdown("### Monthly Trend")
    monthly_data = quarter_data.groupby(quarter_data['Expected Close Date'].dt.to_period('M')).agg({
        'Amount': 'sum',
        'Sales Stage': lambda x: x[quarter_data['Sales Stage'].str.contains('Won', case=False, na=False)].count()
    }).reset_index()
    
    monthly_data['Expected Close Date'] = monthly_data['Expected Close Date'].astype(str)
    monthly_data['Amount'] = monthly_data['Amount'] / 100000
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly_data['Expected Close Date'],
        y=monthly_data['Amount'],
        name='Amount',
        text=monthly_data['Amount'].apply(lambda x: f"₹{int(x)}L"),
        textposition='outside',
        textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
        marker_color='#4A90E2',
        marker_line=dict(color='#357ABD', width=2),
        opacity=0.9
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['Expected Close Date'],
        y=monthly_data['Sales Stage'],
        name='Closed Deals',
        mode='lines+markers',
        line=dict(width=3, color='#2ecc71'),
        marker=dict(size=8, color='#2ecc71'),
        text=monthly_data['Sales Stage'],
        textposition='top center',
        textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold')
    ))
    
    fig_trend.update_layout(
        title=dict(
            text="Monthly Trend",
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
            text="Month",
            font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
            standoff=15
        ),
        yaxis_title=dict(
            text="Amount (Lakhs) / Number of Deals",
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
    
    st.plotly_chart(fig_trend, use_container_width=True)

def show_previous_data_view(df):
    """Display the previous data view"""
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Previous Data View")
    df = process_data(df)

    # Year selection
    current_year = pd.Timestamp.now().year
    years = list(range(current_year - 5, current_year))
    selected_year = st.selectbox(
        "Select Year",
        options=years,
        key="year_filter"
    )
    
    # Filter data for selected year
    year_data = df[df['Expected Close Date'].dt.year == selected_year]
    
    # Calculate metrics
    total_pipeline = year_data[~year_data['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
    closed_won = year_data[year_data['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
    total_deals = len(year_data)
    win_rate = (len(year_data[year_data['Sales Stage'].str.contains('Won', case=False, na=False)]) / total_deals * 100) if total_deals > 0 else 0
    
    # Display metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Total Pipeline</div>
                <div class='metric-value'>₹{int(total_pipeline)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Closed Won</div>
                <div class='metric-value'>₹{int(closed_won)}L</div>
                <div style='color: #666; font-size: 0.9em;'>Won deals value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Total Deals</div>
                <div class='metric-value'>{int(total_deals)}</div>
                <div style='color: #666; font-size: 0.9em;'>Number of deals</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                <div class='metric-label'>Win Rate</div>
                <div class='metric-value'>{int(win_rate)}%</div>
                <div style='color: #666; font-size: 0.9em;'>Success rate</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Quarterly trend
    st.markdown("### Quarterly Trend")
    quarterly_data = year_data.groupby(year_data['Expected Close Date'].dt.quarter).agg({
        'Amount': 'sum',
        'Sales Stage': lambda x: x[year_data['Sales Stage'].str.contains('Won', case=False, na=False)].count()
    }).reset_index()
    
    quarterly_data['Expected Close Date'] = quarterly_data['Expected Close Date'].apply(lambda x: f"Q{x}")
    quarterly_data['Amount'] = quarterly_data['Amount'] / 100000
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=quarterly_data['Expected Close Date'],
        y=quarterly_data['Amount'],
        name='Amount',
        text=quarterly_data['Amount'].apply(lambda x: f"₹{int(x)}L"),
        textposition='outside',
        textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
        marker_color='#4A90E2',
        marker_line=dict(color='#357ABD', width=2),
        opacity=0.9
    ))
    fig_trend.add_trace(go.Scatter(
        x=quarterly_data['Expected Close Date'],
        y=quarterly_data['Sales Stage'],
        name='Closed Deals',
        mode='lines+markers',
        line=dict(width=3, color='#2ecc71'),
        marker=dict(size=8, color='#2ecc71'),
        text=quarterly_data['Sales Stage'],
        textposition='top center',
        textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold')
    ))
    
    fig_trend.update_layout(
        title=dict(
            text="Quarterly Trend",
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
            text="Quarter",
            font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
            standoff=15
        ),
        yaxis_title=dict(
            text="Amount (Lakhs) / Number of Deals",
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
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Practice-wise summary
    st.markdown("### Practice-wise Summary")
    practice_metrics = year_data.groupby('Practice').agg({
        'Amount': lambda x: x[year_data['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
        'Sales Stage': lambda x: x[year_data['Sales Stage'].str.contains('Won', case=False, na=False)].count()
    }).reset_index()
    
    practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
    
    # Pipeline by practice
    pipeline_df = year_data[~year_data['Sales Stage'].str.contains('Won', case=False, na=False)]
    total_pipeline = pipeline_df.groupby('Practice')['Amount'].sum() / 100000
    practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
    
    # Pipeline deal counts
    total_deals = pipeline_df.groupby('Practice').size()
    practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals)
    
    # Sort by pipeline
    practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
    
    # Display practice metrics
    st.dataframe(
        practice_metrics,
        use_container_width=True
    ) 

def show_login_page():
    """Display the login page"""
    st.title("Sales Dashboard Login")
    
    # Check if account is locked
    current_time = time.time()
    if st.session_state.locked_until > current_time:
        remaining_time = int(st.session_state.locked_until - current_time)
        st.error(f"Account locked. Please try again in {remaining_time} seconds.")
        return
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
    
    if submit_button:
        # Check credentials
        if username == "admin" and password == "admin":
            st.session_state.is_logged_in = True
            st.session_state.login_attempts = 0
            st.session_state.last_attempt = 0
            st.session_state.locked_until = 0
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.session_state.login_attempts += 1
            st.session_state.last_attempt = current_time
            
            # Check if too many attempts
            if st.session_state.login_attempts >= 3:
                st.session_state.locked_until = current_time + 300  # Lock for 5 minutes
                st.error("Too many failed attempts. Account locked for 5 minutes.")
            else:
                st.error("Invalid credentials. Please try again.")
