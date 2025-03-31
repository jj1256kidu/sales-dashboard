# ... existing code ...

# Custom CSS for modern styling
st.markdown(f"""
    <style>
    /* Main Layout */
    .main {{
        padding: 2rem;
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    
    /* Sticky Navigation */
    .stTabs [data-baseweb="tab-list"] {{
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: {colors['background']};
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid {colors['border']};
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
    
    /* Tab Content Styling */
    .stTabs [data-baseweb="tab-panel"] {{
        padding: 2rem 0;
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
    }}
    
    .table-filter-item {{
        flex: 1;
        min-width: 200px;
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
    </style>
""", unsafe_allow_html=True)

# ... existing code until tabs section ...

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

    # ... existing tab content code until Detailed View tab ...

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
                options=sorted(filtered_df['Practice'].unique()),
                default=[]
            )
        with col2:
            stage_filter = st.multiselect(
                "Sales Stage",
                options=sorted(filtered_df['Sales Stage'].unique()),
                default=[]
            )
        with col3:
            quarter_filter = st.multiselect(
                "Quarter",
                options=sorted(filtered_df['Quarter'].unique()),
                default=[]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_table_df = filtered_df.copy()
        if search_term:
            filtered_table_df = filtered_table_df[
                filtered_table_df['Organization Name'].str.contains(search_term, case=False, na=False) |
                filtered_table_df['Opportunity Number'].str.contains(search_term, case=False, na=False)
            ]
        if practice_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Practice'].isin(practice_filter)]
        if stage_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Sales Stage'].isin(stage_filter)]
        if quarter_filter:
            filtered_table_df = filtered_table_df[filtered_table_df['Quarter'].isin(quarter_filter)]
        
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

# ... rest of the existing code ...
