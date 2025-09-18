#!/usr/bin/env python3
"""
Quick Fix Script for Sentinel Web Application
Fixes common issues and provides immediate access
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_status(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def create_streamlit_config():
    """Create Streamlit config to disable telemetry"""
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.toml"
    config_content = """[browser]
gatherUsageStats = false

[server]
headless = true
port = 8501
address = "0.0.0.0"

[global]
developmentMode = false
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print_status("Created Streamlit config to disable telemetry")

def install_requirements():
    """Install required packages (excluding sqlite3)"""
    requirements = [
        "streamlit",
        "pandas", 
        "plotly",
        "firebase-admin",
        "requests",
        "watchdog"
    ]
    
    print_info("Installing required packages...")
    
    for package in requirements:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ])
            print_status(f"Installed {package}")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install {package}: {e}")

def create_data_directories():
    """Create necessary data directories"""
    directories = ["real_data", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print_status(f"Created directory: {directory}")

def run_application():
    """Run the Streamlit application"""
    print_info("Starting Sentinel Web Application...")
    print_info("Access at: http://localhost:8501")
    print_info("Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "sentinel_web_app_firebase.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print_info("Application stopped by user")
    except Exception as e:
        print_error(f"Error running application: {e}")

def main():
    """Main function"""
    print("🛡️ Sentinel Web Application - Quick Fix & Run")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("sentinel_web_app_firebase.py").exists():
        print_error("sentinel_web_app_firebase.py not found")
        print_info("Please run this script from the sentinel_package directory")
        return
    
    # Fix common issues
    print_info("Fixing common issues...")
    create_streamlit_config()
    create_data_directories()
    
    # Install requirements
    install_requirements()
    
    # Show demo credentials
    print("\n📋 Demo Credentials:")
    print("  Police: police@saps.gov.za / police123")
    print("  Security: security@adt.co.za / security123") 
    print("  Insurance: agent@santam.co.za / insurance123")
    print("  Bank: rep@standardbank.co.za / bank123")
    print("\n⚠️  Note: Police Officers and Bank Representatives have access to the Threat Map tab")
    
    # Run the application
    print("\n🚀 Starting application...")
    run_application()

if __name__ == "__main__":
    main()
