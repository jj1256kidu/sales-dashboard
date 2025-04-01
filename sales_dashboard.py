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
    
    # Convert dates and create MTD/YTD flags
    if 'Expected Close Date' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'])
        current_date = pd.Timestamp.now()
        df['MTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month == current_date.month)
        df['YTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month <= current_date.month)
    
    # 1. Top KPI Cards
    st.markdown("### 🔝 Key Performance Indicators")
    
    # Calculate KPIs
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # Won deals
        won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount = won_deals['Amount'].sum() / 100000  # Convert to Lakhs
        won_amount_mtd = won_deals[won_deals['MTD']]['Amount'].sum() / 100000
        won_amount_ytd = won_deals[won_deals['YTD']]['Amount'].sum() / 100000
        
        # Pipeline and Deal Types
        pipeline_df = df[~df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        total_pipeline = pipeline_df['Amount'].sum() / 100000
        
        committed_deals = df[df['Status'] == 'Committed for the Month']['Amount'].sum() / 100000
        upside_deals = df[df['Status'] == 'Upside for the Month']['Amount'].sum() / 100000
        
        # Win Rate
        closed_deals = df[df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        win_rate = (won_deals.shape[0] / closed_deals.shape[0] * 100) if closed_deals.shape[0] > 0 else 0
        
        # Target and Variance
        target = float(st.session_state.sales_target)  # in Lakhs
        variance = ((won_amount_ytd - target) / target * 100) if target > 0 else 0
        
        # Display KPIs in two rows
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Target KPI with edit option
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
        
        with col2:
            st.metric(
                "✅ Closed Won",
                f"₹{won_amount_ytd:,.2f}L",
                f"MTD: ₹{won_amount_mtd:,.2f}L",
                help="YTD / MTD Closed Won Amount"
            )
        
        with col3:
            st.metric(
                "📈 Total Pipeline",
                f"₹{total_pipeline:,.2f}L",
                f"{(total_pipeline/target*100 if target > 0 else 0):.1f}% of Target",
                help="Active pipeline excluding closed deals"
            )
        
        with col4:
            st.metric(
                "📉 Target Variance",
                f"{variance:+.1f}%",
                f"₹{(target - won_amount_ytd):,.2f}L to go",
                help="Variance from annual target"
            )
        
        # Second row of KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💼 Committed Deals",
                f"₹{committed_deals:,.2f}L",
                f"{(committed_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}% of Pipeline",
                help="Total committed deals in pipeline"
            )
        
        with col2:
            st.metric(
                "📊 Upside Deals",
                f"₹{upside_deals:,.2f}L",
                f"{(upside_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}% of Pipeline",
                help="Total upside deals in pipeline"
            )
        
        with col3:
            st.metric(
                "🧮 Win Rate",
                f"{win_rate:.1f}%",
                help="Percentage of won deals out of total closed deals"
            )
        
        with col4:
            avg_deal_size = won_deals['Amount'].mean() / 100000 if not won_deals.empty else 0
            st.metric(
                "💰 Avg Deal Size",
                f"₹{avg_deal_size:,.2f}L",
                help="Average size of won deals"
            )
        
        # 2. Target vs Closed Won Performance Trend
        st.markdown("### 📊 Target vs Achievement")
        
        # Toggle for MTD/YTD view
        view_type = st.radio(
            "Select View",
            ["MTD", "YTD"],
            horizontal=True,
            key="performance_view"
        )
        
        # Calculate monthly performance
        monthly_performance = df.groupby(df['Expected Close Date'].dt.strftime('%b %Y')).agg({
            'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000
        }).reset_index()
        monthly_performance.columns = ['Month', 'Closed Won']
        
        # Add target line (divided equally for months)
        monthly_target = target / 12
        monthly_performance['Target'] = monthly_target
        
        # Calculate achievement percentage
        monthly_performance['Achievement %'] = (monthly_performance['Closed Won'] / monthly_performance['Target'] * 100).round(1)
        
        # Create performance trend chart
        fig_performance = go.Figure()
        
        # Add target line
        fig_performance.add_trace(go.Scatter(
            x=monthly_performance['Month'],
            y=monthly_performance['Target'],
            name='Target',
            line=dict(color='#666666', dash='dash'),
            hovertemplate="Target: ₹%{y:.2f}L<extra></extra>"
        ))
        
        # Add achievement bars
        fig_performance.add_trace(go.Bar(
            x=monthly_performance['Month'],
            y=monthly_performance['Closed Won'],
            name='Closed Won',
            marker_color='#4CAF50',
            text=monthly_performance['Achievement %'].apply(lambda x: f"{x}%"),
            textposition='outside',
            hovertemplate="Closed Won: ₹%{y:.2f}L<br>Achievement: %{text}<extra></extra>"
        ))
        
        fig_performance.update_layout(
            title="Monthly Target vs Achievement",
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis_title="Month",
            yaxis_title="Amount (₹L)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
        
        # 3. Committed vs Upside Monthly Trend
        st.markdown("### 🧩 Committed vs Upside Trend")
        
        # Create monthly trend chart
        monthly_split = df.pivot_table(
            index=df['Expected Close Date'].dt.strftime('%b %Y'),
            columns='Status',
            values='Amount',
            aggfunc='sum'
        ).div(100000).fillna(0)
        
        # Sort months chronologically
        monthly_split.index = pd.to_datetime(monthly_split.index, format='%b %Y')
        monthly_split = monthly_split.sort_index()
        monthly_split.index = monthly_split.index.strftime('%b %Y')
        
        # Create stacked column chart
        fig_monthly = go.Figure()
        
        # Add bars for Committed and Upside
        fig_monthly.add_trace(go.Bar(
            name='Committed',
            x=monthly_split.index,
            y=monthly_split['Committed for the Month'],
            marker_color='#0052CC',
            text=monthly_split['Committed for the Month'].apply(lambda x: f'₹{x:,.2f}L'),
            textposition='inside'
        ))
        
        fig_monthly.add_trace(go.Bar(
            name='Upside',
            x=monthly_split.index,
            y=monthly_split['Upside for the Month'],
            marker_color='#00C7B1',
            text=monthly_split['Upside for the Month'].apply(lambda x: f'₹{x:,.2f}L'),
            textposition='inside'
        ))
        
        # Highlight latest month
        latest_month = monthly_split.index[-1]
        fig_monthly.add_shape(
            type="rect",
            x0=latest_month,
            x1=latest_month,
            y0=0,
            y1=monthly_split.loc[latest_month].sum(),
            line=dict(color="#FFD700", width=3),
            opacity=0.3
        )
        
        fig_monthly.update_layout(
            title="Monthly Committed vs Upside Split",
            barmode='stack',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='white',
            xaxis_title="Month",
            yaxis_title="Amount (₹L)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # 4. Geography Split
        st.markdown("### 🌍 Geographical Distribution")
        
        # Add filters for Practice and Sales Owner
        col1, col2 = st.columns(2)
        with col1:
            if 'Practice' in df.columns:
                practices = ['All'] + sorted(df['Practice'].unique().tolist())
                selected_practice = st.selectbox("Filter by Practice", practices)
        
        with col2:
            if 'Sales Owner' in df.columns:
                owners = ['All'] + sorted(df['Sales Owner'].unique().tolist())
                selected_owner = st.selectbox("Filter by Sales Owner", owners)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_practice != 'All':
            filtered_df = filtered_df[filtered_df['Practice'] == selected_practice]
        if selected_owner != 'All':
            filtered_df = filtered_df[filtered_df['Sales Owner'] == selected_owner]
        
        # Create geography charts
        if 'Region' in filtered_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Region-wise pipeline and closed won
                geo_data = filtered_df.pivot_table(
                    index='Region',
                    columns='Sales Stage',
                    values='Amount',
                    aggfunc='sum'
                ).div(100000).fillna(0)
                
                fig_geo = go.Figure()
                
                # Add bars for pipeline and closed won
                for stage in geo_data.columns:
                    fig_geo.add_trace(go.Bar(
                        name=stage,
                        x=geo_data.index,
                        y=geo_data[stage],
                        text=geo_data[stage].apply(lambda x: f'₹{x:,.2f}L'),
                        textposition='outside'
                    ))
                
                fig_geo.update_layout(
                    title="Region-wise Pipeline and Closed Won",
                    barmode='group',
                    height=400,
                    xaxis_title="Region",
                    yaxis_title="Amount (₹L)"
                )
                
                st.plotly_chart(fig_geo, use_container_width=True)
            
            with col2:
                # Region-wise deal count
                deal_count = filtered_df.groupby('Region').size()
                fig_count = px.pie(
                    values=deal_count.values,
                    names=deal_count.index,
                    title="Deal Count by Region"
                )
                
                st.plotly_chart(fig_count, use_container_width=True)
        
        # 5. Hunting vs Farming Split
        st.markdown("### 🧭 Hunting vs Farming Split")
        
        if 'Type' in filtered_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Create donut chart
                hunt_farm = filtered_df.groupby('Type')['Amount'].sum().div(100000)
                fig_hunt_farm = go.Figure(go.Pie(
                    values=hunt_farm.values,
                    labels=hunt_farm.index,
                    hole=0.6,
                    marker_colors=['#0052CC', '#00C7B1'],
                    text=[f'₹{x:,.2f}L' for x in hunt_farm.values],
                    textinfo='label+text+percent'
                ))
                
                fig_hunt_farm.update_layout(
                    title="Hunting vs Farming Distribution",
                    height=400
                )
                
                st.plotly_chart(fig_hunt_farm, use_container_width=True)
            
            with col2:
                # Summary metrics
                total = hunt_farm.sum()
                for type_name, amount in hunt_farm.items():
                    st.metric(
                        f"{type_name}",
                        f"₹{amount:,.2f}L",
                        f"{amount/total*100:.1f}% of Total"
                    )
        
        # 6. Sales Funnel
        st.markdown("### 🔄 Sales Funnel")
        
        if 'Sales Stage' in filtered_df.columns:
            # Calculate funnel metrics
            funnel_metrics = filtered_df.groupby('Sales Stage').agg({
                'Amount': lambda x: x.sum() / 100000,
                'Sales Stage': 'count'
            }).reset_index()
            
            funnel_metrics.columns = ['Stage', 'Amount', 'Count']
            funnel_metrics = funnel_metrics.sort_values('Amount', ascending=False)
            
            # Calculate conversion rates
            total_deals = funnel_metrics['Count'].sum()
            funnel_metrics['Conversion'] = (funnel_metrics['Count'] / total_deals * 100).round(1)
            
            # Create funnel chart
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_metrics['Stage'],
                x=funnel_metrics['Amount'],
                textposition="inside",
                textinfo="value+percent initial",
                opacity=0.65,
                marker={
                    "color": ["#4A90E2", "#45B7AF", "#66BB6A", "#FFA726", "#EF5350"],
                    "line": {"width": [2, 2, 2, 2, 2]}
                },
                connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}},
                text=[f"₹{x:,.2f}L<br>{y} deals<br>{z}% conv." for x, y, z in 
                      zip(funnel_metrics['Amount'], funnel_metrics['Count'], funnel_metrics['Conversion'])]
            ))
            
            fig_funnel.update_layout(
                title="Sales Pipeline Funnel",
                height=500
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        # 7. Optional Enhancers
        st.markdown("### 📌 Additional Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Deal Aging Analysis
            if 'Expected Close Date' in filtered_df.columns:
                aging_df = filtered_df[~filtered_df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
                aging_df['Days Open'] = (pd.Timestamp.now() - aging_df['Expected Close Date']).dt.days
                
                aging_metrics = aging_df.groupby('Sales Stage').agg({
                    'Days Open': 'mean',
                    'Amount': lambda x: x.sum() / 100000
                }).round(1)
                
                st.markdown("#### Deal Aging Analysis")
                st.dataframe(
                    aging_metrics.style.format({
                        'Days Open': '{:.0f} days',
                        'Amount': '₹{:,.2f}L'
                    }),
                    use_container_width=True
                )
        
        with col2:
            # Recent Wins/Losses
            if 'Sales Stage' in filtered_df.columns:
                recent_deals = filtered_df[
                    filtered_df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)
                ].sort_values('Expected Close Date', ascending=False).head(5)
                
                st.markdown("#### Recent Wins/Losses")
                for _, deal in recent_deals.iterrows():
                    status_color = "🟢" if "Won" in deal['Sales Stage'] else "🔴"
                    st.markdown(f"{status_color} {deal['Sales Stage']} - ₹{deal['Amount']/100000:,.2f}L")
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
