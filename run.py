#!/usr/bin/env python3
"""
AI Web Test Agent - Main Entry Point
Run this file to start the Flask server
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 AI Web Test Agent - Starting Server...")
    print("=" * 60)
    print(f"📁 Project Root: {project_root}")
    print(f"🌐 Server URL: http://localhost:5000")
    print(f"📊 API Endpoint: http://localhost:5000/chat")
    print("=" * 60)
    print("\n✅ Server is running. Press CTRL+C to stop.\n")
    
    app = create_app()
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )