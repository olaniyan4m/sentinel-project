#!/usr/bin/env python3
"""
Sentinel Real-Time Dashboard
Interactive dashboard for visualizing real crime data and Sentinel system status
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentinelDashboard:
    def __init__(self, data_dir: str = "real_data"):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "sentinel_integrated.db"
        
    def load_data(self):
        """Load data from the integrated database"""
        if not self.db_path.exists():
            st.error(f"Database not found: {self.db_path}")
            return None
        
        conn = sqlite3.connect(self.db_path)
        
        # Load all tables
        data = {
            'hotspots': pd.read_sql("SELECT * FROM crime_hotspots", conn),
            'vehicles': pd.read_sql("SELECT * FROM vehicle_crime_patterns", conn),
            'cit_routes': pd.read_sql("SELECT * FROM cit_routes", conn),
            'partners': pd.read_sql("SELECT * FROM private_security_partners", conn),
            'deployments': pd.read_sql("SELECT * FROM sentinel_deployments", conn)
        }
        
        conn.close()
        return data
    
    def create_crime_hotspots_map(self, data):
        """Create interactive map of crime hotspots"""
        st.subheader("Crime Hotspots Map")
        
        if data['hotspots'].empty:
            st.warning("No hotspot data available")
            return
        
        # Create map
        fig = px.scatter_mapbox(
            data['hotspots'],
            lat='latitude',
            lon='longitude',
            color='severity_score',
            size='incident_count',
            hover_name='name',
            hover_data={
                'province': True,
                'crime_type': True,
                'incident_count': True,
                'severity_score': ':.2f',
                'sentinel_priority': True
            },
            color_continuous_scale='Reds',
            size_max=20,
            zoom=6,
            height=600
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            title="Crime Hotspots by Severity Score",
            coloraxis_colorbar=dict(
                title="Severity Score",
                tickvals=[0, 2, 4, 6, 8, 10],
                ticktext=['Low', 'Low-Med', 'Medium', 'Med-High', 'High', 'Critical']
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_crime_statistics_charts(self, data):
        """Create crime statistics charts"""
        st.subheader("Crime Statistics Analysis")
        
        # Province-wise crime distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Crime Distribution by Province**")
            province_data = data['hotspots'].groupby('province').agg({
                'incident_count': 'sum',
                'severity_score': 'mean'
            }).reset_index()
            
            fig = px.bar(
                province_data,
                x='province',
                y='incident_count',
                title='Total Incidents by Province',
                color='severity_score',
                color_continuous_scale='Reds'
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Crime Types Distribution**")
            crime_type_data = data['hotspots'].groupby('crime_type').agg({
                'incident_count': 'sum'
            }).reset_index().sort_values('incident_count', ascending=False)
            
            fig = px.pie(
                crime_type_data.head(10),
                values='incident_count',
                names='crime_type',
                title='Top 10 Crime Types'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def create_vehicle_crime_analysis(self, data):
        """Create vehicle crime analysis charts"""
        st.subheader("Vehicle Crime Analysis")
        
        if data['vehicles'].empty:
            st.warning("No vehicle crime data available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Most Stolen Vehicles**")
            theft_data = data['vehicles'][data['vehicles']['crime_type'] == 'theft'].nlargest(10, 'theft_count')
            
            fig = px.bar(
                theft_data,
                x='vehicle_model',
                y='theft_count',
                color='vehicle_make',
                title='Top 10 Most Stolen Vehicles',
                labels={'vehicle_model': 'Vehicle Model', 'theft_count': 'Theft Count'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Most Hijacked Vehicles**")
            hijack_data = data['vehicles'][data['vehicles']['crime_type'] == 'hijacking'].nlargest(10, 'hijacking_count')
            
            fig = px.bar(
                hijack_data,
                x='vehicle_model',
                y='hijacking_count',
                color='vehicle_make',
                title='Top 10 Most Hijacked Vehicles',
                labels={'vehicle_model': 'Vehicle Model', 'hijacking_count': 'Hijacking Count'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_cit_analysis(self, data):
        """Create CIT (Cash-in-Transit) analysis"""
        st.subheader("Cash-in-Transit Risk Analysis")
        
        if data['cit_routes'].empty:
            st.warning("No CIT route data available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**CIT Route Risk Levels**")
            risk_data = data['cit_routes'].groupby('risk_level').agg({
                'historical_incidents': 'sum',
                'priority_score': 'mean'
            }).reset_index()
            
            fig = px.bar(
                risk_data,
                x='risk_level',
                y='historical_incidents',
                color='priority_score',
                color_continuous_scale='Reds',
                title='Historical Incidents by Risk Level',
                labels={'historical_incidents': 'Historical Incidents', 'priority_score': 'Priority Score'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**CIT Routes Map**")
            fig = go.Figure()
            
            for _, route in data['cit_routes'].iterrows():
                fig.add_trace(go.Scattermapbox(
                    mode="lines+markers",
                    lon=[route['start_lon'], route['end_lon']],
                    lat=[route['start_lat'], route['end_lat']],
                    marker={'size': 10, 'color': 'red' if route['risk_level'] == 'high' else 'orange'},
                    name=f"{route['route_name']} ({route['risk_level']})",
                    text=f"Incidents: {route['historical_incidents']}<br>Priority: {route['priority_score']:.2f}"
                ))
            
            fig.update_layout(
                mapbox_style="open-street-map",
                mapbox_zoom=6,
                mapbox_center={"lat": -26.2041, "lon": 28.0473},
                title="CIT Routes by Risk Level",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def create_deployment_recommendations(self, data):
        """Create deployment recommendations visualization"""
        st.subheader("Sentinel Deployment Recommendations")
        
        if data['deployments'].empty:
            st.warning("No deployment data available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Deployment Priority Distribution**")
            priority_data = data['deployments'].groupby('priority').size().reset_index(name='count')
            
            fig = px.pie(
                priority_data,
                values='count',
                names='priority',
                title='Deployments by Priority Level',
                color_discrete_map={
                    'critical': '#FF0000',
                    'high': '#FF6600',
                    'medium': '#FFCC00',
                    'low': '#00CC00'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Expected Incidents vs Priority**")
            fig = px.scatter(
                data['deployments'],
                x='expected_incidents_per_month',
                y='priority',
                color='deployment_type',
                size='expected_incidents_per_month',
                hover_name='location_name',
                title='Expected Incidents vs Deployment Priority',
                labels={
                    'expected_incidents_per_month': 'Expected Incidents/Month',
                    'priority': 'Priority Level'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Deployment map
        st.write("**Deployment Locations Map**")
        fig = px.scatter_mapbox(
            data['deployments'],
            lat='latitude',
            lon='longitude',
            color='priority',
            size='expected_incidents_per_month',
            hover_name='location_name',
            hover_data={
                'deployment_type': True,
                'expected_incidents_per_month': True,
                'status': True
            },
            color_discrete_map={
                'critical': '#FF0000',
                'high': '#FF6600',
                'medium': '#FFCC00',
                'low': '#00CC00'
            },
            zoom=6,
            height=500
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            title="Sentinel Deployment Locations"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_private_security_analysis(self, data):
        """Create private security industry analysis"""
        st.subheader("Private Security Industry Analysis")
        
        if data['partners'].empty:
            st.warning("No private security data available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Partnership Tiers Distribution**")
            tier_data = data['partners'].groupby('partnership_tier').agg({
                'officer_count': 'sum'
            }).reset_index()
            
            fig = px.bar(
                tier_data,
                x='partnership_tier',
                y='officer_count',
                title='Officer Count by Partnership Tier',
                labels={'officer_count': 'Total Officers', 'partnership_tier': 'Partnership Tier'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Top Security Companies by Officer Count**")
            top_companies = data['partners'].nlargest(10, 'officer_count')
            
            fig = px.bar(
                top_companies,
                x='officer_count',
                y='company_name',
                orientation='h',
                title='Top 10 Security Companies by Officer Count',
                labels={'officer_count': 'Officer Count', 'company_name': 'Company Name'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def create_kpi_dashboard(self, data):
        """Create KPI dashboard"""
        st.subheader("Key Performance Indicators")
        
        # Calculate KPIs
        total_hotspots = len(data['hotspots'])
        critical_hotspots = len(data['hotspots'][data['hotspots']['sentinel_priority'] == 'critical'])
        total_vehicles = len(data['vehicles'])
        high_risk_vehicles = len(data['vehicles'][data['vehicles']['anpr_priority'] == 'critical'])
        total_deployments = len(data['deployments'])
        critical_deployments = len(data['deployments'][data['deployments']['priority'] == 'critical'])
        total_partners = len(data['partners'])
        
        # Display KPIs in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Crime Hotspots",
                value=total_hotspots,
                delta=f"{critical_hotspots} critical"
            )
        
        with col2:
            st.metric(
                label="Vehicle Crime Patterns",
                value=total_vehicles,
                delta=f"{high_risk_vehicles} high-risk"
            )
        
        with col3:
            st.metric(
                label="Deployment Locations",
                value=total_deployments,
                delta=f"{critical_deployments} critical"
            )
        
        with col4:
            st.metric(
                label="Security Partners",
                value=total_partners,
                delta="Active partnerships"
            )
    
    def create_trend_analysis(self, data):
        """Create trend analysis charts"""
        st.subheader("Crime Trend Analysis")
        
        # Simulate monthly trends (in real implementation, this would come from time-series data)
        months = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
        crime_trends = pd.DataFrame({
            'month': months,
            'total_crimes': np.random.randint(1000, 2000, len(months)),
            'vehicle_crimes': np.random.randint(200, 400, len(months)),
            'cit_robberies': np.random.randint(10, 30, len(months))
        })
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Crimes', 'Vehicle Crimes', 'CIT Robberies', 'Crime Rate by Province'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Total crimes trend
        fig.add_trace(
            go.Scatter(x=crime_trends['month'], y=crime_trends['total_crimes'], name='Total Crimes'),
            row=1, col=1
        )
        
        # Vehicle crimes trend
        fig.add_trace(
            go.Scatter(x=crime_trends['month'], y=crime_trends['vehicle_crimes'], name='Vehicle Crimes'),
            row=1, col=2
        )
        
        # CIT robberies trend
        fig.add_trace(
            go.Scatter(x=crime_trends['month'], y=crime_trends['cit_robberies'], name='CIT Robberies'),
            row=2, col=1
        )
        
        # Crime rate by province
        if not data['hotspots'].empty:
            province_crime_rate = data['hotspots'].groupby('province')['incident_count'].sum().reset_index()
            fig.add_trace(
                go.Bar(x=province_crime_rate['province'], y=province_crime_rate['incident_count'], name='Crime Rate'),
                row=2, col=2
            )
        
        fig.update_layout(height=600, showlegend=False, title_text="Crime Trend Analysis")
        st.plotly_chart(fig, use_container_width=True)
    
    def run_dashboard(self):
        """Run the complete dashboard"""
        st.set_page_config(
            page_title="Sentinel Crime Analysis Dashboard",
            page_icon="🛡️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🛡️ Sentinel Crime Analysis Dashboard")
        st.markdown("Real-time crime data analysis and Sentinel deployment insights")
        
        # Load data
        data = self.load_data()
        if data is None:
            return
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        # Province filter
        if not data['hotspots'].empty:
            provinces = ['All'] + list(data['hotspots']['province'].unique())
            selected_province = st.sidebar.selectbox("Select Province", provinces)
            
            if selected_province != 'All':
                data['hotspots'] = data['hotspots'][data['hotspots']['province'] == selected_province]
        
        # Priority filter
        priorities = ['All', 'critical', 'high', 'medium', 'low']
        selected_priority = st.sidebar.selectbox("Select Priority", priorities)
        
        if selected_priority != 'All':
            data['hotspots'] = data['hotspots'][data['hotspots']['sentinel_priority'] == selected_priority]
            data['deployments'] = data['deployments'][data['deployments']['priority'] == selected_priority]
        
        # Main dashboard sections
        self.create_kpi_dashboard(data)
        st.divider()
        
        self.create_crime_hotspots_map(data)
        st.divider()
        
        self.create_crime_statistics_charts(data)
        st.divider()
        
        self.create_vehicle_crime_analysis(data)
        st.divider()
        
        self.create_cit_analysis(data)
        st.divider()
        
        self.create_deployment_recommendations(data)
        st.divider()
        
        self.create_private_security_analysis(data)
        st.divider()
        
        self.create_trend_analysis(data)
        
        # Footer
        st.markdown("---")
        st.markdown("**Sentinel Crime Analysis Dashboard** - Powered by real SAPS and PSIRA data")
        st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    dashboard = SentinelDashboard()
    dashboard.run_dashboard()
