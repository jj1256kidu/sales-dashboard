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
        
        # Calculate MTD and YTD flags
        df['MTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month == current_date.month)
        df['YTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month <= current_date.month)
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # Add filters at the top
        st.markdown("### 🔍 Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Expected Close Date' in df.columns:
                selected_month = st.selectbox(
                    "Select Month",
                    options=sorted(df['Expected Close Date'].dt.strftime('%b %Y').unique()),
                    index=len(df['Expected Close Date'].dt.strftime('%b %Y').unique()) - 1
                )
        
        with col2:
            if 'Practice' in df.columns:
                selected_practice = st.selectbox(
                    "Select Practice",
                    options=['All'] + sorted(df['Practice'].unique().tolist())
                )
        
        with col3:
            if 'Sales Stage' in df.columns:
                selected_stage = st.selectbox(
                    "Select Stage",
                    options=['All'] + sorted(df['Sales Stage'].unique().tolist())
                )
        
        # Apply filters
        filtered_df = df.copy()
        if 'Expected Close Date' in df.columns:
            filtered_df = filtered_df[filtered_df['Expected Close Date'].dt.strftime('%b %Y') == selected_month]
        if selected_practice != 'All':
            filtered_df = filtered_df[filtered_df['Practice'] == selected_practice]
        if selected_stage != 'All':
            filtered_df = filtered_df[filtered_df['Sales Stage'] == selected_stage]
        
        # I. Top KPI Cards
        st.markdown("### 🔝 Key Performance Indicators")
        
        # Calculate core metrics
        won_deals = filtered_df[filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount = won_deals['Amount'].sum() / 100000
        
        pipeline_df = filtered_df[~filtered_df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        total_pipeline = pipeline_df['Amount'].sum() / 100000
        
        # Calculate Committed vs Upside if Status column exists
        committed_deals = 0
        upside_deals = 0
        if 'Status' in filtered_df.columns:
            committed_deals = filtered_df[filtered_df['Status'] == 'Committed for the Month']['Amount'].sum() / 100000
            upside_deals = filtered_df[filtered_df['Status'] == 'Upside for the Month']['Amount'].sum() / 100000
        
        target = float(st.session_state.sales_target)
        achievement_pct = (won_amount / target * 100) if target > 0 else 0
        
        # Display KPIs in three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Target with edit option
            new_target = st.number_input(
                "🎯 Sales Target (Lakhs)",
                value=float(st.session_state.sales_target),
                step=1.0,
                format="%.2f",
                help="Enter annual target in Lakhs (1L = ₹100,000)"
            )
            if new_target != st.session_state.sales_target:
                st.session_state.sales_target = new_target
                st.rerun()
            
            st.metric(
                "✅ Closed Won",
                f"₹{won_amount:,.2f}L",
                f"{achievement_pct:.1f}% of Target"
            )
        
        with col2:
            st.metric(
                "📈 Total Pipeline",
                f"₹{total_pipeline:,.2f}L",
                f"{(total_pipeline/target*100 if target > 0 else 0):.1f}% of Target"
            )
            
            st.metric(
                "📉 Target Gap",
                f"₹{(target - won_amount):,.2f}L",
                f"{(100 - achievement_pct):.1f}% remaining"
            )
        
        with col3:
            if 'Status' in filtered_df.columns:
                st.metric(
                    "💼 Committed Deals",
                    f"₹{committed_deals:,.2f}L",
                    f"{(committed_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}% of Pipeline"
                )
                
                st.metric(
                    "📊 Upside Deals",
                    f"₹{upside_deals:,.2f}L",
                    f"{(upside_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}% of Pipeline"
                )
            else:
                st.metric(
                    "🎯 Win Rate",
                    f"{(len(won_deals) / len(filtered_df) * 100):.1f}%",
                    f"{len(won_deals)}/{len(filtered_df)} deals"
                )
        
        # II. Business Mix Analysis
        st.markdown("### 📊 Business Mix Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hunting vs Farming Split
            if 'Type' in filtered_df.columns:
                type_data = filtered_df.groupby('Type').agg({
                    'Amount': 'sum',
                    'id': 'count'
                }).reset_index()
                
                type_data['Amount'] = type_data['Amount'] / 100000
                total_amount = type_data['Amount'].sum()
                total_count = type_data['id'].sum()
                
                fig_type = go.Figure(go.Pie(
                    values=type_data['Amount'],
                    labels=type_data['Type'],
                    hole=0.6,
                    textinfo='label+percent+value',
                    text=type_data.apply(lambda x: f"{x['Type']}<br>₹{x['Amount']:,.1f}L<br>{(x['Amount']/total_amount*100):.1f}%<br>{x['id']} deals", axis=1),
                    hovertemplate="<b>%{label}</b><br>" +
                                "Amount: ₹%{value:,.1f}L<br>" +
                                "Percentage: %{percent}<br>" +
                                "Deal Count: %{text}<br>" +
                                "<extra></extra>"
                ))
                
                fig_type.update_layout(
                    title="Hunting vs Farming Split",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_type, use_container_width=True)
        
        with col2:
            # Geographical Split
            if 'Region' in filtered_df.columns:
                region_data = filtered_df.groupby('Region').agg({
                    'Amount': 'sum',
                    'id': 'count'
                }).reset_index()
                
                region_data['Amount'] = region_data['Amount'] / 100000
                total_amount = region_data['Amount'].sum()
                total_count = region_data['id'].sum()
                
                fig_geo = go.Figure(go.Pie(
                    values=region_data['Amount'],
                    labels=region_data['Region'],
                    hole=0.6,
                    textinfo='label+percent+value',
                    text=region_data.apply(lambda x: f"{x['Region']}<br>₹{x['Amount']:,.1f}L<br>{(x['Amount']/total_amount*100):.1f}%<br>{x['id']} deals", axis=1),
                    hovertemplate="<b>%{label}</b><br>" +
                                "Amount: ₹%{value:,.1f}L<br>" +
                                "Percentage: %{percent}<br>" +
                                "Deal Count: %{text}<br>" +
                                "<extra></extra>"
                ))
                
                fig_geo.update_layout(
                    title="Geographical Distribution",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_geo, use_container_width=True)
        
        # III. Target vs Achievement
        st.markdown("### 🎯 Target vs Achievement")
        
        if 'Expected Close Date' in filtered_df.columns:
            # Monthly performance trend
            monthly_performance = filtered_df.groupby(filtered_df['Expected Close Date'].dt.strftime('%b %Y')).agg({
                'Amount': lambda x: x[filtered_df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000
            }).reset_index()
            monthly_performance.columns = ['Month', 'Achievement']
            
            # Add target line
            monthly_target = target / 12
            
            fig_achievement = go.Figure()
            
            # Add target line
            fig_achievement.add_trace(go.Scatter(
                x=monthly_performance['Month'],
                y=[monthly_target] * len(monthly_performance),
                name='Monthly Target',
                line=dict(color='red', dash='dash')
            ))
            
            # Add achievement bars
            fig_achievement.add_trace(go.Bar(
                x=monthly_performance['Month'],
                y=monthly_performance['Achievement'],
                name='Achievement',
                text=monthly_performance['Achievement'].apply(lambda x: f'₹{x:,.1f}L<br>{(x/monthly_target*100 if monthly_target > 0 else 0):.1f}%'),
                textposition='outside'
            ))
            
            fig_achievement.update_layout(
                title="Monthly Target vs Achievement",
                height=400,
                barmode='group'
            )
            
            st.plotly_chart(fig_achievement, use_container_width=True)
        
        # IV. Pipeline Analysis
        st.markdown("### 🕳️ Pipeline Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sales Funnel
            stage_data = filtered_df.groupby('Sales Stage').agg({
                'Amount': 'sum',
                'id': 'count'
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
                title="Pipeline Funnel",
                height=400
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Deal Alerts
            st.markdown("#### 🚨 Deal Alerts")
            
            # High-value deals
            high_value_deals = pipeline_df.nlargest(3, 'Amount')
            for _, deal in high_value_deals.iterrows():
                st.markdown(f"""
                    💰 **High Value Deal**: ₹{deal['Amount']/100000:,.1f}L  
                    Stage: {deal['Sales Stage']}
                """)
            
            # Recent Wins
            st.markdown("#### 🏆 Recent Wins")
            recent_wins = won_deals.nlargest(3, 'Amount')
            for _, deal in recent_wins.iterrows():
                st.markdown(f"✨ ₹{deal['Amount']/100000:,.1f}L")
    
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
