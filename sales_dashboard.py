import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io

# Set page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
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
</style>
""", unsafe_allow_html=True)

def show_data_input():
    # Custom header
    st.markdown("""
        <div class="custom-header">
            <h1>📊 Sales Dashboard</h1>
            <p style="font-size: 1.2em; margin: 0;">Upload your sales data to get started</p>
        </div>
    """, unsafe_allow_html=True)

    # Main upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your Excel or CSV file here",
            type=['xlsx', 'csv'],
            help="Upload your sales data file (Excel or CSV format)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    # Handle Excel files
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheet_name = st.selectbox("Select Sheet", excel_file.sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
                    # Handle CSV files
                    df = pd.read_csv(uploaded_file)
                
                st.session_state.df = df
                st.success(f"✅ Successfully loaded {len(df):,} rows of data!")
                
                # Preview the data
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📋 Required Columns</h4>
            <ul>
                <li>Amount</li>
                <li>Sales Stage</li>
                <li>Expected Close Date</li>
                <li>Practice/Region</li>
            </ul>
            <h4>📁 Supported Formats</h4>
            <ul>
                <li>Excel (.xlsx)</li>
                <li>CSV (.csv)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_overview():
    if st.session_state.df is None:
        st.warning("Please upload your data first!")
        return
    
    # Create a clean header with subtle gradient
    st.markdown("""
        <div style='background: linear-gradient(90deg, #0052CC 0%, #00C7B1 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>Sales Performance Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.df.copy()
    
    # Initialize and prepare data
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0
    
    if 'Expected Close Date' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'])
        current_date = pd.Timestamp.now()
        df['MTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month == current_date.month)
        df['YTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month <= current_date.month)
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # Calculate core metrics
        won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount_ytd = won_deals[won_deals['YTD']]['Amount'].sum() / 100000
        won_amount_mtd = won_deals[won_deals['MTD']]['Amount'].sum() / 100000
        pipeline_df = df[~df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        total_pipeline = pipeline_df['Amount'].sum() / 100000
        target = float(st.session_state.sales_target)
        
        # 1. Executive Summary Cards
        st.markdown("### Key Performance Metrics")
        
        # Create a container with custom styling for KPI cards
        st.markdown("""
            <style>
                .metric-card {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin: 10px 0;
                }
                .metric-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0052CC;
                }
                .metric-delta {
                    font-size: 14px;
                    color: #666;
                }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Target vs Achievement
            achievement_pct = (won_amount_ytd / target * 100) if target > 0 else 0
            st.metric(
                "🎯 Target Achievement",
                f"₹{won_amount_ytd:,.1f}L",
                f"{achievement_pct:.1f}% of ₹{target:,.1f}L target",
                help="YTD achievement against annual target"
            )
        
        with col2:
            # Pipeline Coverage
            coverage = (total_pipeline / (target - won_amount_ytd) * 100) if (target - won_amount_ytd) > 0 else 0
            st.metric(
                "📈 Pipeline Coverage",
                f"₹{total_pipeline:,.1f}L",
                f"{coverage:.1f}% of remaining target",
                help="Active pipeline coverage against remaining target"
            )
        
        with col3:
            # Monthly Performance
            mtd_growth = ((won_amount_mtd - won_amount_ytd/12) / (won_amount_ytd/12) * 100) if won_amount_ytd > 0 else 0
            st.metric(
                "📅 Monthly Performance",
                f"₹{won_amount_mtd:,.1f}L",
                f"{mtd_growth:+.1f}% vs monthly average",
                help="MTD performance compared to monthly average"
            )
        
        # 2. Performance Trends
        st.markdown("""
            <div style='height: 30px'></div>
            <h3>Performance Trends</h3>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📊 Achievement Trend", "🎯 Pipeline Analysis"])
        
        with tab1:
            # Monthly Achievement Chart
            monthly_performance = df.groupby(df['Expected Close Date'].dt.strftime('%b %Y')).agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000
            }).reset_index()
            monthly_performance.columns = ['Month', 'Achievement']
            
            fig_achievement = go.Figure()
            fig_achievement.add_trace(go.Bar(
                x=monthly_performance['Month'],
                y=monthly_performance['Achievement'],
                marker_color='#0052CC',
                text=monthly_performance['Achievement'].apply(lambda x: f'₹{x:,.1f}L'),
                textposition='outside'
            ))
            
            fig_achievement.add_shape(
                type="line",
                x0=monthly_performance['Month'].iloc[0],
                x1=monthly_performance['Month'].iloc[-1],
                y0=target/12,
                y1=target/12,
                line=dict(color="#FF6B6B", width=2, dash="dash"),
                name="Monthly Target"
            )
            
            fig_achievement.update_layout(
                height=400,
                margin=dict(t=30),
                xaxis_title="",
                yaxis_title="Amount (₹L)",
                showlegend=False,
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig_achievement, use_container_width=True)
        
        with tab2:
            # Pipeline Distribution
            if 'Type' in df.columns:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Funnel Chart
                    funnel_data = pipeline_df.groupby('Sales Stage').agg({
                        'Amount': 'sum',
                        'Sales Stage': 'count'
                    }).reset_index()
                    funnel_data['Amount'] = funnel_data['Amount'] / 100000
                    
                    fig_funnel = go.Figure(go.Funnel(
                        y=funnel_data['Sales Stage'],
                        x=funnel_data['Amount'],
                        textposition="inside",
                        textinfo="value+percent initial",
                        opacity=0.8,
                        marker={
                            "color": ["#0052CC", "#00C7B1", "#47B881", "#7986CB"],
                            "line": {"width": [2, 2, 2, 2]}
                        }
                    ))
                    
                    fig_funnel.update_layout(
                        height=400,
                        margin=dict(t=30),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_funnel, use_container_width=True)
                
                with col2:
                    # Summary Stats
                    st.markdown("#### Pipeline Summary")
                    for stage, data in funnel_data.iterrows():
                        st.markdown(f"""
                            <div class="metric-card">
                                <div style="color: #666;">{data['Sales Stage']}</div>
                                <div class="metric-value">₹{data['Amount']:,.1f}L</div>
                                <div class="metric-delta">{data['Sales Stage_y']} deals</div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # 3. Business Mix Analysis
        st.markdown("""
            <div style='height: 30px'></div>
            <h3>Business Mix Analysis</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hunting vs Farming
            if 'Type' in df.columns:
                hunt_farm = df.groupby('Type')['Amount'].sum().div(100000)
                fig_hunt_farm = go.Figure(go.Pie(
                    values=hunt_farm.values,
                    labels=hunt_farm.index,
                    hole=0.7,
                    marker_colors=['#0052CC', '#00C7B1'],
                    textinfo='label+percent'
                ))
                
                fig_hunt_farm.update_layout(
                    title="Revenue Mix",
                    height=300,
                    margin=dict(t=30, b=0),
                    showlegend=False
                )
                
                st.plotly_chart(fig_hunt_farm, use_container_width=True)
        
        with col2:
            # Regional Split
            if 'Region' in df.columns:
                region_data = df.groupby('Region')['Amount'].sum().div(100000)
                fig_region = go.Figure(go.Bar(
                    x=region_data.index,
                    y=region_data.values,
                    marker_color='#0052CC',
                    text=region_data.values.round(1),
                    textposition='outside'
                ))
                
                fig_region.update_layout(
                    title="Regional Performance",
                    height=300,
                    margin=dict(t=30, b=0),
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title="Amount (₹L)"
                )
                
                st.plotly_chart(fig_region, use_container_width=True)
        
        # 4. Quick Insights
        st.markdown("""
            <div style='height: 30px'></div>
            <h3>Quick Insights</h3>
        """, unsafe_allow_html=True)
        
        # Recent Activities
        recent_deals = won_deals.sort_values('Expected Close Date', ascending=False).head(3)
        for _, deal in recent_deals.iterrows():
            st.markdown(f"""
                <div style='background: white; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                    <div style='color: #0052CC; font-weight: bold;'>₹{deal['Amount']/100000:,.1f}L</div>
                    <div style='color: #666; font-size: 14px;'>{deal['Sales Stage']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Required columns (Sales Stage, Amount) not found in the dataset")

def show_detailed():
    if st.session_state.df is None:
        st.warning("Please upload your data first!")
        return
    
    st.title("🔍 Detailed View")
    
    df = st.session_state.df
    
    # Search and filters
    search = st.text_input("🔍 Search", placeholder="Search in any column...")
    
    # Filter the dataframe based on search
    if search:
        mask = np.column_stack([df[col].astype(str).str.contains(search, case=False, na=False) 
                              for col in df.columns])
        df = df[mask.any(axis=1)]
    
    # Display the filtered dataframe
    st.dataframe(df, use_container_width=True)

def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Detailed View"],
            key="navigation"
        )
        
        st.session_state.current_view = selected.lower().replace(" ", "_")
    
    # Display the selected view
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "detailed_view":
        show_detailed()

if __name__ == "__main__":
    main() 
