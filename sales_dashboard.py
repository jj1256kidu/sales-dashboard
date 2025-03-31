import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Borealis theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'background': '#0F172A',  # Dark slate background
            'text': '#E2E8F0',        # Light gray text
            'card_bg': '#1E293B',     # Slightly lighter slate for cards
            'border': '#334155',      # Border color
            'primary': '#3B82F6',     # Blue accent
            'secondary': '#94A3B8',   # Muted gray
            'success': '#10B981',     # Green for success
            'hover': '#2D3748',       # Hover state
            'header': '#1E293B',      # Header background
            'metric_bg': '#1E293B',   # Metric card background
            'metric_border': '#334155', # Metric card border
            'accent1': '#6366F1',     # Indigo accent
            'accent2': '#EC4899',     # Pink accent
            'warning': '#F59E0B',     # Amber warning
            'error': '#EF4444'        # Red error
        }
    else:
        return {
            'background': '#F8FAFC',  # Light background
            'text': '#1E293B',        # Dark text
            'card_bg': '#FFFFFF',     # White cards
            'border': '#E2E8F0',      # Light border
            'primary': '#3B82F6',     # Blue accent
            'secondary': '#64748B',   # Muted gray
            'success': '#10B981',     # Green for success
            'hover': '#F1F5F9',       # Hover state
            'header': '#FFFFFF',      # Header background
            'metric_bg': '#FFFFFF',   # Metric card background
            'metric_border': '#E2E8F0', # Metric card border
            'accent1': '#6366F1',     # Indigo accent
            'accent2': '#EC4899',     # Pink accent
            'warning': '#F59E0B',     # Amber warning
            'error': '#EF4444'        # Red error
        }

# Set page config with full page mode
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Get current theme colors
colors = get_theme_colors()

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

def safe_sort_unique(series):
    """Safely sort unique values from a series, handling mixed types."""
    unique_values = series.unique()
    return sorted([str(x) for x in unique_values if pd.notna(x)])

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

# Custom CSS for modern corporate styling
st.markdown(f"""
    <style>
    /* Main Layout */
    .main {{
        padding: 0;
        background-color: {colors['background']};
        color: {colors['text']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header Styling */
    .stApp header {{
        background-color: {colors['header']};
        border-bottom: 1px solid {colors['border']};
        padding: 1rem 2rem;
    }}
    
    /* Title Styling */
    .stTitle {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: {colors['text']};
        margin-bottom: 2rem;
    }}
    
    /* Sticky Navigation */
    .stTabs [data-baseweb="tab-list"] {{
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: {colors['header']};
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: transparent;
        padding: 0.5rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 60px;
        white-space: pre-wrap;
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 0 1.5rem;
        color: {colors['secondary']};
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid {colors['border']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 200px;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        background-color: {colors['hover']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {colors['primary']};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        border: none;
        font-weight: 600;
    }}
    
    /* Section Headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    .section-header h3 {{
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['text']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Metric Cards */
    .stMetric {{
        background-color: {colors['metric_bg']};
        border: 1px solid {colors['metric_border']};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }}
    
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['primary']};
    }}
    
    .stMetric [data-testid="stMetricLabel"] {{
        font-size: 0.875rem;
        color: {colors['secondary']};
    }}
    
    /* Detailed View Table */
    .stDataFrame {{
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
        margin-top: 1rem;
    }}
    
    .stDataFrame thead th {{
        background-color: {colors['hover']};
        color: {colors['text']};
        font-weight: 600;
        padding: 1rem;
        border-bottom: 1px solid {colors['border']};
    }}
    
    .stDataFrame tbody td {{
        padding: 1rem;
        border-bottom: 1px solid {colors['border']};
        color: {colors['text']};
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: {colors['hover']};
    }}
    
    /* Table Filters */
    .table-filters {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        background-color: {colors['card_bg']};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    .table-filter-item {{
        flex: 1;
        min-width: 200px;
    }}
    
    /* Buttons */
    .stButton button {{
        background-color: {colors['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }}
    
    .stButton button:hover {{
        background-color: {colors['primary']};
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
    }}
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input {{
        background-color: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        color: {colors['text']};
        padding: 0.5rem;
        font-family: 'Inter', sans-serif;
    }}
    
    /* Radio Buttons */
    .stRadio > div {{
        background-color: {colors['card_bg']};
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .stTabs [data-baseweb="tab"] {{
            min-width: 100%;
            margin-bottom: 0.5rem;
        }}
        
        .table-filters {{
            flex-direction: column;
        }}
        
        .table-filter-item {{
            width: 100%;
        }}
    }}
    
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['background']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['border']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['secondary']};
    }}
    </style>
""", unsafe_allow_html=True)

# Title and Header with theme toggle
col1, col2 = st.columns([6, 1])
with col1:
    st.title("📊 Sales Dashboard")
with col2:
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        key='theme_selector'
    )
    st.session_state.theme = theme.lower()

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
                <h3>⚙️ Settings</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Sales Target Input
        sales_target = st.number_input(
            "Enter Sales Target (in Lakhs)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )
        
        st.markdown("""
            <div class="section-header">
                <h3>🔍 Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Practice filter
        practices = ['All'] + safe_sort_unique(df['Practice'])
        selected_practice = st.selectbox("Practice", practices)
        
        # Quarter filter
        quarters = ['All'] + safe_sort_unique(df['Quarter'])
        selected_quarter = st.selectbox("Quarter", quarters)
        
        # Hunting/Farming filter
        deal_types = ['All'] + safe_sort_unique(df['Hunting/Farming'])
        selected_deal_type = st.selectbox("Hunting/Farming", deal_types)
        
        # Sales Owner filter (if available)
        if 'Sales Owner' in df.columns:
            sales_owners = ['All'] + safe_sort_unique(df['Sales Owner'])
            selected_sales_owner = st.selectbox("Sales Owner", sales_owners)
        
        # Tech Owner filter (if available)
        if 'Tech Owner' in df.columns:
            tech_owners = ['All'] + safe_sort_unique(df['Tech Owner'])
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
        "🧾 Detailed View"
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
        
        # Create donut chart with custom colors
        fig = go.Figure(data=[go.Pie(
            labels=hunting_farming['Hunting/Farming'],
            values=hunting_farming['Amount'] / 100000,  # Convert to Lakhs
            hole=.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(
                colors=[colors['accent1'], colors['accent2']],
                line=dict(color=colors['card_bg'], width=2)
            )
        )])
        
        fig = apply_theme_to_plot(fig)
        fig.update_layout(
            title="Distribution of Hunting vs Farming (in Lakhs)",
            showlegend=True,
            annotations=[dict(
                text='Hunting/Farming',
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
                font_color=colors['text']
            )],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Display hunting/farming metrics table
        st.markdown("""
            <div class="section-header">
                <h3>📊 Hunting/Farming Metrics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        hunting_farming_metrics = hunting_farming.copy()
        hunting_farming_metrics['Amount'] = hunting_farming_metrics['Amount'] / 100000
        
        st.dataframe(
            hunting_farming_metrics.style.format({
                'Amount': '₹{:.2f}L',
                'Percentage': '{:.1f}%'
            }),
            use_container_width=True
        )

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
        
        # Check for available geography columns
        geography_columns = ['Region', 'Country', 'Geography']
        available_geo_column = next((col for col in geography_columns if col in filtered_df.columns), None)
        
        if available_geo_column:
            # Calculate geography-wise metrics
            geo_metrics = filtered_df.groupby(available_geo_column).agg({
                'Amount': 'sum',
                'Opportunity Number': 'count'
            }).reset_index()
            
            geo_metrics['Amount'] = geo_metrics['Amount'] / 100000
            
            # Create choropleth map
            fig = px.choropleth(
                geo_metrics,
                locations=available_geo_column,
                locationmode='country names' if available_geo_column in ['Country', 'Geography'] else None,
                color='Amount',
                hover_data=['Opportunity Number'],
                title=f'{available_geo_column}-wise Pipeline Distribution',
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
            
            # Display geography metrics table
            st.markdown("""
                <div class="section-header">
                    <h3>📊 Geography Metrics</h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                geo_metrics.style.format({
                    'Amount': '₹{:.2f}L',
                    'Opportunity Number': '{:,.0f}'
                }),
                use_container_width=True
            )
        else:
            st.info("No geography data (Region, Country, or Geography) is available in the dataset.")

    # Detailed View Tab
    with tab7:
        st.markdown("""
            <div class="section-header">
                <h3>🧾 Detailed Deals</h3>
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
        
        # Table filters
        st.markdown('<div class="table-filters">', unsafe_allow_html=True)
        
        # Search filter
        search_term = st.text_input("🔍 Search", key="table_search")
        
        # Column filters
        col1, col2, col3 = st.columns(3)
        with col1:
            practice_filter = st.multiselect(
                "Practice",
                options=safe_sort_unique(filtered_df['Practice']),
                default=[]
            )
        with col2:
            stage_filter = st.multiselect(
                "Sales Stage",
                options=safe_sort_unique(filtered_df['Sales Stage']),
                default=[]
            )
        with col3:
            quarter_filter = st.multiselect(
                "Quarter",
                options=safe_sort_unique(filtered_df['Quarter']),
                default=[]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_table_df = filtered_df.copy()
        if search_term:
            filtered_table_df = filtered_table_df[
                filtered_table_df['Organization Name'].astype(str).str.contains(search_term, case=False, na=False) |
                filtered_table_df['Opportunity Number'].astype(str).str.contains(search_term, case=False, na=False)
            ]
        if practice_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Practice'].astype(str).isin(practice_filter)]
        if stage_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Sales Stage'].astype(str).isin(stage_filter)]
        if quarter_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Quarter'].astype(str).isin(quarter_filter)]
        
        # Display table with formatting and column configuration
        st.dataframe(
            filtered_table_df[available_columns].style.format({
                'Amount': '₹{:.2f}L',
                'Weighted Revenue': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True,
            height=600
        )

        # Export options
        col1, col2 = st.columns(2)
        with col1:
            # Export to CSV
            csv = filtered_table_df[available_columns].to_csv(index=False)
            st.download_button(
                label="📥 Export to CSV",
                data=csv,
                file_name="filtered_deals.csv",
                mime="text/csv"
            )
        with col2:
            # Export to Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                filtered_table_df[available_columns].to_excel(writer, index=False, sheet_name='Deals')
            excel_buffer.seek(0)
            st.download_button(
                label="📊 Export to Excel",
                data=excel_buffer,
                file_name="filtered_deals.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
else:
    st.info("Please upload data to view the dashboard.")
