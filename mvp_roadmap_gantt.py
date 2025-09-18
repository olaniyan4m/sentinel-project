#!/usr/bin/env python3
"""
Sentinel MVP Product Roadmap with GANTT Chart
Detailed milestone-based roadmap with timeline visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import json
from pathlib import Path

class SentinelMVPRoadmap:
    def __init__(self):
        self.start_date = datetime(2025, 1, 1)  # Project start date
        self.phases = {
            "Phase 0": {"duration": 12, "color": "#FF6B6B", "description": "Foundation & Pilot"},
            "Phase 1": {"duration": 24, "color": "#4ECDC4", "description": "Core Development"},
            "Phase 2": {"duration": 36, "color": "#45B7D1", "description": "Scale & Integration"},
            "Phase 3": {"duration": 24, "color": "#96CEB4", "description": "National Deployment"}
        }
        
    def create_detailed_roadmap(self):
        """Create detailed MVP roadmap with milestones"""
        
        roadmap_data = [
            # Phase 0: Foundation & Pilot (Months 1-3)
            {
                "phase": "Phase 0",
                "milestone": "Project Initiation",
                "start_week": 1,
                "duration_weeks": 2,
                "owner": "PM",
                "dependencies": [],
                "deliverables": ["Project charter", "Team assembly", "Stakeholder alignment"],
                "success_criteria": ["Team hired", "Budget approved", "Stakeholders aligned"]
            },
            {
                "phase": "Phase 0",
                "milestone": "Stakeholder Partnerships",
                "start_week": 3,
                "duration_weeks": 4,
                "owner": "BD",
                "dependencies": ["Project Initiation"],
                "deliverables": ["Private security MoUs", "Bank partnerships", "Insurance agreements"],
                "success_criteria": ["3+ security partners", "2+ bank partnerships", "2+ insurance partners"]
            },
            {
                "phase": "Phase 0",
                "milestone": "Technical Foundation",
                "start_week": 1,
                "duration_weeks": 8,
                "owner": "Tech Lead",
                "dependencies": [],
                "deliverables": ["Infrastructure setup", "Database design", "API framework"],
                "success_criteria": ["Cloud infrastructure ready", "Database deployed", "API endpoints functional"]
            },
            {
                "phase": "Phase 0",
                "milestone": "MVP ANPR System",
                "start_week": 4,
                "duration_weeks": 6,
                "owner": "ML Engineer",
                "dependencies": ["Technical Foundation"],
                "deliverables": ["ANPR model training", "Edge deployment", "Real-time processing"],
                "success_criteria": ["95%+ ANPR accuracy", "50ms inference time", "10+ edge devices deployed"]
            },
            {
                "phase": "Phase 0",
                "milestone": "Mobile App MVP",
                "start_week": 6,
                "duration_weeks": 8,
                "owner": "Mobile Dev",
                "dependencies": ["Technical Foundation"],
                "deliverables": ["Android app", "iOS app", "Citizen reporting features"],
                "success_criteria": ["App store approval", "1000+ downloads", "50+ daily active users"]
            },
            {
                "phase": "Phase 0",
                "milestone": "Pilot Deployment",
                "start_week": 10,
                "duration_weeks": 4,
                "owner": "Ops Team",
                "dependencies": ["MVP ANPR System", "Mobile App MVP", "Stakeholder Partnerships"],
                "deliverables": ["Sandton CBD deployment", "User training", "Performance monitoring"],
                "success_criteria": ["20+ edge devices active", "30% detection improvement", "User satisfaction >80%"]
            },
            
            # Phase 1: Core Development (Months 4-9)
            {
                "phase": "Phase 1",
                "milestone": "Advanced ML Models",
                "start_week": 14,
                "duration_weeks": 12,
                "owner": "ML Engineer",
                "dependencies": ["Pilot Deployment"],
                "deliverables": ["Gunshot detection", "Weapon detection", "Behavioral analysis"],
                "success_criteria": ["90%+ gunshot accuracy", "85%+ weapon detection", "Real-time processing"]
            },
            {
                "phase": "Phase 1",
                "milestone": "Threat Intelligence Integration",
                "start_week": 16,
                "duration_weeks": 10,
                "owner": "Security Engineer",
                "dependencies": ["Technical Foundation"],
                "deliverables": ["Cyber threat feeds", "OSINT integration", "Threat correlation"],
                "success_criteria": ["5+ threat feeds integrated", "Real-time correlation", "Automated alerts"]
            },
            {
                "phase": "Phase 1",
                "milestone": "Bank Integration",
                "start_week": 18,
                "duration_weeks": 8,
                "owner": "Integration Engineer",
                "dependencies": ["Stakeholder Partnerships"],
                "deliverables": ["Fraud detection API", "Real-time alerts", "Cross-domain correlation"],
                "success_criteria": ["2+ banks integrated", "Fraud detection working", "Response time <5min"]
            },
            {
                "phase": "Phase 1",
                "milestone": "Scale to 3 Cities",
                "start_week": 20,
                "duration_weeks": 16,
                "owner": "Ops Team",
                "dependencies": ["Advanced ML Models", "Threat Intelligence Integration"],
                "deliverables": ["Cape Town deployment", "Durban deployment", "Performance optimization"],
                "success_criteria": ["100+ edge devices", "3 cities active", "40% detection improvement"]
            },
            
            # Phase 2: Scale & Integration (Months 10-21)
            {
                "phase": "Phase 2",
                "milestone": "National Infrastructure",
                "start_week": 36,
                "duration_weeks": 20,
                "owner": "Infrastructure Team",
                "dependencies": ["Scale to 3 Cities"],
                "deliverables": ["Multi-region deployment", "Load balancing", "Disaster recovery"],
                "success_criteria": ["9 provinces covered", "99.9% uptime", "Auto-scaling working"]
            },
            {
                "phase": "Phase 2",
                "milestone": "Advanced Analytics",
                "start_week": 40,
                "duration_weeks": 16,
                "owner": "Data Scientist",
                "dependencies": ["National Infrastructure"],
                "deliverables": ["Predictive analytics", "Crime forecasting", "Pattern recognition"],
                "success_criteria": ["80%+ prediction accuracy", "Real-time forecasting", "Pattern detection"]
            },
            {
                "phase": "Phase 2",
                "milestone": "Law Enforcement Gateway",
                "start_week": 44,
                "duration_weeks": 12,
                "owner": "Legal/Compliance",
                "dependencies": ["Advanced Analytics"],
                "deliverables": ["LE portal", "Audit trails", "Legal compliance"],
                "success_criteria": ["Legal approval", "Audit compliance", "LE adoption"]
            },
            {
                "phase": "Phase 2",
                "milestone": "Full Ecosystem Integration",
                "start_week": 48,
                "duration_weeks": 20,
                "owner": "Integration Team",
                "dependencies": ["Law Enforcement Gateway"],
                "deliverables": ["All banks integrated", "Insurance integration", "Government systems"],
                "success_criteria": ["10+ banks", "5+ insurers", "Government approval"]
            },
            
            # Phase 3: National Deployment (Months 22-30)
            {
                "phase": "Phase 3",
                "milestone": "National Rollout",
                "start_week": 68,
                "duration_weeks": 24,
                "owner": "Ops Team",
                "dependencies": ["Full Ecosystem Integration"],
                "deliverables": ["National deployment", "User training", "Support systems"],
                "success_criteria": ["500+ edge devices", "50,000+ users", "45% crime reduction"]
            }
        ]
        
        return roadmap_data
    
    def create_gantt_chart(self, roadmap_data):
        """Create GANTT chart visualization"""
        
        # Prepare data for GANTT chart
        gantt_data = []
        for item in roadmap_data:
            start_date = self.start_date + timedelta(weeks=item["start_week"] - 1)
            end_date = start_date + timedelta(weeks=item["duration_weeks"])
            
            gantt_data.append({
                "Task": f"{item['milestone']} ({item['phase']})",
                "Start": start_date,
                "Finish": end_date,
                "Duration": item["duration_weeks"],
                "Owner": item["owner"],
                "Phase": item["phase"]
            })
        
        # Create GANTT chart
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Color mapping for phases
        phase_colors = {
            "Phase 0": "#FF6B6B",
            "Phase 1": "#4ECDC4", 
            "Phase 2": "#45B7D1",
            "Phase 3": "#96CEB4"
        }
        
        # Plot GANTT bars
        y_pos = 0
        for i, task in enumerate(gantt_data):
            start = task["Start"]
            duration = task["Duration"]
            end = task["Finish"]
            
            color = phase_colors.get(task["Phase"], "#CCCCCC")
            
            ax.barh(y_pos, duration, left=start, height=0.6, 
                   color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
            
            # Add task label
            ax.text(start + timedelta(weeks=duration/2), y_pos, 
                   task["Task"], ha='center', va='center', 
                   fontsize=8, fontweight='bold')
            
            y_pos += 1
        
        # Customize chart
        ax.set_yticks(range(len(gantt_data)))
        ax.set_yticklabels([f"{task['Task']} ({task['Owner']})" for task in gantt_data])
        ax.set_xlabel('Timeline (Weeks)')
        ax.set_title('Sentinel MVP Product Roadmap - GANTT Chart', fontsize=16, fontweight='bold')
        
        # Format x-axis
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        
        # Add phase legend
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=phase) 
                          for phase, color in phase_colors.items()]
        ax.legend(handles=legend_elements, loc='upper right')
        
        # Add milestone markers
        milestone_weeks = [12, 24, 36, 48, 68, 92]  # Key milestone weeks
        for week in milestone_weeks:
            milestone_date = self.start_date + timedelta(weeks=week-1)
            ax.axvline(x=milestone_date, color='red', linestyle='--', alpha=0.7)
            ax.text(milestone_date, len(gantt_data)-0.5, f'Week {week}', 
                   rotation=90, ha='right', va='top', fontsize=8, color='red')
        
        plt.tight_layout()
        return fig
    
    def create_milestone_timeline(self, roadmap_data):
        """Create milestone timeline with key deliverables"""
        
        milestones = [
            {
                "week": 12,
                "milestone": "Phase 0 Complete",
                "description": "Pilot deployment in Sandton CBD",
                "key_metrics": ["20+ edge devices", "30% detection improvement", "1000+ app users"],
                "deliverables": ["MVP ANPR system", "Mobile app", "Basic dashboard"]
            },
            {
                "week": 24,
                "milestone": "Phase 1 Complete", 
                "description": "3 cities deployed with advanced features",
                "key_metrics": ["100+ edge devices", "40% detection improvement", "10,000+ users"],
                "deliverables": ["Gunshot detection", "Threat intelligence", "Bank integration"]
            },
            {
                "week": 36,
                "milestone": "Phase 2 Complete",
                "description": "National infrastructure with full integration",
                "key_metrics": ["300+ edge devices", "45% detection improvement", "25,000+ users"],
                "deliverables": ["National infrastructure", "Advanced analytics", "LE gateway"]
            },
            {
                "week": 48,
                "milestone": "Full Ecosystem",
                "description": "Complete integration with all partners",
                "key_metrics": ["500+ edge devices", "50% detection improvement", "50,000+ users"],
                "deliverables": ["All banks integrated", "Insurance integration", "Government systems"]
            },
            {
                "week": 68,
                "milestone": "National Deployment",
                "description": "Full national rollout complete",
                "key_metrics": ["1000+ edge devices", "55% detection improvement", "100,000+ users"],
                "deliverables": ["National coverage", "Full ecosystem", "Operational excellence"]
            }
        ]
        
        return milestones
    
    def create_resource_plan(self):
        """Create resource allocation plan"""
        
        resources = {
            "Phase 0": {
                "team_size": 8,
                "roles": {
                    "Product Manager": 1,
                    "Tech Lead": 1,
                    "ML Engineer": 1,
                    "Backend Developer": 2,
                    "Mobile Developer": 1,
                    "DevOps Engineer": 1,
                    "Business Development": 1
                },
                "budget": 2500000,  # R2.5M
                "duration_weeks": 12
            },
            "Phase 1": {
                "team_size": 12,
                "roles": {
                    "Product Manager": 1,
                    "Tech Lead": 1,
                    "ML Engineer": 2,
                    "Backend Developer": 3,
                    "Frontend Developer": 1,
                    "Mobile Developer": 1,
                    "DevOps Engineer": 1,
                    "Security Engineer": 1,
                    "Business Development": 1
                },
                "budget": 5000000,  # R5M
                "duration_weeks": 24
            },
            "Phase 2": {
                "team_size": 18,
                "roles": {
                    "Product Manager": 1,
                    "Tech Lead": 1,
                    "ML Engineer": 3,
                    "Backend Developer": 4,
                    "Frontend Developer": 2,
                    "Mobile Developer": 1,
                    "DevOps Engineer": 2,
                    "Security Engineer": 2,
                    "Data Scientist": 1,
                    "Legal/Compliance": 1
                },
                "budget": 10000000,  # R10M
                "duration_weeks": 36
            },
            "Phase 3": {
                "team_size": 25,
                "roles": {
                    "Product Manager": 2,
                    "Tech Lead": 2,
                    "ML Engineer": 4,
                    "Backend Developer": 6,
                    "Frontend Developer": 3,
                    "Mobile Developer": 2,
                    "DevOps Engineer": 3,
                    "Security Engineer": 2,
                    "Data Scientist": 2,
                    "Legal/Compliance": 1,
                    "Support Engineer": 2
                },
                "budget": 15000000,  # R15M
                "duration_weeks": 24
            }
        }
        
        return resources
    
    def generate_roadmap_report(self):
        """Generate comprehensive roadmap report"""
        
        roadmap_data = self.create_detailed_roadmap()
        milestones = self.create_milestone_timeline(roadmap_data)
        resources = self.create_resource_plan()
        
        # Create GANTT chart
        fig = self.create_gantt_chart(roadmap_data)
        
        # Save GANTT chart
        gantt_file = Path("real_data/sentinel_mvp_gantt_chart.png")
        fig.savefig(gantt_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        # Create comprehensive report
        report = {
            "project_overview": {
                "name": "Sentinel MVP Product Roadmap",
                "total_duration_weeks": 92,
                "total_duration_months": 23,
                "total_budget": 32500000,  # R32.5M
                "start_date": self.start_date.isoformat(),
                "end_date": (self.start_date + timedelta(weeks=92)).isoformat()
            },
            "phases": self.phases,
            "roadmap": roadmap_data,
            "milestones": milestones,
            "resources": resources,
            "risk_mitigation": {
                "technical_risks": [
                    "ML model accuracy below target - Mitigation: Extended training, data augmentation",
                    "Edge device deployment challenges - Mitigation: Pilot testing, vendor partnerships",
                    "Integration complexity - Mitigation: API-first design, modular architecture"
                ],
                "business_risks": [
                    "Partner adoption slower than expected - Mitigation: Early engagement, value demonstration",
                    "Regulatory approval delays - Mitigation: Early legal consultation, compliance framework",
                    "Competition from established players - Mitigation: Unique value proposition, first-mover advantage"
                ],
                "operational_risks": [
                    "Team scaling challenges - Mitigation: Gradual hiring, knowledge transfer",
                    "Infrastructure scaling issues - Mitigation: Cloud-native architecture, auto-scaling",
                    "User adoption challenges - Mitigation: User-centric design, training programs"
                ]
            },
            "success_metrics": {
                "phase_0": {
                    "technical": ["95%+ ANPR accuracy", "50ms inference time", "20+ edge devices"],
                    "business": ["3+ security partners", "1000+ app users", "30% detection improvement"],
                    "operational": ["Team assembled", "Infrastructure ready", "Pilot deployed"]
                },
                "phase_1": {
                    "technical": ["90%+ gunshot accuracy", "100+ edge devices", "Real-time correlation"],
                    "business": ["10,000+ users", "40% detection improvement", "Bank integration"],
                    "operational": ["3 cities deployed", "Advanced features", "Threat intelligence"]
                },
                "phase_2": {
                    "technical": ["500+ edge devices", "99.9% uptime", "Predictive analytics"],
                    "business": ["50,000+ users", "45% detection improvement", "Full ecosystem"],
                    "operational": ["National infrastructure", "LE gateway", "Government approval"]
                },
                "phase_3": {
                    "technical": ["1000+ edge devices", "55% detection improvement", "Operational excellence"],
                    "business": ["100,000+ users", "National coverage", "Market leadership"],
                    "operational": ["Full deployment", "Support systems", "Continuous improvement"]
                }
            }
        }
        
        # Save report
        report_file = Path("real_data/sentinel_mvp_roadmap_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report, gantt_file

if __name__ == "__main__":
    roadmap = SentinelMVPRoadmap()
    report, gantt_file = roadmap.generate_roadmap_report()
    
    print("🎯 Sentinel MVP Roadmap Generated Successfully!")
    print(f"📊 GANTT Chart saved to: {gantt_file}")
    print(f"📋 Report saved to: real_data/sentinel_mvp_roadmap_report.json")
    print(f"⏱️  Total Duration: 23 months (92 weeks)")
    print(f"💰 Total Budget: R32.5M")
    print(f"🎯 Key Milestones: 5 major phases with 15 milestones")
