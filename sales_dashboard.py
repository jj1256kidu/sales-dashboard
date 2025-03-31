# ... existing code ...

    # Calculate KPIs (in Lakhs)
    current_pipeline = filtered_df['Amount'].sum() / 100000
    amount = filtered_df['Amount'].sum() / 100000
    closed_won = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Practice Analysis", "🎯 Deal Distribution", "📋 Detailed View"])

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
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            xaxis_title="Quarter",
            yaxis_title="Amount (Lakhs)",
            showlegend=False
        )
        
        fig.update_traces(
            texttemplate='₹%{text:.2f}L',
            textposition='outside',
            marker_color='#3b82f6'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ... existing code ...
