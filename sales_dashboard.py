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

# Borealis-inspired theme colors
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
            'error': '#EF4444',       # Red error
            'input_bg': '#1E293B',    # Input background
            'input_border': '#334155', # Input border
            'input_text': '#E2E8F0',  # Input text
            'select_bg': '#1E293B',   # Select background
            'select_border': '#334155', # Select border
            'select_text': '#E2E8F0', # Select text
            'radio_bg': '#1E293B',    # Radio background
            'radio_border': '#334155', # Radio border
            'radio_text': '#E2E8F0',  # Radio text
            'table_header': '#1E293B', # Table header background
            'table_row': '#1E293B',   # Table row background
            'table_hover': '#2D3748', # Table row hover
            'table_border': '#334155', # Table border
            'table_text': '#E2E8F0',  # Table text
            'sidebar_bg': '#1E293B',  # Sidebar background
            'sidebar_text': '#E2E8F0' # Sidebar text
        }
    else:
        return {
            'background': '#F2F6FF',  # Soft pastel background
            'text': '#1A1A1A',        # Dark text
            'card_bg': '#FFFFFF',     # White cards
            'border': '#E5E7EB',      # Light border
            'primary': '#60A5FA',     # Sky blue accent
            'secondary': '#6B7280',   # Muted gray
            'success': '#3DD598',     # Mint green
            'hover': '#F3F4F6',       # Hover state
            'header': '#FFFFFF',      # Header background
            'metric_bg': '#FFFFFF',   # Metric card background
            'metric_border': '#E5E7EB', # Metric card border
            'accent1': '#A78BFA',     # Lavender accent
            'accent2': '#3DD598',     # Mint green accent
            'warning': '#F59E0B',     # Amber warning
            'error': '#EF4444',       # Red error
            'input_bg': '#FFFFFF',    # Input background
            'input_border': '#E5E7EB', # Input border
            'input_text': '#1A1A1A',  # Input text
            'select_bg': '#FFFFFF',   # Select background
            'select_border': '#E5E7EB', # Select border
            'select_text': '#1A1A1A', # Select text
            'radio_bg': '#FFFFFF',    # Radio background
            'radio_border': '#E5E7EB', # Radio border
            'radio_text': '#1A1A1A',  # Radio text
            'table_header': '#F8FAFC', # Table header background
            'table_row': '#FFFFFF',   # Table row background
            'table_hover': '#F3F4F6', # Table row hover
            'table_border': '#E5E7EB', # Table border
            'table_text': '#1A1A1A',  # Table text
            'sidebar_bg': '#FFFFFF',  # Sidebar background
            'sidebar_text': '#1A1A1A' # Sidebar text
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
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* Title Styling */
    .stTitle {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: {colors['text']};
        margin-bottom: 2rem;
        letter-spacing: -0.025em;
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
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
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
        border-radius: 16px;
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
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(96, 165, 250, 0.2);
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
        letter-spacing: -0.025em;
    }}
    
    /* Metric Cards */
    .stMetric {{
        background-color: {colors['metric_bg']};
        border: 1px solid {colors['metric_border']};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
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
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .stDataFrame thead th {{
        background-color: {colors['table_header']};
        color: {colors['table_text']};
        font-weight: 600;
        padding: 1rem;
        border-bottom: 1px solid {colors['table_border']};
    }}
    
    .stDataFrame tbody td {{
        padding: 1rem;
        border-bottom: 1px solid {colors['table_border']};
        color: {colors['table_text']};
        background-color: {colors['table_row']};
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: {colors['table_hover']};
    }}
    
    /* Table Filters */
    .table-filters {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        background-color: {colors['card_bg']};
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid {colors['border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
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
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 4px rgba(96, 165, 250, 0.2);
    }}
    
    .stButton button:hover {{
        background-color: {colors['primary']};
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(96, 165, 250, 0.3);
    }}
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input {{
        background-color: {colors['input_bg']};
        border: 1px solid {colors['input_border']};
        border-radius: 12px;
        color: {colors['input_text']};
        padding: 0.5rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }}
    
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: {colors['primary']};
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.1);
    }}
    
    /* Select Boxes */
    .stSelectbox select {{
        background-color: {colors['select_bg']};
        border: 1px solid {colors['select_border']};
        color: {colors['select_text']};
        border-radius: 12px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }}
    
    .stSelectbox select:focus {{
        border-color: {colors['primary']};
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.1);
    }}
    
    /* Radio Buttons */
    .stRadio > div {{
        background-color: {colors['radio_bg']};
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid {colors['radio_border']};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background-color: {colors['sidebar_bg']};
        color: {colors['sidebar_text']};
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    /* Custom Table Styling */
    .custom-table {{
        background-color: {colors['card_bg']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid {colors['border']};
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .custom-table table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
    }}
    
    .custom-table th {{
        background-color: {colors['table_header']};
        color: {colors['table_text']};
        font-weight: 600;
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid {colors['table_border']};
    }}
    
    .custom-table td {{
        padding: 1rem;
        border-bottom: 1px solid {colors['table_border']};
        color: {colors['table_text']};
        background-color: {colors['table_row']};
    }}
    
    .custom-table tr:hover td {{
        background-color: {colors['table_hover']};
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
        ["Dark", "Light"],
        index=0 if st.session_state.theme == 'dark' else 1,
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
    # Initialize filtered_df with the original dataframe
    filtered_df = df.copy()
    
    # Configuration Section
    with st.sidebar:
        st.markdown("""
            <div class="section-header">
                <h3>⚙️ Dashboard Configuration</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Available columns for metrics
        available_columns = df.columns.tolist()
        
        # Metric Selection
        st.subheader("📊 Select Metrics to Display")
        selected_metrics = st.multiselect(
            "Choose metrics to show in KPIs",
            options=available_columns,
            default=['Amount', 'Probability', 'Sales Stage']
        )
        
        # Graph Selection
        st.subheader("📈 Select Graphs to Display")
        graph_options = {
            "Quarter-wise Breakdown": "quarter_breakdown",
            "Hunting vs Farming": "hunting_farming",
            "Sales Leaderboard": "sales_leaderboard",
            "Monthly Trend": "monthly_trend",
            "Sales Funnel": "sales_funnel",
            "Strategy View": "strategy_view",
            "Geography View": "geo_view"
        }
        selected_graphs = st.multiselect(
            "Choose graphs to display",
            options=list(graph_options.keys()),
            default=list(graph_options.keys())
        )
        
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
        
        st.markdown("""
            <div class="section-header">
                <h3>🔍 Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Dynamic filter creation based on available columns
        for column in available_columns:
            if column not in ['Amount', 'Probability']:  # Skip numeric columns
                unique_values = safe_sort_unique(df[column])
                if len(unique_values) > 0:
                    selected_value = st.selectbox(
                        f"Filter by {column}",
                        ['All'] + unique_values
                    )
                    if selected_value != 'All':
                        filtered_df = filtered_df[filtered_df[column].astype(str) == selected_value]

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
        
        # Dynamic KPI display based on selected metrics
        num_cols = min(3, len(selected_metrics))
        kpi_cols = st.columns(num_cols)
        for idx, metric in enumerate(selected_metrics):
            with kpi_cols[idx % num_cols]:
                if metric == 'Amount':
                    value = filtered_df['Amount'].sum() / 100000
                    st.metric(
                        "Total Amount",
                        format_lakhs(value * 100000),
                        delta=None,
                        delta_color="normal"
                    )
                elif metric == 'Probability':
                    value = filtered_df['Probability'].mean()
                    st.metric(
                        "Average Probability",
                        f"{value:.1f}%",
                        delta=None,
                        delta_color="normal"
                    )
                elif metric == 'Sales Stage':
                    won_count = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
                    st.metric(
                        "Closed Won",
                        format_lakhs(won_count * 100000),
                        delta=None,
                        delta_color="normal"
                    )
                else:
                    # For other metrics, show count or sum based on data type
                    if pd.api.types.is_numeric_dtype(filtered_df[metric]):
                        value = filtered_df[metric].sum()
                    else:
                        value = filtered_df[metric].nunique()
                    st.metric(
                        metric,
                        str(value),
                        delta=None,
                        delta_color="normal"
                    )

        # Display selected graphs in Overview tab
        for graph_name in selected_graphs:
            graph_id = graph_options[graph_name]
            
            st.markdown(f"""
                <div class="section-header">
                    <h3>{graph_name}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            if graph_id == "quarter_breakdown":
                # Quarter-wise Breakdown
                quarter_metrics = filtered_df.groupby('Quarter').agg({
                    'Amount': ['sum', 'count'],
                    'Probability': 'mean'
                }).reset_index()
                
                quarter_metrics.columns = ['Quarter', 'Total Amount (Lakhs)', 'Number of Deals', 'Avg Probability']
                quarter_metrics['Total Amount (Lakhs)'] = quarter_metrics['Total Amount (Lakhs)'] / 100000
                
                st.dataframe(
                    quarter_metrics.style.format({
                        'Total Amount (Lakhs)': '₹{:.2f}L',
                        'Avg Probability': '{:.1f}%'
                    }),
                    use_container_width=True
                )
                
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"quarter_breakdown_{graph_name}")
            
            elif graph_id == "hunting_farming" and 'Hunting/Farming' in filtered_df.columns:
                # Hunting vs Farming Distribution
                hunting_farming = filtered_df.groupby('Hunting/Farming')['Amount'].sum().reset_index()
                total_amount = hunting_farming['Amount'].sum()
                
                if total_amount > 0:
                    hunting_farming['Percentage'] = (hunting_farming['Amount'] / total_amount * 100).round(1)
                    
                    fig = go.Figure(data=[go.Pie(
                        labels=hunting_farming['Hunting/Farming'],
                        values=hunting_farming['Amount'] / 100000,
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
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"hunting_farming_{graph_name}")
                    
                    # Display metrics table
                    hunting_farming_metrics = hunting_farming.copy()
                    hunting_farming_metrics['Amount'] = hunting_farming_metrics['Amount'] / 100000
                    
                    table_html = f"""
                    <div class="custom-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Type</th>
                                    <th>Amount (Lakhs)</th>
                                    <th>Percentage</th>
                                </tr>
                            </thead>
                            <tbody>
                    """
                    
                    for _, row in hunting_farming_metrics.iterrows():
                        table_html += f"""
                                <tr>
                                    <td>{row['Hunting/Farming']}</td>
                                    <td>₹{row['Amount']:.2f}L</td>
                                    <td>{row['Percentage']:.1f}%</td>
                                </tr>
                        """
                    
                    table_html += """
                            </tbody>
                        </table>
                    </div>
                    """
                    
                    st.markdown(table_html, unsafe_allow_html=True)
            
            elif graph_id == "sales_leaderboard" and 'Sales Owner' in filtered_df.columns:
                # Sales Leaderboard
                owner_metrics = filtered_df.groupby('Sales Owner').agg({
                    'Amount': 'sum',
                    'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
                }).reset_index()
                
                owner_metrics.columns = ['Sales Owner', 'Total Pipeline', 'Closed Won']
                owner_metrics['Total Pipeline'] = owner_metrics['Total Pipeline'] / 100000
                owner_metrics['Closed Won'] = owner_metrics['Closed Won'] / 100000
                owner_metrics['Win Rate'] = (owner_metrics['Closed Won'] / owner_metrics['Total Pipeline'] * 100).round(1)
                
                owner_metrics = owner_metrics.sort_values('Total Pipeline', ascending=False)
                
                st.dataframe(
                    owner_metrics.style.format({
                        'Total Pipeline': '₹{:.2f}L',
                        'Closed Won': '₹{:.2f}L',
                        'Win Rate': '{:.1f}%'
                    }),
                    use_container_width=True
                )
                
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"sales_leaderboard_{graph_name}")
            
            elif graph_id == "monthly_trend":
                # Monthly Trend
                filtered_df['Date'] = pd.to_datetime(filtered_df['Expected Close Date'], errors='coerce')
                monthly_metrics = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).agg({
                    'Amount': 'sum',
                    'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
                }).reset_index()
                
                monthly_metrics['Date'] = monthly_metrics['Date'].astype(str)
                monthly_metrics['Amount'] = monthly_metrics['Amount'] / 100000
                
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"monthly_trend_{graph_name}")
            
            elif graph_id == "sales_funnel":
                # Sales Funnel
                stage_metrics = filtered_df.groupby('Sales Stage').agg({
                    'Amount': 'sum',
                    'Opportunity Number': 'count'
                }).reset_index()
                
                stage_metrics['Amount'] = stage_metrics['Amount'] / 100000
                
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"sales_funnel_{graph_name}")
            
            elif graph_id == "strategy_view":
                # Strategy View
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"strategy_view_{graph_name}")
            
            elif graph_id == "geo_view":
                # Geography View
                geography_columns = ['Region', 'Country', 'Geography']
                available_geo_column = next((col for col in geography_columns if col in filtered_df.columns), None)
                
                if available_geo_column:
                    geo_metrics = filtered_df.groupby(available_geo_column).agg({
                        'Amount': 'sum',
                        'Opportunity Number': 'count'
                    }).reset_index()
                    
                    geo_metrics['Amount'] = geo_metrics['Amount'] / 100000
                    
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
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"geo_view_{graph_name}")
                    
                    st.dataframe(
                        geo_metrics.style.format({
                            'Amount': '₹{:.2f}L',
                            'Opportunity Number': '{:,.0f}'
                        }),
                        use_container_width=True
                    )

    # Remove duplicate graph displays from other tabs
    # Keep only the detailed view and data tables in their respective tabs
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
        else:
            st.info("Sales Owner data is not available in the dataset.")

    # Keep the rest of the tabs for detailed data views
    with tab3:
        st.markdown("""
            <div class="section-header">
                <h3>📈 Trend View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display monthly trend data table
        filtered_df['Date'] = pd.to_datetime(filtered_df['Expected Close Date'], errors='coerce')
        monthly_metrics = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).agg({
            'Amount': 'sum',
            'Sales Stage': lambda x: (x.isin(['Closed Won', 'Won'])).sum()
        }).reset_index()
        
        monthly_metrics['Date'] = monthly_metrics['Date'].astype(str)
        monthly_metrics['Amount'] = monthly_metrics['Amount'] / 100000
        
        st.dataframe(
            monthly_metrics.style.format({
                'Amount': '₹{:.2f}L'
            }),
            use_container_width=True
        )

    with tab4:
        st.markdown("""
            <div class="section-header">
                <h3>🔄 Funnel View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display funnel data table
        stage_metrics = filtered_df.groupby('Sales Stage').agg({
            'Amount': 'sum',
            'Opportunity Number': 'count'
        }).reset_index()
        
        stage_metrics['Amount'] = stage_metrics['Amount'] / 100000
        
        st.dataframe(
            stage_metrics.style.format({
                'Amount': '₹{:.2f}L'
            }),
            use_container_width=True
        )

    with tab5:
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Strategy View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display strategy data table
        strategy_metrics = filtered_df.groupby('Practice').agg({
            'Amount': 'sum',
            'Probability': 'mean',
            'Opportunity Number': 'count'
        }).reset_index()
        
        strategy_metrics['Amount'] = strategy_metrics['Amount'] / 100000
        
        st.dataframe(
            strategy_metrics.style.format({
                'Amount': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

    with tab6:
        st.markdown("""
            <div class="section-header">
                <h3>🌍 Geo View</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display geography data table
        geography_columns = ['Region', 'Country', 'Geography']
        available_geo_column = next((col for col in geography_columns if col in filtered_df.columns), None)
        
        if available_geo_column:
            geo_metrics = filtered_df.groupby(available_geo_column).agg({
                'Amount': 'sum',
                'Opportunity Number': 'count'
            }).reset_index()
            
            geo_metrics['Amount'] = geo_metrics['Amount'] / 100000
            
            st.dataframe(
                geo_metrics.style.format({
                    'Amount': '₹{:.2f}L',
                    'Opportunity Number': '{:,.0f}'
                }),
                use_container_width=True
            )
        else:
            st.info("No geography data (Region, Country, or Geography) is available in the dataset.")

    # Keep the Detailed View tab as is
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
