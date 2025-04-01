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
    
    st.title("Sales Overview")
    
    df = st.session_state.df.copy()
    
    # Initialize target if not in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0
    
    # Date filtering
    if 'Expected Close Date' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'])
        current_date = pd.Timestamp.now()
        df['MTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month == current_date.month)
        df['YTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month <= current_date.month)
    
    # Basic KPI Section
    st.markdown("### Key Metrics")
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # Calculate basic metrics
        won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount = won_deals['Amount'].sum() / 100000  # Convert to Lakhs
        won_amount_mtd = won_deals[won_deals['MTD']]['Amount'].sum() / 100000
        won_amount_ytd = won_deals[won_deals['YTD']]['Amount'].sum() / 100000
        
        pipeline_df = df[~df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        pipeline_amount = pipeline_df['Amount'].sum() / 100000
        
        target = float(st.session_state.sales_target)
        
        # Display KPIs in three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Target input and achievement
            new_target = st.number_input(
                "Sales Target (Lakhs)",
                value=float(st.session_state.sales_target),
                step=1.0,
                format="%.2f",
                help="Enter annual target in Lakhs (1L = ₹100,000)"
            )
            if new_target != st.session_state.sales_target:
                st.session_state.sales_target = new_target
                st.rerun()
            
            achievement_pct = (won_amount_ytd / target * 100) if target > 0 else 0
            st.metric(
                "Closed Won (YTD)",
                f"₹{won_amount_ytd:,.2f}L",
                f"{achievement_pct:.1f}% of target"
            )
        
        with col2:
            pipeline_coverage = (pipeline_amount / (target - won_amount_ytd) * 100) if (target - won_amount_ytd) > 0 else 0
            st.metric(
                "Active Pipeline",
                f"₹{pipeline_amount:,.2f}L",
                f"{pipeline_coverage:.1f}% coverage",
                help="Total pipeline excluding closed deals"
            )
            
            st.metric(
                "MTD Achievement",
                f"₹{won_amount_mtd:,.2f}L",
                help="Month to Date Achievement"
            )
        
        with col3:
            # Win Rate
            closed_deals = df[df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
            win_rate = (won_deals.shape[0] / closed_deals.shape[0] * 100) if closed_deals.shape[0] > 0 else 0
            st.metric(
                "Win Rate",
                f"{win_rate:.1f}%",
                help="Percentage of won deals out of total closed deals"
            )
            
            avg_deal_size = won_deals['Amount'].mean() / 100000 if not won_deals.empty else 0
            st.metric(
                "Avg Deal Size",
                f"₹{avg_deal_size:,.2f}L",
                help="Average size of won deals"
            )
        
        # Sales Stage Analysis
        st.markdown("### Sales Stages")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Funnel chart
            stage_data = df.groupby('Sales Stage').agg({
                'Amount': 'sum',
                'Sales Stage': 'count'
            }).reset_index()
            stage_data['Amount'] = stage_data['Amount'] / 100000
            
            fig_funnel = go.Figure(go.Funnel(
                y=stage_data['Sales Stage'],
                x=stage_data['Amount'],
                textposition="inside",
                textinfo="value+percent initial",
                marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
            ))
            
            fig_funnel.update_layout(
                height=400,
                title="Pipeline by Stage",
                showlegend=False
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Stage-wise metrics table
            st.markdown("#### Stage Details")
            stage_metrics = stage_data.copy()
            stage_metrics['Deal Count'] = stage_metrics['Sales Stage_y']
            stage_metrics['Amount'] = stage_metrics['Amount'].apply(lambda x: f"₹{x:,.2f}L")
            st.dataframe(
                stage_metrics[['Sales Stage', 'Deal Count', 'Amount']],
                use_container_width=True
            )
        
        # Hunting vs Farming Split (if available)
        if 'Type' in df.columns:
            st.markdown("### Business Type Split")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Donut chart
                type_data = df.groupby('Type')['Amount'].sum().div(100000)
                fig_type = go.Figure(go.Pie(
                    values=type_data.values,
                    labels=type_data.index,
                    hole=0.6,
                    marker_colors=['#1f77b4', '#ff7f0e'],
                    textinfo='label+percent+value'
                ))
                
                fig_type.update_layout(
                    height=400,
                    title="Revenue by Business Type",
                    showlegend=True
                )
                
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                # Summary metrics
                st.markdown("#### Type Details")
                for type_name, amount in type_data.items():
                    st.metric(
                        type_name,
                        f"₹{amount:,.2f}L",
                        f"{(amount/type_data.sum()*100):.1f}% of total"
                    )
        
        # Monthly Trend
        if 'Expected Close Date' in df.columns:
            st.markdown("### Monthly Performance")
            
            view_type = st.radio(
                "Select View",
                ["Closed Won", "Pipeline"],
                horizontal=True
            )
            
            monthly_data = df.groupby(df['Expected Close Date'].dt.strftime('%b %Y')).agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won' if view_type == 'Closed Won' else 'Won|Lost', case=False, na=False)].sum() / 100000
            }).reset_index()
            
            fig_trend = go.Figure()
            
            # Add target line
            if view_type == 'Closed Won':
                fig_trend.add_shape(
                    type="line",
                    x0=monthly_data['Expected Close Date'].iloc[0],
                    x1=monthly_data['Expected Close Date'].iloc[-1],
                    y0=target/12,
                    y1=target/12,
                    line=dict(color="red", width=2, dash="dash"),
                    name="Monthly Target"
                )
            
            fig_trend.add_trace(go.Bar(
                x=monthly_data['Expected Close Date'],
                y=monthly_data['Amount'],
                text=monthly_data['Amount'].apply(lambda x: f'₹{x:,.2f}L'),
                textposition='outside',
                marker_color='#1f77b4'
            ))
            
            fig_trend.update_layout(
                height=400,
                title=f"Monthly {view_type}",
                xaxis_title="Month",
                yaxis_title="Amount (₹L)",
                showlegend=False
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        # Regional Split (if available)
        if 'Region' in df.columns:
            st.markdown("### Regional Performance")
            
            # Add filters
            col1, col2 = st.columns(2)
            with col1:
                if 'Practice' in df.columns:
                    practices = ['All'] + sorted(df['Practice'].unique().tolist())
                    selected_practice = st.selectbox("Filter by Practice", practices)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_practice != 'All':
                filtered_df = filtered_df[filtered_df['Practice'] == selected_practice]
            
            # Calculate metrics
            region_data = filtered_df.groupby('Region').agg({
                'Amount': lambda x: x.sum() / 100000,
                'Region': 'count'
            }).reset_index()
            
            fig_region = go.Figure(go.Bar(
                x=region_data['Region'],
                y=region_data['Amount'],
                text=region_data['Amount'].round(1).apply(lambda x: f'₹{x:,.2f}L'),
                textposition='outside',
                marker_color='#1f77b4'
            ))
            
            fig_region.update_layout(
                height=400,
                title="Revenue by Region",
                xaxis_title="Region",
                yaxis_title="Amount (₹L)",
                showlegend=False
            )
            
            st.plotly_chart(fig_region, use_container_width=True)
    
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
