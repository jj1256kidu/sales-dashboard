import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'background': '#1a1a1a',
            'text': '#ffffff',
            'card_bg': '#2d2d2d',
            'border': '#404040',
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'hover': '#3d3d3d'
        }
    else:
        return {
            'background': '#f8fafc',
            'text': '#1e293b',
            'card_bg': '#ffffff',
            'border': '#e2e8f0',
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'hover': '#f1f5f9'
        }

# Set page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get current theme colors
colors = get_theme_colors()

# Custom CSS for modern styling
st.markdown(f"""
    <style>
    /* Main Layout */
    .main {{
        padding: 2rem;
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background-color: {colors['card_bg']};
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
    }}
    
    /* Header Styling */
    .css-1v0mbdj {{
        margin-bottom: 2rem;
        color: {colors['text']};
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: transparent;
        padding: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: {colors['hover']};
        border-radius: 12px;
        padding: 0 1.5rem;
        color: {colors['secondary']};
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid {colors['border']};
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {colors['primary']};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        border: none;
    }}
    
    /* Metric Cards */
    .stMetric {{
        background-color: {colors['card_bg']};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border: 1px solid {colors['border']};
        transition: all 0.3s ease;
    }}
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {colors['text']};
    }}
    .stMetric [data-testid="stMetricLabel"] {{
        color: {colors['secondary']};
    }}
    
    /* DataFrames */
    .stDataFrame {{
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {colors['text']};
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Selectbox Styling */
    .stSelectbox {{
        background-color: {colors['card_bg']};
        border-radius: 8px;
        border: 1px solid {colors['border']};
    }}
    .stSelectbox select {{
        color: {colors['text']};
    }}
    
    /* Radio Buttons */
    .stRadio > div {{
        background-color: {colors['card_bg']};
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid {colors['border']};
    }}
    .stRadio label {{
        color: {colors['text']};
    }}
    
    /* Number Input */
    .stNumberInput input {{
        border-radius: 8px;
        border: 1px solid {colors['border']};
        background-color: {colors['card_bg']};
        color: {colors['text']};
    }}
    
    /* Download Button */
    .stDownloadButton button {{
        background-color: {colors['primary']};
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    .stDownloadButton button:hover {{
        background-color: {colors['primary']};
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
    }}
    
    /* Section Headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    /* Info Messages */
    .stInfo {{
        background-color: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 1rem;
        color: {colors['text']};
    }}
    
    /* Error Messages */
    .stError {{
        background-color: {colors['card_bg']};
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        color: #ef4444;
    }}
    </style>
""", unsafe_allow_html=True)

# Helper functions
def format_lakhs(value):
    try:
        return f"₹{float(value)/100000:,.2f}L"
    except (ValueError, TypeError):
        return "₹0.00L"

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def apply_theme_to_plot(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Inter",
            color=colors['text']
        ),
        xaxis=dict(
            gridcolor=colors['border'],
            color=colors['text']
        ),
        yaxis=dict(
            gridcolor=colors['border'],
            color=colors['text']
        ),
        legend=dict(
            font=dict(color=colors['text'])
        )
    )
    return fig

# Title and Header
st.title("📊 Sales Dashboard")

# Sidebar
with st.sidebar:
    st.markdown("""
        <div class="section-header">
            <h3>⚙️ Settings</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        key='theme_selector'
    )
    
    # Update session state theme
    st.session_state.theme = theme.lower()
    
    # Sales Target Input
    st.markdown("""
        <div class="section-header">
            <h3>🎯 Sales Target</h3>
        </div>
    """, unsafe_allow_html=True)
    
    sales_target = st.number_input(
        "Enter Sales Target (in Lakhs)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

# Data Input Section
st.markdown("""
    <div class="section-header">
        <h3>📁 Data Input</h3>
    </div>
""", unsafe_allow_html=True)

input_method = st.radio("Choose data input method:", ["Excel File", "Google Sheet URL"])

df = None
if input_method == "Excel File":
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Raw_Data')
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
else:
    sheet_url = st.text_input("Paste Google Sheet URL")
    if sheet_url:
        try:
            csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(csv_url)
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Google Sheet: {str(e)}")

if df is not None:
    # Sidebar Filters
    with st.sidebar:
        st.markdown("""
            <div class="section-header">
                <h3>🔍 Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Practice filter
        practices = ['All'] + sorted(df['Practice'].astype(str).unique().tolist())
        selected_practice = st.selectbox("Practice", practices)
        
        # Quarter filter
        quarters = ['All'] + sorted(df['Quarter'].astype(str).unique().tolist())
        selected_quarter = st.selectbox("Quarter", quarters)
        
        # Hunting/Farming filter
        deal_types = ['All'] + sorted(df['Hunting/Farming'].astype(str).unique().tolist())
        selected_deal_type = st.selectbox("Hunting/Farming", deal_types)
        
        # Sales Owner filter (if available)
        if 'Sales Owner' in df.columns:
            sales_owners = ['All'] + sorted(df['Sales Owner'].astype(str).unique().tolist())
            selected_sales_owner = st.selectbox("Sales Owner", sales_owners)
        
        # Tech Owner filter (if available)
        if 'Tech Owner' in df.columns:
            tech_owners = ['All'] + sorted(df['Tech Owner'].astype(str).unique().tolist())
            selected_tech_owner = st.selectbox("Tech Owner", tech_owners)

    # Apply filters
    filtered_df = df.copy()
    if selected_practice != 'All':
        filtered_df = filtered_df[filtered_df['Practice'].astype(str) == selected_practice]
    if selected_quarter != 'All':
        filtered_df = filtered_df[filtered_df['Quarter'].astype(str) == selected_quarter]
    if selected_deal_type != 'All':
        filtered_df = filtered_df[filtered_df['Hunting/Farming'].astype(str) == selected_deal_type]
    if 'Sales Owner' in df.columns and selected_sales_owner != 'All':
        filtered_df = filtered_df[filtered_df['Sales Owner'].astype(str) == selected_sales_owner]
    if 'Tech Owner' in df.columns and selected_tech_owner != 'All':
        filtered_df = filtered_df[filtered_df['Tech Owner'].astype(str) == selected_tech_owner]

    # Calculate KPIs (in Lakhs)
    current_pipeline = filtered_df['Amount'].sum() / 100000
    amount = filtered_df['Amount'].sum() / 100000
    closed_won = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Create tabs with improved styling
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", 
        "👤 Sales Leaderboard", 
        "📈 Trend View", 
        "🔄 Funnel View", 
        "🎯 Strategy View", 
        "🌍 Geo View", 
        "📋 Detailed View"
    ])

    # Overview Tab
    with tab1:
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Key Performance Indicators</h3>
            </div>
        """, unsafe_allow_html=True)
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(
                "Sales Target",
                format_lakhs(sales_target * 100000),
                delta=None,
                delta_color="normal"
            )
            st.metric(
                "Current Pipeline",
                format_lakhs(current_pipeline * 100000),
                delta=None,
                delta_color="normal"
            )
        
        with kpi_col2:
            st.metric(
                "Amount",
                format_lakhs(amount * 100000),
                delta=None,
                delta_color="normal"
            )
            st.metric(
                "Closed Won",
                format_lakhs(closed_won * 100000),
                delta=None,
                delta_color="normal"
            )
        
        with kpi_col3:
            st.metric(
                "Achieved %",
                f"{achieved_percentage:.1f}%",
                delta=None,
                delta_color="normal"
            )

        # Quarter-wise Breakdown
        st.markdown("""
            <div class="section-header">
                <h3>📅 Quarter-wise Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate quarter-wise metrics
        quarter_metrics = filtered_df.groupby('Quarter').agg({
            'Amount': ['sum', 'count'],
            'Probability': 'mean'
        }).reset_index()
        
        quarter_metrics.columns = ['Quarter', 'Total Amount (Lakhs)', 'Number of Deals', 'Avg Probability']
        quarter_metrics['Total Amount (Lakhs)'] = quarter_metrics['Total Amount (Lakhs)'] / 100000
        
        # Display quarter summary table
        st.dataframe(
            quarter_metrics.style.format({
                'Total Amount (Lakhs)': '₹{:.2f}L',
                'Avg Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

        # Create quarter-wise bar chart
        fig = px.bar(
            quarter_metrics,
            x='Quarter',
            y='Total Amount (Lakhs)',
            title='Quarter-wise Pipeline Distribution',
            text='Total Amount (Lakhs)',
            labels={'Total Amount (Lakhs)': 'Amount (Lakhs)'}
        )
        
        fig = apply_theme_to_plot(fig)
        fig.update_traces(
            texttemplate='₹%{text:.2f}L',
            textposition='outside',
            marker_color=colors['primary']
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Hunting vs Farming Distribution
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Hunting vs Farming Distribution</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate percentages
        hunting_farming = filtered_df.groupby('Hunting/Farming')['Amount'].sum().reset_index()
        total_amount = hunting_farming['Amount'].sum()
        hunting_farming['Percentage'] = (hunting_farming['Amount'] / total_amount * 100).round(1)
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=hunting_farming['Hunting/Farming'],
            values=hunting_farming['Amount'] / 100000,  # Convert to Lakhs
            hole=.4,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig = apply_theme_to_plot(fig)
        fig.update_layout(
            title="Distribution of Hunting vs Farming (in Lakhs)",
            showlegend=True,
            annotations=[dict(text='Hunting/Farming', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Sales Leaderboard Tab
    with tab2:
        st.markdown("""
            <div class="section-header">
                <h3>👤 Sales Leaderboard</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if 'Sales Owner' in filtered_df.columns:
            # Calculate owner-wise metrics
            owner_metrics = filtered_df.groupby('Sales Owner').agg({
                'Amount': 'sum',
                'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
            }).reset_index()
            
            owner_metrics.columns = ['Sales Owner', 'Total Pipeline', 'Closed Won']
            owner_metrics['Total Pipeline'] = owner_metrics['Total Pipeline'] / 100000
            owner_metrics['Closed Won'] = owner_metrics['Closed Won'] / 100000
            owner_metrics['Win Rate'] = (owner_metrics['Closed Won'] / owner_metrics['Total Pipeline'] * 100).round(1)
            
            # Sort by Total Pipeline
            owner_metrics = owner_metrics.sort_values('Total Pipeline', ascending=False)
            
            # Display owner metrics table
            st.dataframe(
                owner_metrics.style.format({
                    'Total Pipeline': '₹{:.2f}L',
                    'Closed Won': '₹{:.2f}L',
                    'Win Rate': '{:.1f}%'
                }),
                use_container_width=True
            )
            
            # Create horizontal bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=owner_metrics['Sales Owner'],
                x=owner_metrics['Total Pipeline'],
                name='Total Pipeline',
                orientation='h',
                marker_color=colors['primary']
            ))
            
            fig.add_trace(go.Bar(
                y=owner_metrics['Sales Owner'],
                x=owner_metrics['Closed Won'],
                name='Closed Won',
                orientation='h',
                marker_color=colors['success']
            ))
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                title='Sales Owner Performance',
                barmode='overlay',
                xaxis_title='Amount (Lakhs)',
                yaxis_title='Sales Owner',
                showlegend=True
            )
            
            fig.update_traces(texttemplate='₹%{x:.2f}L', textposition='auto')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sales Owner data is not available in the dataset.")

    # Trend View Tab
    with tab3:
        st.markdown("""
            <div class="section-header">
                <h3>📈 Trend View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate monthly metrics
        filtered_df['Date'] = pd.to_datetime(filtered_df['Expected Close Date'], errors='coerce')
        monthly_metrics = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).agg({
            'Amount': 'sum',
            'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
        }).reset_index()
        
        monthly_metrics['Date'] = monthly_metrics['Date'].astype(str)
        monthly_metrics['Amount'] = monthly_metrics['Amount'] / 100000
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_metrics['Date'],
            y=monthly_metrics['Amount'],
            name='Pipeline',
            line=dict(color=colors['primary'], width=2),
            mode='lines+markers'
        ))
        
        fig = apply_theme_to_plot(fig)
        fig.update_layout(
            title='Monthly Pipeline Trend',
            xaxis_title='Month',
            yaxis_title='Amount (Lakhs)',
            showlegend=True
        )
        
        fig.update_traces(texttemplate='₹%{y:.2f}L', textposition='top center')
        
        st.plotly_chart(fig, use_container_width=True)

    # Funnel View Tab
    with tab4:
        st.markdown("""
            <div class="section-header">
                <h3>🔄 Funnel View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate stage-wise metrics
        stage_metrics = filtered_df.groupby('Sales Stage').agg({
            'Amount': 'sum',
            'Opportunity Number': 'count'
        }).reset_index()
        
        stage_metrics['Amount'] = stage_metrics['Amount'] / 100000
        
        # Create funnel chart
        fig = go.Figure(go.Funnel(
            y=stage_metrics['Sales Stage'],
            x=stage_metrics['Amount'],
            textinfo='value+percent initial',
            texttemplate='₹%{value:.2f}L',
            textposition='inside',
            marker=dict(color=colors['primary'])
        ))
        
        fig = apply_theme_to_plot(fig)
        fig.update_layout(
            title='Sales Stage Funnel',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Strategy View Tab
    with tab5:
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Strategy View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Create bubble chart
        fig = px.scatter(
            filtered_df,
            x='Probability',
            y='Amount',
            size='Amount',
            color='Practice',
            hover_data=['Organization Name', 'Sales Stage'],
            title='Deal Value vs Probability by Practice',
            labels={
                'Amount': 'Deal Value (Lakhs)',
                'Probability': 'Probability (%)',
                'Practice': 'Practice'
            }
        )
        
        fig = apply_theme_to_plot(fig)
        fig.update_traces(
            texttemplate='₹%{y:.2f}L',
            textposition='top center'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Geo View Tab
    with tab6:
        st.markdown("""
            <div class="section-header">
                <h3>🌍 Geo View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if 'Region' in filtered_df.columns:
            # Calculate region-wise metrics
            region_metrics = filtered_df.groupby('Region').agg({
                'Amount': 'sum',
                'Opportunity Number': 'count'
            }).reset_index()
            
            region_metrics['Amount'] = region_metrics['Amount'] / 100000
            
            # Create choropleth map
            fig = px.choropleth(
                region_metrics,
                locations='Region',
                locationmode='country names',
                color='Amount',
                hover_data=['Opportunity Number'],
                title='Regional Pipeline Distribution',
                color_continuous_scale='Viridis'
            )
            
            fig = apply_theme_to_plot(fig)
            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Region data is not available in the dataset.")

    # Detailed View Tab
    with tab7:
        st.markdown("""
            <div class="section-header">
                <h3>📋 Detailed Deals</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Add Weighted Revenue column
        filtered_df['Weighted Revenue'] = filtered_df['Amount'] * filtered_df['Probability'] / 100
        
        # Define columns for display
        columns_to_show = [
            'Opportunity Number',
            'Organization Name',
            'Amount',
            'Probability',
            'Weighted Revenue',
            'Quarter',
            'Practice',
            'Sales Stage',
            'Tech Owner',
            'Sales Owner',
            'Expected Close Date'
        ]
        
        # Filter columns that exist in the dataframe
        available_columns = [col for col in columns_to_show if col in filtered_df.columns]
        
        # Display table with formatting
        st.dataframe(
            filtered_df[available_columns].style.format({
                'Amount': '₹{:.2f}L',
                'Weighted Revenue': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

        # Export to CSV option
        csv = filtered_df[available_columns].to_csv(index=False)
        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name="filtered_deals.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload data to view the dashboard.")
