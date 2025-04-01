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

    # Filters section in an expander
    with st.expander("📊 Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        # Time filter
        with col1:
            if 'Expected Close Date' in df.columns:
                df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'])
                min_date = df['Expected Close Date'].min()
                max_date = df['Expected Close Date'].max()
                
                date_filter = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_filter"
                )
                if len(date_filter) == 2:
                    start_date, end_date = date_filter
                    df = df[
                        (df['Expected Close Date'].dt.date >= start_date) &
                        (df['Expected Close Date'].dt.date <= end_date)
                    ]
        
        # Practice filter
        with col2:
            if 'Practice' in df.columns:
                practices = ['All'] + sorted(df['Practice'].unique().tolist())
                selected_practice = st.selectbox("Practice", practices)
                if selected_practice != 'All':
                    df = df[df['Practice'] == selected_practice]
        
        # Sales Stage filter
        with col3:
            if 'Sales Stage' in df.columns:
                stages = ['All'] + sorted(df['Sales Stage'].unique().tolist())
                selected_stage = st.selectbox("Sales Stage", stages)
                if selected_stage != 'All':
                    df = df[df['Sales Stage'] == selected_stage]

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

        # Add a visual representation of the pipeline
        st.markdown("#### Pipeline Breakdown")
        
        # Create waterfall chart with values in Lakhs
        fig = go.Figure(go.Waterfall(
            name="Pipeline", 
            orientation="v",
            measure=["total", "relative", "relative", "total"],
            x=["Target", "Closed Won", "Active Pipeline", "Gap"],
            y=[target, won_amount, active_pipeline, -(target)],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#EF5350"}},
            increasing={"marker": {"color": "#66BB6A"}},
            totals={"marker": {"color": "#4A90E2"}},
            text=[f"₹{target:,.1f}L", f"₹{won_amount:,.1f}L", f"₹{active_pipeline:,.1f}L", f"₹{(won_amount + active_pipeline - target):,.1f}L"],
            textposition="outside"
        ))
        
        fig.update_layout(
            title="Pipeline Coverage Analysis (in Lakhs)",
            showlegend=False,
            height=400,
            waterfallgap=0.2,
            xaxis={"title": ""},
            yaxis={"title": "Amount (₹L)"},
        )
        
        st.plotly_chart(fig, use_container_width=True)
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
            # Bar chart for amount
            hunt_farm_amount = df.groupby('Business Type')['Amount'].sum().reset_index()
            fig_amount = px.bar(
                hunt_farm_amount,
                x='Business Type',
                y='Amount',
                title="Revenue Distribution",
                color='Business Type',
                color_discrete_sequence=['#4A90E2', '#45B7AF'],
                text=hunt_farm_amount['Amount'].apply(lambda x: f'₹{x:,.2f}L')
            )
            fig_amount.update_traces(textposition='outside')
            fig_amount.update_layout(showlegend=True)
            st.plotly_chart(fig_amount, use_container_width=True)
            
        # Add summary metrics
        col1, col2 = st.columns(2)
        with col1:
            farming_amount = df[df['Type'] == 'Existing Business (Farming)']['Amount'].sum()
            st.metric("Farming Revenue", f"₹{farming_amount:,.2f}L")
        with col2:
            hunting_amount = df[df['Type'] == 'New Business (Hunting)']['Amount'].sum()
            st.metric("Hunting Revenue", f"₹{hunting_amount:,.2f}L")
    else:
        st.info("Business Type classification not found in the dataset")

    # Sales Stages Analysis
    st.markdown("### 🎯 Sales Stages Analysis")
    if 'Sales Stage' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Funnel chart for sales stages
            stage_metrics = df.groupby('Sales Stage').agg({
                'Amount': 'sum',
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
                connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}}
            ))
            
            fig_funnel.update_layout(
                title="Pipeline Funnel",
                showlegend=False,
                height=400
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
        
        # Add stage transition timeline
        st.markdown("#### Pipeline Movement")
        if 'Expected Close Date' in df.columns:
            # Create timeline of stage changes
            timeline_data = df.groupby([
                pd.Grouper(key='Expected Close Date', freq='M'),
                'Sales Stage'
            ])['Amount'].sum().reset_index()
            
            fig_timeline = px.area(
                timeline_data,
                x='Expected Close Date',
                y='Amount',
                color='Sales Stage',
                title="Pipeline Stage Movement Over Time",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_timeline.update_layout(
                xaxis_title="Date",
                yaxis_title="Amount (₹L)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Stage conversion metrics
            st.markdown("#### Stage Conversion Rates")
            stage_order = df['Sales Stage'].unique().tolist()
            conversion_metrics = []
            
            for i in range(len(stage_order)-1):
                current_stage = stage_order[i]
                next_stage = stage_order[i+1]
                current_count = df[df['Sales Stage'] == current_stage].shape[0]
                next_count = df[df['Sales Stage'] == next_stage].shape[0]
                
                if current_count > 0:
                    conversion_rate = (next_count / current_count) * 100
                    conversion_metrics.append({
                        'From Stage': current_stage,
                        'To Stage': next_stage,
                        'Conversion Rate': f"{conversion_rate:.1f}%"
                    })
            
            if conversion_metrics:
                st.dataframe(pd.DataFrame(conversion_metrics), use_container_width=True)
    else:
        st.info("Sales Stage information not found in the dataset")

    # Geographical Split
    st.markdown("### 🌍 Geographical Distribution")
    if 'Region' in df.columns or 'Geography' in df.columns:
        geo_col = 'Region' if 'Region' in df.columns else 'Geography'
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Region-wise revenue
            geo_data = df.groupby(geo_col)['Amount'].sum().reset_index()
            fig_geo = px.bar(
                geo_data,
                x=geo_col,
                y='Amount',
                title=f"Revenue by {geo_col}",
                color=geo_col
            )
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
    if 'Deal Type' in df.columns:  # Assuming 'Deal Type' contains Committed/Upside classification
        col1, col2 = st.columns(2)
        
        with col1:
            # Amount distribution
            deal_type_amount = df.groupby('Deal Type')['Amount'].sum().reset_index()
            fig_deal_type = px.bar(
                deal_type_amount,
                x='Deal Type',
                y='Amount',
                title="Revenue: Committed vs Upside",
                color='Deal Type'
            )
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
