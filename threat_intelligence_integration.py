#!/usr/bin/env python3
"""
Sentinel Threat Intelligence Integration
Integrates cyber threat intelligence with physical crime data for comprehensive threat analysis
"""

import json
import sqlite3
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from pathlib import Path
import hashlib
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentinelThreatIntelligence:
    def __init__(self, data_dir: str = "real_data"):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "sentinel_integrated.db"
        
        # Threat intelligence API endpoints (from threats_package)
        self.threat_apis = {
            "abuseipdb": "https://api.abuseipdb.com/api/v2",
            "shodan": "https://api.shodan.io/shodan",
            "ipapi": "https://ipapi.co",
            "virustotal": "https://www.virustotal.com/api/v3"
        }
        
        # South African IP ranges (major ISPs and organizations)
        self.sa_ip_ranges = [
            "41.0.0.0/8", "102.0.0.0/8", "105.0.0.0/8", "196.0.0.0/8",
            "197.0.0.0/8", "198.0.0.0/8", "200.0.0.0/8", "201.0.0.0/8"
        ]
        
        # Cyber-physical crime correlation patterns
        self.cyber_physical_patterns = {
            "sim_swap_fraud": {
                "physical_indicators": ["phone_theft", "identity_theft", "card_fraud"],
                "cyber_indicators": ["sim_swap", "account_takeover", "unauthorized_transactions"],
                "correlation_weight": 0.8
            },
            "card_fraud": {
                "physical_indicators": ["card_theft", "atm_skimming", "pos_fraud"],
                "cyber_indicators": ["card_not_present", "online_fraud", "data_breach"],
                "correlation_weight": 0.7
            },
            "identity_theft": {
                "physical_indicators": ["document_theft", "mail_theft", "dumpster_diving"],
                "cyber_indicators": ["phishing", "social_engineering", "data_breach"],
                "correlation_weight": 0.6
            }
        }

    def setup_threat_database(self):
        """Set up threat intelligence database tables"""
        logger.info("Setting up threat intelligence database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Threat intelligence tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_events (
                event_id TEXT PRIMARY KEY,
                ip_address TEXT NOT NULL,
                threat_type TEXT NOT NULL,
                severity_score REAL NOT NULL,
                confidence_score REAL NOT NULL,
                source TEXT NOT NULL,
                country_code TEXT,
                latitude REAL,
                longitude REAL,
                city TEXT,
                region TEXT,
                isp TEXT,
                asn TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                report_count INTEGER DEFAULT 0,
                categories TEXT,
                raw_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ip_enrichment_cache (
                ip_address TEXT PRIMARY KEY,
                geo_data TEXT,
                abuse_data TEXT,
                shodan_data TEXT,
                virustotal_data TEXT,
                threat_score REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cache_expiry TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cyber_physical_correlations (
                correlation_id TEXT PRIMARY KEY,
                cyber_event_id TEXT,
                physical_event_id TEXT,
                correlation_type TEXT,
                correlation_score REAL,
                evidence_links TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cyber_event_id) REFERENCES threat_events (event_id),
                FOREIGN KEY (physical_event_id) REFERENCES evidence (evidence_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_intelligence_feeds (
                feed_id TEXT PRIMARY KEY,
                feed_name TEXT NOT NULL,
                feed_type TEXT NOT NULL,
                last_updated TIMESTAMP,
                record_count INTEGER,
                status TEXT DEFAULT 'active',
                configuration TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_indicators (
                indicator_id TEXT PRIMARY KEY,
                indicator_type TEXT NOT NULL,
                indicator_value TEXT NOT NULL,
                threat_type TEXT,
                severity_score REAL,
                confidence_score REAL,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                source TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Threat intelligence database setup completed")

    def enrich_ip_address(self, ip_address: str, api_keys: Dict[str, str]) -> Dict[str, Any]:
        """Enrich IP address with threat intelligence data"""
        logger.info(f"Enriching IP address: {ip_address}")
        
        # Check cache first
        cached_data = self.get_cached_ip_data(ip_address)
        if cached_data and not self.is_cache_expired(cached_data):
            return cached_data
        
        enrichment_data = {
            "ip_address": ip_address,
            "geo_data": {},
            "abuse_data": {},
            "shodan_data": {},
            "virustotal_data": {},
            "threat_score": 0.0,
            "enrichment_timestamp": datetime.now().isoformat()
        }
        
        # Geographic data
        try:
            geo_response = requests.get(f"{self.threat_apis['ipapi']}/{ip_address}/json/", timeout=10)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                enrichment_data["geo_data"] = {
                    "latitude": geo_data.get("latitude"),
                    "longitude": geo_data.get("longitude"),
                    "city": geo_data.get("city"),
                    "region": geo_data.get("region"),
                    "country": geo_data.get("country_name"),
                    "country_code": geo_data.get("country"),
                    "isp": geo_data.get("org"),
                    "asn": geo_data.get("asn")
                }
        except Exception as e:
            logger.warning(f"Failed to get geo data for {ip_address}: {e}")
        
        # AbuseIPDB data
        if api_keys.get("abuseipdb_key"):
            try:
                abuse_response = requests.get(
                    f"{self.threat_apis['abuseipdb']}/check",
                    params={"ipAddress": ip_address, "maxAgeInDays": 90},
                    headers={"Key": api_keys["abuseipdb_key"], "Accept": "application/json"},
                    timeout=10
                )
                if abuse_response.status_code == 200:
                    abuse_data = abuse_response.json()
                    if abuse_data.get("data"):
                        d = abuse_data["data"]
                        enrichment_data["abuse_data"] = {
                            "abuse_confidence_score": d.get("abuseConfidenceScore", 0),
                            "total_reports": d.get("totalReports", 0),
                            "last_reported_at": d.get("lastReportedAt"),
                            "country_code": d.get("countryCode"),
                            "usage_type": d.get("usageType"),
                            "is_public": d.get("isPublic", False),
                            "is_whitelisted": d.get("isWhitelisted", False)
                        }
            except Exception as e:
                logger.warning(f"Failed to get AbuseIPDB data for {ip_address}: {e}")
        
        # Shodan data
        if api_keys.get("shodan_key"):
            try:
                shodan_response = requests.get(
                    f"{self.threat_apis['shodan']}/host/{ip_address}",
                    params={"key": api_keys["shodan_key"]},
                    timeout=10
                )
                if shodan_response.status_code == 200:
                    shodan_data = shodan_response.json()
                    enrichment_data["shodan_data"] = {
                        "ports": shodan_data.get("ports", []),
                        "organization": shodan_data.get("org"),
                        "hostnames": shodan_data.get("hostnames", []),
                        "vulnerabilities": list(shodan_data.get("vulns", {}).keys()),
                        "vulnerability_count": len(shodan_data.get("vulns", {})),
                        "services": shodan_data.get("data", [])
                    }
            except Exception as e:
                logger.warning(f"Failed to get Shodan data for {ip_address}: {e}")
        
        # Calculate threat score
        enrichment_data["threat_score"] = self.calculate_threat_score(enrichment_data)
        
        # Cache the results
        self.cache_ip_data(ip_address, enrichment_data)
        
        return enrichment_data

    def calculate_threat_score(self, enrichment_data: Dict[str, Any]) -> float:
        """Calculate comprehensive threat score for IP address"""
        score = 0.0
        
        # AbuseIPDB score (0-100, weight 0.6)
        abuse_score = enrichment_data.get("abuse_data", {}).get("abuse_confidence_score", 0)
        score += (abuse_score / 100) * 0.6
        
        # Shodan vulnerability score (0-4, weight 0.3)
        vuln_count = enrichment_data.get("shodan_data", {}).get("vulnerability_count", 0)
        vuln_score = min(vuln_count / 20, 1.0) * 4  # Normalize to 0-4 scale
        score += (vuln_score / 4) * 0.3
        
        # Geographic risk (South African IPs get lower base risk, weight 0.1)
        country_code = enrichment_data.get("geo_data", {}).get("country_code", "")
        if country_code == "ZA":
            score += 0.05  # Lower risk for South African IPs
        else:
            score += 0.1   # Higher risk for foreign IPs
        
        return min(score, 1.0)  # Cap at 1.0

    def get_cached_ip_data(self, ip_address: str) -> Dict[str, Any]:
        """Get cached IP enrichment data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM ip_enrichment_cache WHERE ip_address = ?",
            (ip_address,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "ip_address": row[0],
                "geo_data": json.loads(row[1]) if row[1] else {},
                "abuse_data": json.loads(row[2]) if row[2] else {},
                "shodan_data": json.loads(row[3]) if row[3] else {},
                "virustotal_data": json.loads(row[4]) if row[4] else {},
                "threat_score": row[5],
                "last_updated": row[6],
                "cache_expiry": row[7]
            }
        
        return None

    def cache_ip_data(self, ip_address: str, data: Dict[str, Any]):
        """Cache IP enrichment data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cache_expiry = datetime.now() + timedelta(hours=24)  # 24-hour cache
        
        cursor.execute('''
            INSERT OR REPLACE INTO ip_enrichment_cache
            (ip_address, geo_data, abuse_data, shodan_data, virustotal_data, threat_score, last_updated, cache_expiry)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ip_address,
            json.dumps(data.get("geo_data", {})),
            json.dumps(data.get("abuse_data", {})),
            json.dumps(data.get("shodan_data", {})),
            json.dumps(data.get("virustotal_data", {})),
            data.get("threat_score", 0.0),
            datetime.now().isoformat(),
            cache_expiry.isoformat()
        ))
        
        conn.commit()
        conn.close()

    def is_cache_expired(self, cached_data: Dict[str, Any]) -> bool:
        """Check if cached data is expired"""
        if not cached_data.get("cache_expiry"):
            return True
        
        expiry_time = datetime.fromisoformat(cached_data["cache_expiry"])
        return datetime.now() > expiry_time

    def ingest_threat_feed(self, feed_data: List[Dict[str, Any]], source: str):
        """Ingest threat intelligence feed data"""
        logger.info(f"Ingesting {len(feed_data)} threat events from {source}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for event in feed_data:
            event_id = hashlib.md5(f"{event.get('ip', '')}-{event.get('timestamp', '')}".encode()).hexdigest()
            
            cursor.execute('''
                INSERT OR REPLACE INTO threat_events
                (event_id, ip_address, threat_type, severity_score, confidence_score, source,
                 country_code, latitude, longitude, city, region, isp, asn,
                 first_seen, last_seen, report_count, categories, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_id,
                event.get("ip", ""),
                event.get("threat_type", "unknown"),
                event.get("severity_score", 0.0),
                event.get("confidence_score", 0.0),
                source,
                event.get("country_code", ""),
                event.get("latitude"),
                event.get("longitude"),
                event.get("city", ""),
                event.get("region", ""),
                event.get("isp", ""),
                event.get("asn", ""),
                event.get("first_seen", datetime.now().isoformat()),
                event.get("last_seen", datetime.now().isoformat()),
                event.get("report_count", 0),
                json.dumps(event.get("categories", [])),
                json.dumps(event)
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Successfully ingested {len(feed_data)} threat events")

    def correlate_cyber_physical_threats(self) -> List[Dict[str, Any]]:
        """Correlate cyber threats with physical crime data"""
        logger.info("Correlating cyber and physical threats...")
        
        conn = sqlite3.connect(self.db_path)
        
        # Get recent cyber threats
        cyber_threats = pd.read_sql('''
            SELECT * FROM threat_events 
            WHERE created_at >= datetime('now', '-7 days')
            AND country_code = 'ZA'
            ORDER BY severity_score DESC
        ''', conn)
        
        # Get recent physical evidence
        physical_evidence = pd.read_sql('''
            SELECT * FROM evidence 
            WHERE created_at >= datetime('now', '-7 days')
            AND location IS NOT NULL
        ''', conn)
        
        correlations = []
        
        for _, cyber_threat in cyber_threats.iterrows():
            for _, physical_event in physical_evidence.iterrows():
                correlation_score = self.calculate_correlation_score(cyber_threat, physical_event)
                
                if correlation_score > 0.5:  # Threshold for significant correlation
                    correlation_id = hashlib.md5(
                        f"{cyber_threat['event_id']}-{physical_event['evidence_id']}".encode()
                    ).hexdigest()
                    
                    correlation = {
                        "correlation_id": correlation_id,
                        "cyber_event_id": cyber_threat["event_id"],
                        "physical_event_id": physical_event["evidence_id"],
                        "correlation_type": self.determine_correlation_type(cyber_threat, physical_event),
                        "correlation_score": correlation_score,
                        "evidence_links": self.generate_evidence_links(cyber_threat, physical_event),
                        "created_at": datetime.now().isoformat()
                    }
                    
                    correlations.append(correlation)
        
        # Store correlations in database
        if correlations:
            correlation_df = pd.DataFrame(correlations)
            correlation_df.to_sql('cyber_physical_correlations', conn, if_exists='append', index=False)
        
        conn.close()
        logger.info(f"Found {len(correlations)} cyber-physical correlations")
        return correlations

    def calculate_correlation_score(self, cyber_threat: pd.Series, physical_event: pd.Series) -> float:
        """Calculate correlation score between cyber and physical events"""
        score = 0.0
        
        # Temporal correlation (events within 24 hours)
        cyber_time = pd.to_datetime(cyber_threat["created_at"])
        physical_time = pd.to_datetime(physical_event["created_at"])
        time_diff = abs((cyber_time - physical_time).total_seconds())
        
        if time_diff < 86400:  # 24 hours
            score += 0.3 * (1 - time_diff / 86400)
        
        # Geographic correlation (events within 10km)
        if (cyber_threat["latitude"] and cyber_threat["longitude"] and 
            physical_event["latitude"] and physical_event["longitude"]):
            
            distance = self.calculate_distance(
                cyber_threat["latitude"], cyber_threat["longitude"],
                physical_event["latitude"], physical_event["longitude"]
            )
            
            if distance < 10:  # 10km
                score += 0.4 * (1 - distance / 10)
        
        # Pattern correlation (matching cyber-physical patterns)
        cyber_type = cyber_threat.get("threat_type", "")
        physical_type = physical_event.get("kind", "")
        
        for pattern, indicators in self.cyber_physical_patterns.items():
            if (cyber_type in indicators["cyber_indicators"] and 
                physical_type in indicators["physical_indicators"]):
                score += indicators["correlation_weight"] * 0.3
        
        return min(score, 1.0)

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine formula
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Earth's radius in kilometers
        return c * r

    def determine_correlation_type(self, cyber_threat: pd.Series, physical_event: pd.Series) -> str:
        """Determine the type of correlation between cyber and physical events"""
        cyber_type = cyber_threat.get("threat_type", "")
        physical_type = physical_event.get("kind", "")
        
        if "fraud" in cyber_type.lower() and "anpr" in physical_type.lower():
            return "fraud_vehicle_correlation"
        elif "sim_swap" in cyber_type.lower() and "theft" in physical_type.lower():
            return "sim_swap_theft_correlation"
        elif "phishing" in cyber_type.lower() and "cyber_fraud" in physical_type.lower():
            return "phishing_fraud_correlation"
        else:
            return "general_correlation"

    def generate_evidence_links(self, cyber_threat: pd.Series, physical_event: pd.Series) -> List[str]:
        """Generate evidence links between cyber and physical events"""
        links = []
        
        # Temporal link
        links.append(f"Events occurred within 24 hours of each other")
        
        # Geographic link
        if (cyber_threat["latitude"] and cyber_threat["longitude"] and 
            physical_event["latitude"] and physical_event["longitude"]):
            distance = self.calculate_distance(
                cyber_threat["latitude"], cyber_threat["longitude"],
                physical_event["latitude"], physical_event["longitude"]
            )
            links.append(f"Events occurred within {distance:.1f}km of each other")
        
        # Pattern link
        cyber_type = cyber_threat.get("threat_type", "")
        physical_type = physical_event.get("kind", "")
        links.append(f"Cyber threat type '{cyber_type}' correlates with physical event type '{physical_type}'")
        
        return links

    def generate_threat_intelligence_report(self) -> Dict[str, Any]:
        """Generate comprehensive threat intelligence report"""
        logger.info("Generating threat intelligence report...")
        
        conn = sqlite3.connect(self.db_path)
        
        # Get threat statistics
        threat_stats = pd.read_sql('''
            SELECT 
                source,
                COUNT(*) as event_count,
                AVG(severity_score) as avg_severity,
                AVG(confidence_score) as avg_confidence
            FROM threat_events 
            WHERE created_at >= datetime('now', '-30 days')
            GROUP BY source
        ''', conn)
        
        # Get top threat types
        top_threats = pd.read_sql('''
            SELECT 
                threat_type,
                COUNT(*) as count,
                AVG(severity_score) as avg_severity
            FROM threat_events 
            WHERE created_at >= datetime('now', '-30 days')
            GROUP BY threat_type
            ORDER BY count DESC
            LIMIT 10
        ''', conn)
        
        # Get geographic distribution
        geo_distribution = pd.read_sql('''
            SELECT 
                country_code,
                city,
                COUNT(*) as event_count,
                AVG(severity_score) as avg_severity
            FROM threat_events 
            WHERE created_at >= datetime('now', '-30 days')
            AND country_code IS NOT NULL
            GROUP BY country_code, city
            ORDER BY event_count DESC
            LIMIT 20
        ''', conn)
        
        # Get correlations
        correlations = pd.read_sql('''
            SELECT 
                correlation_type,
                COUNT(*) as correlation_count,
                AVG(correlation_score) as avg_score
            FROM cyber_physical_correlations 
            WHERE created_at >= datetime('now', '-7 days')
            GROUP BY correlation_type
            ORDER BY correlation_count DESC
        ''', conn)
        
        conn.close()
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "report_period": "30_days",
            "threat_statistics": {
                "total_events": threat_stats["event_count"].sum(),
                "sources": threat_stats.to_dict('records'),
                "top_threat_types": top_threats.to_dict('records'),
                "geographic_distribution": geo_distribution.to_dict('records')
            },
            "correlations": {
                "total_correlations": correlations["correlation_count"].sum(),
                "correlation_types": correlations.to_dict('records')
            },
            "recommendations": self.generate_threat_recommendations(threat_stats, top_threats, correlations)
        }
        
        return report

    def generate_threat_recommendations(self, threat_stats: pd.DataFrame, 
                                      top_threats: pd.DataFrame, 
                                      correlations: pd.DataFrame) -> List[str]:
        """Generate threat intelligence recommendations"""
        recommendations = []
        
        # High-severity threat recommendations
        high_severity_threats = top_threats[top_threats["avg_severity"] > 0.7]
        if not high_severity_threats.empty:
            recommendations.append(
                f"Focus on {high_severity_threats.iloc[0]['threat_type']} threats - "
                f"highest severity score ({high_severity_threats.iloc[0]['avg_severity']:.2f})"
            )
        
        # Correlation recommendations
        if not correlations.empty:
            top_correlation = correlations.iloc[0]
            recommendations.append(
                f"Investigate {top_correlation['correlation_type']} correlations - "
                f"{top_correlation['correlation_count']} instances found"
            )
        
        # Source recommendations
        if not threat_stats.empty:
            top_source = threat_stats.iloc[0]
            recommendations.append(
                f"Monitor {top_source['source']} feed closely - "
                f"{top_source['event_count']} events in last 30 days"
            )
        
        return recommendations

    def run_threat_intelligence_analysis(self, api_keys: Dict[str, str] = None):
        """Run complete threat intelligence analysis"""
        logger.info("Starting threat intelligence analysis...")
        
        # Setup database
        self.setup_threat_database()
        
        # Sample IP addresses for testing (replace with real data)
        test_ips = [
            "41.0.0.1",  # South African IP
            "8.8.8.8",   # Google DNS
            "1.1.1.1"    # Cloudflare DNS
        ]
        
        if api_keys:
            # Enrich IP addresses
            for ip in test_ips:
                enrichment_data = self.enrich_ip_address(ip, api_keys)
                logger.info(f"Enriched {ip}: threat score {enrichment_data['threat_score']:.2f}")
        
        # Correlate cyber-physical threats
        correlations = self.correlate_cyber_physical_threats()
        
        # Generate report
        report = self.generate_threat_intelligence_report()
        
        # Save report
        report_file = self.data_dir / "threat_intelligence_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info("Threat intelligence analysis completed")
        return report

if __name__ == "__main__":
    threat_intel = SentinelThreatIntelligence()
    
    # Sample API keys (replace with real keys)
    api_keys = {
        "abuseipdb_key": "your_abuseipdb_key_here",
        "shodan_key": "your_shodan_key_here",
        "virustotal_key": "your_virustotal_key_here"
    }
    
    report = threat_intel.run_threat_intelligence_analysis(api_keys)
    print(f"Threat intelligence analysis completed. Report saved to {threat_intel.data_dir}")
