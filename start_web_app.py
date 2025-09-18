#!/usr/bin/env python3
"""
Startup script for Sentinel Web Application
Launches the web application with proper configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements = [
        "streamlit",
        "pandas",
        "plotly",
        "firebase-admin",
        "requests"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def start_web_app():
    """Start the web application"""
    print("🚀 Starting Sentinel Web Application...")
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Start Streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "sentinel_web_app_firebase.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "true",
            "--global.developmentMode", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main function"""
    print("🛡️ Sentinel Web Application Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("sentinel_web_app_firebase.py").exists():
        print("❌ Error: sentinel_web_app_firebase.py not found")
        print("Please run this script from the sentinel_package directory")
        return
    
    # Install requirements
    install_requirements()
    
    print("\n🌐 Starting web application...")
    print("The application will be available at:")
    print("  - Local: http://localhost:8501")
    print("  - Network: http://0.0.0.0:8501")
    print("\n📋 Demo Credentials:")
    print("  Police: police@saps.gov.za / police123")
    print("  Security: security@adt.co.za / security123")
    print("  Insurance: agent@santam.co.za / insurance123")
    print("  Bank: rep@standardbank.co.za / bank123")
    print("\n⚠️  Note: Only Police Officers have access to the Threat Map tab")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    # Start the application
    start_web_app()

if __name__ == "__main__":
    main()
