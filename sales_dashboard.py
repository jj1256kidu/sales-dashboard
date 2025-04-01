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
    
    st.title("📈 Sales Overview")
    
    df = st.session_state.df.copy()  # Create a copy to avoid modifying original data
    
    # Initialize target if not in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0

    # KPI Row
    st.markdown("### 📌 Key Metrics")
    
    # First get all the metrics
    if 'Sales Stage' in df.columns:
        # Total Won (Closed) - Convert to Lakhs
        won_amount = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum() / 100000
        
        # Active Pipeline (excluding Won) - Convert to Lakhs
        pipeline_df = df[~df['Sales Stage'].str.contains('Won', case=False, na=False)]
        active_pipeline = (pipeline_df['Amount'].sum() if 'Amount' in pipeline_df.columns else 0) / 100000
        
        # Total (Pipeline + Won) - Already in Lakhs
        total_amount = active_pipeline + won_amount
        
        # Target vs Achievement
        target = float(st.session_state.sales_target)  # Already in Lakhs from input
        pending_target = max(0, target - won_amount)  # Already in Lakhs
        
        # Create two rows of metrics
        st.markdown("#### Target vs Achievement")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Target", 
                f"₹{target:,.2f}L",
                help="Annual target set for the team (in Lakhs)"
            )
        
        with col2:
            achievement_pct = (won_amount / target * 100) if target > 0 else 0
            st.metric(
                "Closed Won", 
                f"₹{won_amount:,.2f}L",
                f"{achievement_pct:.1f}% of target",
                help="Total amount of closed/won deals (in Lakhs)"
            )
        
        with col3:
            st.metric(
                "Pending Target", 
                f"₹{pending_target:,.2f}L",
                help="Amount still needed to reach target (in Lakhs)"
            )
        
        # Pipeline metrics
        st.markdown("#### Pipeline Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pipeline_coverage = (active_pipeline / pending_target * 100) if pending_target > 0 else 0
            st.metric(
                "Active Pipeline", 
                f"₹{active_pipeline:,.2f}L",
                f"{pipeline_coverage:.1f}% coverage",
                help="Current pipeline excluding closed won deals (in Lakhs)"
            )
        
        with col2:
            win_rate = (df['Sales Stage'].str.contains('Won', case=False, na=False).sum() / len(df)) * 100
            st.metric(
                "Win Rate", 
                f"{win_rate:.1f}%",
                help="Percentage of deals won out of total deals"
            )
        
        with col3:
            # Target input
            new_target = st.number_input(
                "Update Target (in Lakhs)",
                value=float(st.session_state.sales_target),
                step=1.0,
                key="target_input",
                help="Enter target amount in Lakhs (1L = ₹100,000)"
            )
            if new_target != st.session_state.sales_target:
                st.session_state.sales_target = new_target
                st.rerun()
    else:
        st.error("Sales Stage column not found in the dataset. Please check your data format.")
        
    # Hunting vs Farming Split
    st.markdown("### 🎯 Hunting vs Farming Split")
    if 'Type' in df.columns:
        # Create mapping for cleaner labels
        df['Business Type'] = df['Type'].map({
            'Existing Business (Farming)': 'Farming',
            'New Business (Hunting)': 'Hunting'
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for deal count
            hunt_farm_count = df['Business Type'].value_counts()
            fig_count = px.pie(
                values=hunt_farm_count.values,
                names=hunt_farm_count.index,
                title="Deal Distribution (Count)",
                color_discrete_sequence=['#4A90E2', '#45B7AF'],
                hole=0.4
            )
            fig_count.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig_count, use_container_width=True)
        
        with col2:
            # Bar chart for amount (in lakhs)
            hunt_farm_amount = df.groupby('Business Type')['Amount'].sum().div(100000).reset_index()
            fig_amount = px.bar(
                hunt_farm_amount,
                x='Business Type',
                y='Amount',
                title="Revenue Distribution (in Lakhs)",
                color='Business Type',
                color_discrete_sequence=['#4A90E2', '#45B7AF'],
                text=hunt_farm_amount['Amount'].apply(lambda x: f'₹{x:,.2f}L')
            )
            fig_amount.update_traces(textposition='outside')
            fig_amount.update_layout(
                showlegend=True,
                yaxis_title="Amount (₹L)"
            )
            st.plotly_chart(fig_amount, use_container_width=True)
            
        # Add summary metrics
        col1, col2 = st.columns(2)
        with col1:
            farming_amount = df[df['Type'] == 'Existing Business (Farming)']['Amount'].sum() / 100000
            st.metric("Farming Revenue", f"₹{farming_amount:,.2f}L")
        with col2:
            hunting_amount = df[df['Type'] == 'New Business (Hunting)']['Amount'].sum() / 100000
            st.metric("Hunting Revenue", f"₹{hunting_amount:,.2f}L")
    else:
        st.info("Business Type classification not found in the dataset")

    # Sales Stages Analysis
    st.markdown("### 🎯 Sales Stages Analysis")
    if 'Sales Stage' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Funnel chart for sales stages (in lakhs)
            stage_metrics = df.groupby('Sales Stage').agg({
                'Amount': lambda x: x.sum() / 100000,  # Convert to lakhs
                'Type': 'count'
            }).reset_index()
            stage_metrics = stage_metrics.sort_values('Amount', ascending=False)
            
            fig_funnel = go.Figure(go.Funnel(
                y=stage_metrics['Sales Stage'],
                x=stage_metrics['Amount'],
                textposition="inside",
                textinfo="value+percent initial",
                opacity=0.65,
                marker={
                    "color": ["#4A90E2", "#45B7AF", "#66BB6A", "#FFA726", "#EF5350"],
                    "line": {"width": [2, 2, 2, 2, 2]}
                },
                connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}},
                text=[f"₹{x:,.2f}L" for x in stage_metrics['Amount']]
            ))
            
            fig_funnel.update_layout(
                title="Pipeline Funnel (in Lakhs)",
                showlegend=False,
                height=400,
                yaxis_title="Sales Stage",
                xaxis_title="Amount (₹L)"
            )
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Detailed metrics table
            stage_metrics['Deal Count'] = stage_metrics['Type']
            stage_metrics['Amount'] = stage_metrics['Amount'].apply(lambda x: f"₹{x:,.2f}L")
            stage_metrics['Percentage'] = (stage_metrics['Deal Count'] / stage_metrics['Deal Count'].sum() * 100).apply(lambda x: f"{x:.1f}%")
            
            st.markdown("#### Stage-wise Breakdown")
            st.dataframe(
                stage_metrics[['Sales Stage', 'Deal Count', 'Amount', 'Percentage']],
                use_container_width=True
            )
            
            # Win Rate Calculation
            if any(df['Sales Stage'].str.contains('Won', case=False, na=False)):
                total_closed = df[df['Sales Stage'].str.contains('Closed|Won|Lost', case=False, na=False)].shape[0]
                total_won = df[df['Sales Stage'].str.contains('Won', case=False, na=False)].shape[0]
                if total_closed > 0:
                    win_rate = (total_won / total_closed) * 100
                    st.metric("Win Rate (Closed Deals)", f"{win_rate:.1f}%")
    else:
        st.info("Sales Stage information not found in the dataset")

    # Geographical Split
    st.markdown("### 🌍 Geographical Distribution")
    if 'Region' in df.columns or 'Geography' in df.columns:
        geo_col = 'Region' if 'Region' in df.columns else 'Geography'
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Region-wise revenue (in lakhs)
            geo_data = df.groupby(geo_col)['Amount'].sum().div(100000).reset_index()
            fig_geo = px.bar(
                geo_data,
                x=geo_col,
                y='Amount',
                title=f"Revenue by {geo_col} (in Lakhs)",
                color=geo_col,
                text=geo_data['Amount'].apply(lambda x: f'₹{x:,.2f}L')
            )
            fig_geo.update_layout(yaxis_title="Amount (₹L)")
            fig_geo.update_traces(textposition='outside')
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col2:
            # Region-wise deal count
            geo_count = df.groupby(geo_col).size().reset_index(name='Count')
            fig_geo_count = px.pie(
                geo_count,
                values='Count',
                names=geo_col,
                title=f"Deal Distribution by {geo_col}"
            )
            st.plotly_chart(fig_geo_count, use_container_width=True)
    else:
        st.info("Geographical information not found in the dataset")

    # Committed vs Upside
    st.markdown("### 📊 Committed vs Upside")
    if 'Deal Type' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Amount distribution (in lakhs)
            deal_type_amount = df.groupby('Deal Type')['Amount'].sum().div(100000).reset_index()
            fig_deal_type = px.bar(
                deal_type_amount,
                x='Deal Type',
                y='Amount',
                title="Revenue: Committed vs Upside (in Lakhs)",
                color='Deal Type',
                text=deal_type_amount['Amount'].apply(lambda x: f'₹{x:,.2f}L')
            )
            fig_deal_type.update_layout(yaxis_title="Amount (₹L)")
            fig_deal_type.update_traces(textposition='outside')
            st.plotly_chart(fig_deal_type, use_container_width=True)
        
        with col2:
            # Deal count distribution
            deal_type_count = df['Deal Type'].value_counts()
            fig_deal_count = px.pie(
                values=deal_type_count.values,
                names=deal_type_count.index,
                title="Distribution: Committed vs Upside"
            )
            st.plotly_chart(fig_deal_count, use_container_width=True)
    else:
        st.info("Committed/Upside classification not found in the dataset")

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
