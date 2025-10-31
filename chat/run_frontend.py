#!/usr/bin/env python3
"""
Frontend launcher for Imarika Agricultural AI Assistant
Professional UI/UX system for showcase and production use
"""

import subprocess
import sys
import os

def main():
    """Launch the professional frontend"""
    
    print("🌾 Starting Imarika Professional Frontend...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("frontend/modern_ui.py"):
        print("❌ Error: frontend/modern_ui.py not found")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Launch Streamlit app
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "frontend/modern_ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--theme.primaryColor", "#10a37f",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f8f9fa"
        ]
        
        print("🚀 Launching professional frontend...")
        print("📱 Access at: http://localhost:8501")
        print("🌐 Network access: http://0.0.0.0:8501")
        print("\n💡 Features available:")
        print("   • Modern Glass Morphism Design")
        print("   • Gradient Backgrounds")
        print("   • Interactive Suggestion Cards")
        print("   • Smooth Animations")
        print("   • Enhanced Agricultural AI")
        print("\n⏹️  Press Ctrl+C to stop")
        print("=" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()