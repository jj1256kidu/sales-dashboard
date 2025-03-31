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

# ... existing code ...

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

# ... existing code ...

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

# ... rest of the existing code ...
