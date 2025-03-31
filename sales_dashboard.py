# ... existing code until tabs creation ...

    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", 
        "👤 Sales Leaderboard", 
        "📈 Trend View", 
        "🔄 Funnel View", 
        "🎯 Strategy View", 
        "🌍 Geo View", 
        "📋 Detailed View"
    ])

    # Overview Tab (existing code)
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
        
        fig.update_layout(
            title="Distribution of Hunting vs Farming (in Lakhs)",
            showlegend=True,
            annotations=[dict(text='Hunting/Farming', x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
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
                marker_color='#3b82f6'
            ))
            
            fig.add_trace(go.Bar(
                y=owner_metrics['Sales Owner'],
                x=owner_metrics['Closed Won'],
                name='Closed Won',
                orientation='h',
                marker_color='#10b981'
            ))
            
            fig.update_layout(
                title='Sales Owner Performance',
                barmode='overlay',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter"),
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
            line=dict(color='#3b82f6', width=2),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='Monthly Pipeline Trend',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
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
            marker=dict(color='#3b82f6')
        ))
        
        fig.update_layout(
            title='Sales Stage Funnel',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
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
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            showlegend=True
        )
        
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
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter"),
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Region data is not available in the dataset.")

    # Detailed View Tab (existing code)
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

# ... rest of the code ...
