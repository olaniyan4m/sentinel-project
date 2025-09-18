#!/usr/bin/env python3
"""
Firebase Integration for Sentinel Web Application
Integrates with Firebase for authentication, database, and real-time features
"""

import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebaseIntegration:
    def __init__(self):
        self.cred = None
        self.app = None
        self.db = None
        self.initialized = False
        
    def initialize_firebase(self):
        """Initialize Firebase with service account credentials"""
        try:
            # Firebase service account configuration from environment variables
            firebase_config = {
                "type": "service_account",
                "project_id": os.getenv("FIREBASE_PROJECT_ID", "vigilo-fight-crime"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
                "client_id": "115405211372157999404",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40vigilo-fight-crime.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
            
            # Initialize Firebase Admin SDK
            self.cred = credentials.Certificate(firebase_config)
            self.app = firebase_admin.initialize_app(self.cred, {
                'projectId': 'vigilo-fight-crime'
            })
            
            # Initialize Firestore
            self.db = firestore.client()
            
            self.initialized = True
            logger.info("Firebase initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            return False
    
    def create_user(self, email, password, display_name, role):
        """Create a new user in Firebase Auth"""
        try:
            if not self.initialized:
                return None
                
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            
            # Store user role in Firestore
            user_doc = {
                'uid': user.uid,
                'email': email,
                'display_name': display_name,
                'role': role,
                'created_at': datetime.now(),
                'last_login': None,
                'active': True
            }
            
            self.db.collection('users').document(user.uid).set(user_doc)
            
            logger.info(f"User created successfully: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            if not self.initialized:
                return None
                
            # Get user from Firestore
            users = self.db.collection('users').where('email', '==', email).limit(1).get()
            
            if users:
                return users[0].to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None
    
    def update_user_last_login(self, uid):
        """Update user's last login time"""
        try:
            if not self.initialized:
                return False
                
            self.db.collection('users').document(uid).update({
                'last_login': datetime.now()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update last login: {e}")
            return False
    
    def store_threat_event(self, event_data):
        """Store threat event in Firestore"""
        try:
            if not self.initialized:
                return False
                
            event_doc = {
                'event_id': event_data.get('event_id'),
                'ip_address': event_data.get('ip_address'),
                'threat_type': event_data.get('threat_type'),
                'severity_score': event_data.get('severity_score'),
                'confidence_score': event_data.get('confidence_score'),
                'source': event_data.get('source'),
                'country_code': event_data.get('country_code'),
                'latitude': event_data.get('latitude'),
                'longitude': event_data.get('longitude'),
                'city': event_data.get('city'),
                'region': event_data.get('region'),
                'isp': event_data.get('isp'),
                'asn': event_data.get('asn'),
                'first_seen': event_data.get('first_seen'),
                'last_seen': event_data.get('last_seen'),
                'report_count': event_data.get('report_count', 0),
                'categories': event_data.get('categories', []),
                'raw_data': event_data.get('raw_data'),
                'created_at': datetime.now()
            }
            
            self.db.collection('threat_events').add(event_doc)
            
            logger.info(f"Threat event stored: {event_data.get('event_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store threat event: {e}")
            return False
    
    def get_recent_threat_events(self, hours=6, limit=100):
        """Get recent threat events"""
        try:
            if not self.initialized:
                return []
                
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            events = self.db.collection('threat_events')\
                .where('created_at', '>=', cutoff_time)\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .get()
            
            return [event.to_dict() for event in events]
            
        except Exception as e:
            logger.error(f"Failed to get threat events: {e}")
            return []
    
    def store_alert(self, alert_data):
        """Store alert in Firestore"""
        try:
            if not self.initialized:
                return False
                
            alert_doc = {
                'alert_id': alert_data.get('alert_id'),
                'type': alert_data.get('type'),
                'severity': alert_data.get('severity'),
                'location': alert_data.get('location'),
                'description': alert_data.get('description'),
                'status': alert_data.get('status', 'active'),
                'assigned_to': alert_data.get('assigned_to'),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            self.db.collection('alerts').add(alert_doc)
            
            logger.info(f"Alert stored: {alert_data.get('alert_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store alert: {e}")
            return False
    
    def get_active_alerts(self, user_role=None):
        """Get active alerts, optionally filtered by user role"""
        try:
            if not self.initialized:
                return []
                
            query = self.db.collection('alerts').where('status', '==', 'active')
            
            # Filter by role if specified
            if user_role == 'police':
                # Police can see all alerts
                pass
            elif user_role == 'private_security':
                # Private security can see security-related alerts
                query = query.where('type', 'in', ['security', 'perimeter', 'suspicious'])
            elif user_role == 'insurance':
                # Insurance can see fraud-related alerts
                query = query.where('type', 'in', ['fraud', 'claim', 'risk'])
            elif user_role == 'bank':
                # Banks can see financial crime alerts
                query = query.where('type', 'in', ['fraud', 'transaction', 'account'])
            
            alerts = query.order_by('created_at', direction=firestore.Query.DESCENDING).get()
            
            return [alert.to_dict() for alert in alerts]
            
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []
    
    def store_case(self, case_data):
        """Store case in Firestore"""
        try:
            if not self.initialized:
                return False
                
            case_doc = {
                'case_id': case_data.get('case_id'),
                'type': case_data.get('type'),
                'status': case_data.get('status', 'open'),
                'priority': case_data.get('priority', 'medium'),
                'assigned_to': case_data.get('assigned_to'),
                'description': case_data.get('description'),
                'evidence_ids': case_data.get('evidence_ids', []),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            self.db.collection('cases').add(case_doc)
            
            logger.info(f"Case stored: {case_data.get('case_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store case: {e}")
            return False
    
    def get_cases_by_user(self, user_id, user_role):
        """Get cases for a specific user based on their role"""
        try:
            if not self.initialized:
                return []
                
            if user_role == 'police':
                # Police can see all cases
                cases = self.db.collection('cases').get()
            else:
                # Other roles can only see cases assigned to them
                cases = self.db.collection('cases').where('assigned_to', '==', user_id).get()
            
            return [case.to_dict() for case in cases]
            
        except Exception as e:
            logger.error(f"Failed to get cases: {e}")
            return []
    
    def store_evidence(self, evidence_data):
        """Store evidence in Firestore"""
        try:
            if not self.initialized:
                return False
                
            evidence_doc = {
                'evidence_id': evidence_data.get('evidence_id'),
                'type': evidence_data.get('type'),
                'source': evidence_data.get('source'),
                'content': evidence_data.get('content'),
                'metadata': evidence_data.get('metadata'),
                'confidence_score': evidence_data.get('confidence_score'),
                'verification_status': evidence_data.get('verification_status', 'pending'),
                'created_at': datetime.now()
            }
            
            self.db.collection('evidence').add(evidence_doc)
            
            logger.info(f"Evidence stored: {evidence_data.get('evidence_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store evidence: {e}")
            return False
    
    def get_evidence_by_case(self, case_id):
        """Get evidence for a specific case"""
        try:
            if not self.initialized:
                return []
                
            evidence = self.db.collection('evidence')\
                .where('case_id', '==', case_id)\
                .get()
            
            return [doc.to_dict() for doc in evidence]
            
        except Exception as e:
            logger.error(f"Failed to get evidence: {e}")
            return []
    
    def setup_initial_data(self):
        """Setup initial data in Firestore"""
        try:
            if not self.initialized:
                return False
            
            # Create sample users
            sample_users = [
                {
                    'email': 'police@saps.gov.za',
                    'password': 'police123',
                    'display_name': 'Police Officer',
                    'role': 'police'
                },
                {
                    'email': 'security@adt.co.za',
                    'password': 'security123',
                    'display_name': 'Security Officer',
                    'role': 'private_security'
                },
                {
                    'email': 'agent@santam.co.za',
                    'password': 'insurance123',
                    'display_name': 'Insurance Agent',
                    'role': 'insurance'
                },
                {
                    'email': 'rep@standardbank.co.za',
                    'password': 'bank123',
                    'display_name': 'Bank Representative',
                    'role': 'bank'
                }
            ]
            
            for user_data in sample_users:
                self.create_user(
                    user_data['email'],
                    user_data['password'],
                    user_data['display_name'],
                    user_data['role']
                )
            
            # Create sample threat events
            sample_threats = [
                {
                    'event_id': 'THREAT-001',
                    'ip_address': '192.168.1.100',
                    'threat_type': 'ANPR Alert',
                    'severity_score': 8.5,
                    'confidence_score': 0.95,
                    'source': 'edge_device',
                    'country_code': 'ZA',
                    'latitude': -26.2041,
                    'longitude': 28.0473,
                    'city': 'Johannesburg',
                    'region': 'Gauteng',
                    'isp': 'Telkom',
                    'asn': 'AS3741',
                    'first_seen': datetime.now() - timedelta(hours=2),
                    'last_seen': datetime.now(),
                    'report_count': 1,
                    'categories': ['vehicle_theft'],
                    'raw_data': {'plate_number': 'ABC123GP', 'vehicle_type': 'Toyota Hilux'}
                },
                {
                    'event_id': 'THREAT-002',
                    'ip_address': '10.0.0.50',
                    'threat_type': 'Gunshot Detection',
                    'severity_score': 9.2,
                    'confidence_score': 0.92,
                    'source': 'audio_sensor',
                    'country_code': 'ZA',
                    'latitude': -33.9249,
                    'longitude': 18.4241,
                    'city': 'Cape Town',
                    'region': 'Western Cape',
                    'isp': 'Vodacom',
                    'asn': 'AS29975',
                    'first_seen': datetime.now() - timedelta(hours=1),
                    'last_seen': datetime.now(),
                    'report_count': 1,
                    'categories': ['gunshot', 'violence'],
                    'raw_data': {'audio_level': 85, 'frequency': 1200}
                }
            ]
            
            for threat_data in sample_threats:
                self.store_threat_event(threat_data)
            
            # Create sample alerts
            sample_alerts = [
                {
                    'alert_id': 'ALERT-001',
                    'type': 'ANPR',
                    'severity': 'High',
                    'location': 'Sandton CBD',
                    'description': 'Stolen vehicle detected via ANPR system',
                    'status': 'active',
                    'assigned_to': 'police@saps.gov.za'
                },
                {
                    'alert_id': 'ALERT-002',
                    'type': 'Gunshot',
                    'severity': 'Critical',
                    'location': 'Hillbrow',
                    'description': 'Gunshot detected in residential area',
                    'status': 'active',
                    'assigned_to': 'police@saps.gov.za'
                },
                {
                    'alert_id': 'ALERT-003',
                    'type': 'Fraud',
                    'severity': 'High',
                    'location': 'Online',
                    'description': 'Suspicious transaction detected',
                    'status': 'active',
                    'assigned_to': 'rep@standardbank.co.za'
                }
            ]
            
            for alert_data in sample_alerts:
                self.store_alert(alert_data)
            
            logger.info("Initial data setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup initial data: {e}")
            return False

if __name__ == "__main__":
    firebase = FirebaseIntegration()
    
    if firebase.initialize_firebase():
        print("✅ Firebase initialized successfully")
        
        # Setup initial data
        if firebase.setup_initial_data():
            print("✅ Initial data setup completed")
        else:
            print("❌ Failed to setup initial data")
    else:
        print("❌ Failed to initialize Firebase")
