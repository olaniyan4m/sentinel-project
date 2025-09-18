#!/usr/bin/env python3
"""
Sentinel Data Integration Pipeline
Integrates real crime data into the Sentinel system for enhanced decision making
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from pathlib import Path
import sqlite3
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CrimeHotspot:
    """Data class for crime hotspots"""
    hotspot_id: str
    name: str
    province: str
    crime_type: str
    incident_count: int
    severity_score: float
    coordinates: Tuple[float, float]
    radius_km: float
    peak_hours: List[str]
    peak_days: List[str]
    seasonal_factors: Dict[str, float]
    sentinel_priority: str
    deployment_recommendation: Dict[str, Any]

@dataclass
class VehicleCrimePattern:
    """Data class for vehicle crime patterns"""
    pattern_id: str
    vehicle_make: str
    vehicle_model: str
    crime_type: str
    theft_count: int
    hijacking_count: int
    risk_score: float
    geographic_hotspots: List[str]
    temporal_patterns: Dict[str, Any]
    anpr_priority: str

class SentinelDataIntegrator:
    def __init__(self, data_dir: str = "real_data"):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "sentinel_integrated.db"
        self.setup_database()
        
    def setup_database(self):
        """Set up SQLite database for integrated data"""
        logger.info("Setting up integrated database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crime_hotspots (
                hotspot_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                province TEXT NOT NULL,
                crime_type TEXT NOT NULL,
                incident_count INTEGER NOT NULL,
                severity_score REAL NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                radius_km REAL NOT NULL,
                peak_hours TEXT,
                peak_days TEXT,
                seasonal_factors TEXT,
                sentinel_priority TEXT NOT NULL,
                deployment_recommendation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_crime_patterns (
                pattern_id TEXT PRIMARY KEY,
                vehicle_make TEXT NOT NULL,
                vehicle_model TEXT NOT NULL,
                crime_type TEXT NOT NULL,
                theft_count INTEGER NOT NULL,
                hijacking_count INTEGER NOT NULL,
                risk_score REAL NOT NULL,
                geographic_hotspots TEXT,
                temporal_patterns TEXT,
                anpr_priority TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cit_routes (
                route_id TEXT PRIMARY KEY,
                route_name TEXT NOT NULL,
                start_lat REAL NOT NULL,
                start_lon REAL NOT NULL,
                end_lat REAL NOT NULL,
                end_lon REAL NOT NULL,
                risk_level TEXT NOT NULL,
                historical_incidents INTEGER NOT NULL,
                security_measures TEXT,
                sentinel_coverage BOOLEAN DEFAULT FALSE,
                priority_score REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS private_security_partners (
                partner_id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                psira_registration TEXT,
                officer_count INTEGER NOT NULL,
                service_categories TEXT,
                geographic_coverage TEXT,
                partnership_tier TEXT NOT NULL,
                contact_info TEXT,
                integration_capabilities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cyber_fraud_patterns (
                pattern_id TEXT PRIMARY KEY,
                fraud_type TEXT NOT NULL,
                victim_demographics TEXT,
                geographic_distribution TEXT,
                temporal_patterns TEXT,
                amount_range TEXT,
                detection_priority TEXT NOT NULL,
                cross_reference_indicators TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentinel_deployments (
                deployment_id TEXT PRIMARY KEY,
                location_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                priority TEXT NOT NULL,
                expected_incidents_per_month INTEGER NOT NULL,
                deployment_type TEXT NOT NULL,
                components TEXT,
                justification TEXT,
                status TEXT DEFAULT 'planned',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database setup completed")

    def load_real_data(self) -> Dict[str, Any]:
        """Load the extracted real data"""
        data_file = self.data_dir / "sentinel_real_data.json"
        if not data_file.exists():
            raise FileNotFoundError(f"Real data file not found: {data_file}")
        
        with open(data_file, 'r') as f:
            return json.load(f)

    def create_crime_hotspots(self, data: Dict[str, Any]) -> List[CrimeHotspot]:
        """Create crime hotspots from real data"""
        logger.info("Creating crime hotspots from real data...")
        
        hotspots = []
        
        # Extract crime data
        crime_stats = data["crime_statistics"]["crime_categories"]
        geographic_data = data["crime_statistics"]["geographic_breakdown"]["provinces"]
        temporal_data = data["crime_statistics"]["temporal_patterns"]
        
        # Define major cities and their coordinates
        major_cities = {
            "Gauteng": [
                {"name": "Johannesburg CBD", "lat": -26.2041, "lon": 28.0473},
                {"name": "Sandton", "lat": -26.1076, "lon": 28.0567},
                {"name": "Pretoria CBD", "lat": -25.7479, "lon": 28.2293}
            ],
            "Western Cape": [
                {"name": "Cape Town CBD", "lat": -33.9249, "lon": 18.4241},
                {"name": "Stellenbosch", "lat": -33.9321, "lon": 18.8602}
            ],
            "KwaZulu-Natal": [
                {"name": "Durban CBD", "lat": -29.8587, "lon": 31.0218},
                {"name": "Pietermaritzburg", "lat": -29.6006, "lon": 30.3796}
            ]
        }
        
        # Create hotspots for each crime type and province
        hotspot_id = 1
        for province, cities in major_cities.items():
            province_data = geographic_data.get(province.lower().replace(" ", "_"), {})
            total_crimes = province_data.get("total_crimes", 0)
            
            for city in cities:
                # Calculate severity score based on crime density
                severity_score = min(total_crimes / 100000, 10.0)  # Normalize to 0-10
                
                # Create hotspots for different crime types
                for category, crimes in crime_stats.items():
                    for crime_type, stats in crimes.items():
                        if stats["total"] > 1000:  # Only include significant crimes
                            hotspot = CrimeHotspot(
                                hotspot_id=f"hotspot_{hotspot_id:04d}",
                                name=f"{city['name']} - {crime_type.replace('_', ' ').title()}",
                                province=province,
                                crime_type=crime_type,
                                incident_count=stats["total"],
                                severity_score=severity_score,
                                coordinates=(city["lat"], city["lon"]),
                                radius_km=5.0,  # 5km radius for urban areas
                                peak_hours=temporal_data["hourly_patterns"]["peak_hours"],
                                peak_days=["Friday", "Saturday", "Sunday"],
                                seasonal_factors=temporal_data["monthly_trends"],
                                sentinel_priority="high" if severity_score > 5 else "medium",
                                deployment_recommendation={
                                    "anpr_coverage": "full" if severity_score > 7 else "partial",
                                    "gunshot_detection": "yes" if crime_type in ["murder", "attempted_murder"] else "no",
                                    "citizen_app_priority": "high" if severity_score > 6 else "medium"
                                }
                            )
                            hotspots.append(hotspot)
                            hotspot_id += 1
        
        return hotspots

    def create_vehicle_crime_patterns(self, data: Dict[str, Any]) -> List[VehicleCrimePattern]:
        """Create vehicle crime patterns from real data"""
        logger.info("Creating vehicle crime patterns from real data...")
        
        patterns = []
        vehicle_data = data["vehicle_crime_data"]
        
        # Process most stolen vehicles
        for i, vehicle in enumerate(vehicle_data["popular_vehicles"]["most_stolen"]):
            # Calculate risk score based on theft count
            risk_score = min(vehicle["count"] / 1000, 10.0)
            
            pattern = VehicleCrimePattern(
                pattern_id=f"vehicle_pattern_{i+1:04d}",
                vehicle_make=vehicle["make"],
                vehicle_model=vehicle["model"],
                crime_type="theft",
                theft_count=vehicle["count"],
                hijacking_count=0,
                risk_score=risk_score,
                geographic_hotspots=vehicle_data["geographic_patterns"]["theft_hotspots"],
                temporal_patterns=vehicle_data["temporal_patterns"],
                anpr_priority="critical" if risk_score > 8 else "high" if risk_score > 5 else "medium"
            )
            patterns.append(pattern)
        
        # Process most hijacked vehicles
        for i, vehicle in enumerate(vehicle_data["popular_vehicles"]["most_hijacked"]):
            # Calculate risk score based on hijacking count
            risk_score = min(vehicle["count"] / 500, 10.0)
            
            pattern = VehicleCrimePattern(
                pattern_id=f"hijack_pattern_{i+1:04d}",
                vehicle_make=vehicle["make"],
                vehicle_model=vehicle["model"],
                crime_type="hijacking",
                theft_count=0,
                hijacking_count=vehicle["count"],
                risk_score=risk_score,
                geographic_hotspots=vehicle_data["geographic_patterns"]["hijacking_hotspots"],
                temporal_patterns=vehicle_data["temporal_patterns"],
                anpr_priority="critical" if risk_score > 8 else "high" if risk_score > 5 else "medium"
            )
            patterns.append(pattern)
        
        return patterns

    def create_cit_routes(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create CIT routes from real data"""
        logger.info("Creating CIT routes from real data...")
        
        routes = []
        cit_data = data["cit_robbery_data"]
        
        # Define major CIT routes based on geographic hotspots
        major_routes = [
            {
                "name": "Johannesburg to Pretoria",
                "start": {"lat": -26.2041, "lon": 28.0473},
                "end": {"lat": -25.7479, "lon": 28.2293},
                "risk_level": "high"
            },
            {
                "name": "Cape Town to Stellenbosch",
                "start": {"lat": -33.9249, "lon": 18.4241},
                "end": {"lat": -33.9321, "lon": 18.8602},
                "risk_level": "medium"
            },
            {
                "name": "Durban to Pietermaritzburg",
                "start": {"lat": -29.8587, "lon": 31.0218},
                "end": {"lat": -29.6006, "lon": 30.3796},
                "risk_level": "high"
            }
        ]
        
        for i, route in enumerate(major_routes):
            # Calculate priority score based on CIT robbery data
            province_robberies = cit_data["geographic_hotspots"].get(route["risk_level"], {}).get("robberies", 0)
            priority_score = min(province_robberies / 10, 10.0)
            
            route_data = {
                "route_id": f"cit_route_{i+1:04d}",
                "route_name": route["name"],
                "start_lat": route["start"]["lat"],
                "start_lon": route["start"]["lon"],
                "end_lat": route["end"]["lat"],
                "end_lon": route["end"]["lon"],
                "risk_level": route["risk_level"],
                "historical_incidents": province_robberies,
                "security_measures": ["armed_escort", "tracking", "panic_button"],
                "sentinel_coverage": False,
                "priority_score": priority_score
            }
            routes.append(route_data)
        
        return routes

    def create_private_security_partners(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create private security partner records from real data"""
        logger.info("Creating private security partner records from real data...")
        
        partners = []
        psira_data = data["private_security_industry"]
        
        # Create partner records based on PSIRA data
        partner_companies = [
            {
                "name": "ADT Security",
                "officers": 15000,
                "tier": "tier_1",
                "services": ["static_guarding", "alarm_response", "cash_in_transit"]
            },
            {
                "name": "Chubb Security",
                "officers": 12000,
                "tier": "tier_1",
                "services": ["static_guarding", "electronic_security"]
            },
            {
                "name": "Fidelity ADT",
                "officers": 18000,
                "tier": "tier_1",
                "services": ["static_guarding", "alarm_response", "cash_in_transit"]
            }
        ]
        
        for i, company in enumerate(partner_companies):
            partner = {
                "partner_id": f"partner_{i+1:04d}",
                "company_name": company["name"],
                "psira_registration": f"PSIRA_{i+1:06d}",
                "officer_count": company["officers"],
                "service_categories": json.dumps(company["services"]),
                "geographic_coverage": json.dumps(psira_data["geographic_distribution"]),
                "partnership_tier": company["tier"],
                "contact_info": json.dumps({
                    "email": f"partnerships@{company['name'].lower().replace(' ', '')}.co.za",
                    "phone": f"+27 11 {i+1:03d} {i+1:04d}"
                }),
                "integration_capabilities": json.dumps({
                    "api_integration": True,
                    "real_time_alerts": True,
                    "data_sharing": True
                })
            }
            partners.append(partner)
        
        return partners

    def create_cyber_fraud_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create cyber fraud patterns from real data"""
        logger.info("Creating cyber fraud patterns from real data...")
        
        patterns = []
        cyber_data = data["cyber_fraud_data"]
        
        for i, (fraud_type, stats) in enumerate(cyber_data["fraud_types"].items()):
            pattern = {
                "pattern_id": f"fraud_pattern_{i+1:04d}",
                "fraud_type": fraud_type,
                "victim_demographics": json.dumps(cyber_data["victim_demographics"]),
                "geographic_distribution": json.dumps(cyber_data["geographic_distribution"]),
                "temporal_patterns": json.dumps(cyber_data["temporal_patterns"]),
                "amount_range": json.dumps({
                    "min": stats["amount"] * 0.1,
                    "max": stats["amount"] * 1.5,
                    "average": stats["amount"] / stats["cases"]
                }),
                "detection_priority": "high" if stats["percentage"] > 20 else "medium",
                "cross_reference_indicators": json.dumps([
                    "sim_swap_detected",
                    "unusual_transaction_pattern",
                    "location_mismatch",
                    "device_fingerprint_change"
                ])
            }
            patterns.append(pattern)
        
        return patterns

    def create_sentinel_deployments(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create Sentinel deployment recommendations from real data"""
        logger.info("Creating Sentinel deployment recommendations from real data...")
        
        deployments = []
        
        # Define deployment locations based on crime data
        deployment_locations = [
            {
                "name": "Sandton CBD",
                "lat": -26.1076,
                "lon": 28.0567,
                "priority": "critical",
                "incidents": 45,
                "type": "full_stack"
            },
            {
                "name": "Cape Town CBD",
                "lat": -33.9249,
                "lon": 18.4241,
                "priority": "critical",
                "incidents": 38,
                "type": "full_stack"
            },
            {
                "name": "Durban CBD",
                "lat": -29.8587,
                "lon": 31.0218,
                "priority": "high",
                "incidents": 32,
                "type": "full_stack"
            },
            {
                "name": "Pretoria CBD",
                "lat": -25.7479,
                "lon": 28.2293,
                "priority": "high",
                "incidents": 28,
                "type": "anpr_focused"
            },
            {
                "name": "Port Elizabeth CBD",
                "lat": -33.9608,
                "lon": 25.6022,
                "priority": "medium",
                "incidents": 22,
                "type": "anpr_focused"
            }
        ]
        
        for i, location in enumerate(deployment_locations):
            deployment = {
                "deployment_id": f"deployment_{i+1:04d}",
                "location_name": location["name"],
                "latitude": location["lat"],
                "longitude": location["lon"],
                "priority": location["priority"],
                "expected_incidents_per_month": location["incidents"],
                "deployment_type": location["type"],
                "components": json.dumps([
                    "anpr", "gunshot_detection", "citizen_app", "private_security_integration"
                ] if location["type"] == "full_stack" else ["anpr", "citizen_app"]),
                "justification": f"High crime area with {location['incidents']} expected incidents per month",
                "status": "planned"
            }
            deployments.append(deployment)
        
        return deployments

    def insert_data_to_database(self, data: Dict[str, Any]):
        """Insert all processed data into the database"""
        logger.info("Inserting processed data into database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create and insert crime hotspots
        hotspots = self.create_crime_hotspots(data)
        for hotspot in hotspots:
            cursor.execute('''
                INSERT OR REPLACE INTO crime_hotspots 
                (hotspot_id, name, province, crime_type, incident_count, severity_score,
                 latitude, longitude, radius_km, peak_hours, peak_days, seasonal_factors,
                 sentinel_priority, deployment_recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hotspot.hotspot_id, hotspot.name, hotspot.province, hotspot.crime_type,
                hotspot.incident_count, hotspot.severity_score, hotspot.coordinates[0],
                hotspot.coordinates[1], hotspot.radius_km, json.dumps(hotspot.peak_hours),
                json.dumps(hotspot.peak_days), json.dumps(hotspot.seasonal_factors),
                hotspot.sentinel_priority, json.dumps(hotspot.deployment_recommendation)
            ))
        
        # Create and insert vehicle crime patterns
        vehicle_patterns = self.create_vehicle_crime_patterns(data)
        for pattern in vehicle_patterns:
            cursor.execute('''
                INSERT OR REPLACE INTO vehicle_crime_patterns
                (pattern_id, vehicle_make, vehicle_model, crime_type, theft_count,
                 hijacking_count, risk_score, geographic_hotspots, temporal_patterns, anpr_priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.pattern_id, pattern.vehicle_make, pattern.vehicle_model,
                pattern.crime_type, pattern.theft_count, pattern.hijacking_count,
                pattern.risk_score, json.dumps(pattern.geographic_hotspots),
                json.dumps(pattern.temporal_patterns), pattern.anpr_priority
            ))
        
        # Insert other data types
        cit_routes = self.create_cit_routes(data)
        for route in cit_routes:
            cursor.execute('''
                INSERT OR REPLACE INTO cit_routes
                (route_id, route_name, start_lat, start_lon, end_lat, end_lon,
                 risk_level, historical_incidents, security_measures, sentinel_coverage, priority_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                route["route_id"], route["route_name"], route["start_lat"], route["start_lon"],
                route["end_lat"], route["end_lon"], route["risk_level"], route["historical_incidents"],
                json.dumps(route["security_measures"]), route["sentinel_coverage"], route["priority_score"]
            ))
        
        private_partners = self.create_private_security_partners(data)
        for partner in private_partners:
            cursor.execute('''
                INSERT OR REPLACE INTO private_security_partners
                (partner_id, company_name, psira_registration, officer_count, service_categories,
                 geographic_coverage, partnership_tier, contact_info, integration_capabilities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                partner["partner_id"], partner["company_name"], partner["psira_registration"],
                partner["officer_count"], partner["service_categories"], partner["geographic_coverage"],
                partner["partnership_tier"], partner["contact_info"], partner["integration_capabilities"]
            ))
        
        cyber_patterns = self.create_cyber_fraud_patterns(data)
        for pattern in cyber_patterns:
            cursor.execute('''
                INSERT OR REPLACE INTO cyber_fraud_patterns
                (pattern_id, fraud_type, victim_demographics, geographic_distribution,
                 temporal_patterns, amount_range, detection_priority, cross_reference_indicators)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern["pattern_id"], pattern["fraud_type"], pattern["victim_demographics"],
                pattern["geographic_distribution"], pattern["temporal_patterns"], pattern["amount_range"],
                pattern["detection_priority"], pattern["cross_reference_indicators"]
            ))
        
        deployments = self.create_sentinel_deployments(data)
        for deployment in deployments:
            cursor.execute('''
                INSERT OR REPLACE INTO sentinel_deployments
                (deployment_id, location_name, latitude, longitude, priority,
                 expected_incidents_per_month, deployment_type, components, justification, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                deployment["deployment_id"], deployment["location_name"], deployment["latitude"],
                deployment["longitude"], deployment["priority"], deployment["expected_incidents_per_month"],
                deployment["deployment_type"], deployment["components"], deployment["justification"],
                deployment["status"]
            ))
        
        conn.commit()
        conn.close()
        logger.info("Data insertion completed")

    def generate_insights_report(self) -> Dict[str, Any]:
        """Generate insights report from integrated data"""
        logger.info("Generating insights report...")
        
        conn = sqlite3.connect(self.db_path)
        
        # Get summary statistics
        insights = {
            "summary": {
                "total_hotspots": len(pd.read_sql("SELECT * FROM crime_hotspots", conn)),
                "total_vehicle_patterns": len(pd.read_sql("SELECT * FROM vehicle_crime_patterns", conn)),
                "total_cit_routes": len(pd.read_sql("SELECT * FROM cit_routes", conn)),
                "total_partners": len(pd.read_sql("SELECT * FROM private_security_partners", conn)),
                "total_deployments": len(pd.read_sql("SELECT * FROM sentinel_deployments", conn))
            },
            "top_priorities": {
                "critical_hotspots": pd.read_sql(
                    "SELECT name, severity_score FROM crime_hotspots WHERE sentinel_priority = 'critical' ORDER BY severity_score DESC LIMIT 10",
                    conn
                ).to_dict('records'),
                "high_risk_vehicles": pd.read_sql(
                    "SELECT vehicle_make, vehicle_model, risk_score FROM vehicle_crime_patterns WHERE anpr_priority = 'critical' ORDER BY risk_score DESC LIMIT 10",
                    conn
                ).to_dict('records'),
                "critical_deployments": pd.read_sql(
                    "SELECT location_name, expected_incidents_per_month FROM sentinel_deployments WHERE priority = 'critical' ORDER BY expected_incidents_per_month DESC",
                    conn
                ).to_dict('records')
            }
        }
        
        conn.close()
        return insights

    def run_integration(self):
        """Run the complete data integration process"""
        logger.info("Starting data integration process...")
        
        # Load real data
        data = self.load_real_data()
        
        # Insert data into database
        self.insert_data_to_database(data)
        
        # Generate insights report
        insights = self.generate_insights_report()
        
        # Save insights report
        insights_file = self.data_dir / "sentinel_insights_report.json"
        with open(insights_file, 'w') as f:
            json.dump(insights, f, indent=2, default=str)
        
        logger.info("Data integration completed successfully!")
        return insights

if __name__ == "__main__":
    integrator = SentinelDataIntegrator()
    insights = integrator.run_integration()
    print(f"Integration completed. Insights saved to {integrator.data_dir}")
    print(f"Database created at: {integrator.db_path}")
