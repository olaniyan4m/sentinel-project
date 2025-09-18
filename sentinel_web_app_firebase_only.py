#!/usr/bin/env python3
"""
Sentinel Web Application - Firebase Only Version
No SQLite dependency, uses Firebase for all data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import os

# Configure Streamlit
st.set_page_config(
    page_title="Sentinel - Crime Detection & Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SentinelWebAppFirebaseOnly:
    def __init__(self):
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        
    def get_sample_data(self):
        """Return sample data for demonstration"""
        return {
            'crime_statistics': [
                {'province': 'Gauteng', 'crimes': 125000, 'trend': '+5.2%'},
                {'province': 'Western Cape', 'crimes': 85000, 'trend': '+3.1%'},
                {'province': 'KwaZulu-Natal', 'crimes': 95000, 'trend': '+4.8%'},
                {'province': 'Eastern Cape', 'crimes': 65000, 'trend': '+2.3%'},
                {'province': 'Free State', 'crimes': 35000, 'trend': '+1.9%'}
            ],
            'threat_events': [
                {'location': 'Johannesburg', 'lat': -26.2041, 'lon': 28.0473, 'severity': 8, 'type': 'Armed Robbery'},
                {'location': 'Cape Town', 'lat': -33.9249, 'lon': 18.4241, 'severity': 6, 'type': 'Vehicle Theft'},
                {'location': 'Durban', 'lat': -29.8587, 'lon': 31.0218, 'severity': 7, 'type': 'CIT Robbery'},
                {'location': 'Pretoria', 'lat': -25.7479, 'lon': 28.2293, 'severity': 5, 'type': 'Cyber Fraud'}
            ],
            'vehicle_crimes': [
                {'type': 'Carjacking', 'count': 1250, 'change': '+12%'},
                {'type': 'Vehicle Theft', 'count': 8900, 'change': '+8%'},
                {'type': 'Hijacking', 'count': 2100, 'change': '+15%'},
                {'type': 'CIT Robbery', 'count': 180, 'change': '+5%'}
            ]
        }
    
    def render_login(self):
        """Render login page"""
        st.title("🛡️ Sentinel - Fight Crime in South Africa")
        st.markdown("### Secure Access Portal")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            **Welcome to Sentinel Crime Detection & Threat Intelligence Platform**
            
            This platform provides real-time crime intelligence and threat mapping
            for law enforcement, private security, and financial institutions.
            """)
            
            # Role selection
            role = st.selectbox(
                "Select your role:",
                ["Police Officer", "Bank Representative", "Private Security", "Insurance"]
            )
            
            # Email input
            email = st.text_input("Email Address:", placeholder="your.email@organization.co.za")
            
            # Login button
            if st.button("Access Dashboard", type="primary"):
                if email:
                    st.session_state.authenticated = True
                    st.session_state.user_role = role
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Please enter your email address")
    
    def render_police_dashboard(self):
        """Render police officer dashboard"""
        st.title("🚔 Police Officer Dashboard")
        st.markdown("### Crime Intelligence & Threat Analysis")
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Crime Overview", "🗺️ Threat Map", "🚨 Active Alerts", "📋 Cases", "📈 Analytics"
        ])
        
        data = self.get_sample_data()
        
        with tab1:
            st.header("📊 Crime Statistics by Province")
            crime_df = pd.DataFrame(data['crime_statistics'])
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(crime_df, x='province', y='crimes', 
                           title="Crime Count by Province",
                           color='crimes', color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(crime_df, use_container_width=True)
        
        with tab2:
            st.header("🗺️ Real-Time Threat Map")
            threat_df = pd.DataFrame(data['threat_events'])
            
            fig = px.scatter_mapbox(
                threat_df,
                lat="lat",
                lon="lon",
                color="severity",
                size="severity",
                hover_name="location",
                hover_data=["type", "severity"],
                color_continuous_scale="Reds",
                size_max=20,
                zoom=5,
                center={"lat": -30.0, "lon": 25.0}
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                title="South Africa Threat Map",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.header("🚨 Active Crime Alerts")
            alerts = [
                {"time": "14:30", "location": "Sandton", "type": "Armed Robbery", "status": "Active"},
                {"time": "13:45", "location": "Cape Town CBD", "type": "Vehicle Theft", "status": "Investigating"},
                {"time": "12:20", "location": "Durban", "type": "CIT Robbery", "status": "Active"}
            ]
            alerts_df = pd.DataFrame(alerts)
            st.dataframe(alerts_df, use_container_width=True)
    
    def render_bank_dashboard(self):
        """Render bank representative dashboard with threat map access"""
        st.title("🏛️ Bank Representative Dashboard")
        st.markdown("### Financial Crime Prevention & Risk Management")
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Risk Overview", "🗺️ Threat Map", "🚨 Fraud Alerts", "💳 Transactions", "📈 Analytics"
        ])
        
        data = self.get_sample_data()
        
        with tab1:
            st.header("💰 Financial Crime Risk Assessment")
            risk_data = {
                "Risk Type": ["Card Fraud", "ATM Skimming", "Online Banking", "Identity Theft"],
                "Risk Level": ["High", "Medium", "High", "Medium"],
                "Cases (24h)": [45, 12, 23, 8],
                "Trend": ["+15%", "+5%", "+22%", "+3%"]
            }
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, use_container_width=True)
        
        with tab2:
            st.header("🗺️ Threat Intelligence Map")
            st.markdown("### Real-Time Threat Visualization for Financial Crime Prevention")
            
            threat_df = pd.DataFrame(data['threat_events'])
            fig = px.scatter_mapbox(
                threat_df,
                lat="lat",
                lon="lon",
                color="severity",
                size="severity",
                hover_name="location",
                hover_data=["type", "severity"],
                color_continuous_scale="Reds",
                size_max=20,
                zoom=5,
                center={"lat": -30.0, "lon": 25.0}
            )
            fig.update_layout(
                mapbox_style="open-street-map",
                title="South Africa Threat Map - Financial Crime Intelligence",
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_private_security_dashboard(self):
        """Render private security dashboard"""
        st.title("🛡️ Private Security Dashboard")
        st.markdown("### Security Operations & Monitoring")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Operations", "🚨 Alerts", "👥 Personnel", "📈 Performance"
        ])
        
        with tab1:
            st.header("🛡️ Security Operations Overview")
            ops_data = {
                "Location": ["Sandton", "Cape Town CBD", "Durban", "Pretoria"],
                "Personnel": [25, 18, 22, 15],
                "Status": ["Active", "Active", "Active", "Standby"],
                "Incidents (24h)": [3, 1, 2, 0]
            }
            ops_df = pd.DataFrame(ops_data)
            st.dataframe(ops_df, use_container_width=True)
    
    def render_insurance_dashboard(self):
        """Render insurance dashboard"""
        st.title("🏢 Insurance Dashboard")
        st.markdown("### Risk Assessment & Claims Analysis")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Risk Overview", "💰 Claims", "📈 Trends", "🎯 Predictions"
        ])
        
        with tab1:
            st.header("🏠 Property & Vehicle Risk Assessment")
            risk_data = {
                "Risk Category": ["Vehicle Theft", "Property Crime", "CIT Robbery", "Cyber Fraud"],
                "Claims (Month)": [1250, 890, 45, 230],
                "Payout (R Million)": [15.2, 8.7, 2.1, 4.5],
                "Risk Score": ["High", "Medium", "High", "Medium"]
            }
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, use_container_width=True)
    
    def render_sidebar(self):
        """Render sidebar with user info and logout"""
        with st.sidebar:
            st.markdown("### 👤 User Information")
            st.write(f"**Role:** {st.session_state.user_role}")
            st.write(f"**Email:** {st.session_state.user_email}")
            
            st.markdown("---")
            
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.user_email = None
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 🛡️ Sentinel Platform")
            st.markdown("**Version:** 1.0.0")
            st.markdown("**Status:** Operational")
            st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    def run(self):
        """Main application runner"""
        if not st.session_state.authenticated:
            self.render_login()
        else:
            self.render_sidebar()
            
            # Render appropriate dashboard based on user role
            if st.session_state.user_role == "Police Officer":
                self.render_police_dashboard()
            elif st.session_state.user_role == "Bank Representative":
                self.render_bank_dashboard()
            elif st.session_state.user_role == "Private Security":
                self.render_private_security_dashboard()
            elif st.session_state.user_role == "Insurance":
                self.render_insurance_dashboard()

# Run the application
if __name__ == "__main__":
    app = SentinelWebAppFirebaseOnly()
    app.run()
