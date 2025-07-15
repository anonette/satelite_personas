#!/usr/bin/env python3
"""
Launch script for the Civic Theater Stage
Automatically sets up the Python path and launches the Streamlit application
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Set PYTHONPATH environment variable as well
os.environ['PYTHONPATH'] = str(current_dir) + os.pathsep + os.environ.get('PYTHONPATH', '')

def main():
    """Launch the Civic Theater Stage"""
    print("🎭 Launching Civic Theater Stage...")
    print(f"📁 Working directory: {current_dir}")
    print(f"🐍 Python path configured: {str(current_dir)}")
    
    try:
        # Test imports
        from core.config import get_config
        print("✅ Core modules imported successfully")
        
        # Launch Streamlit
        import subprocess
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "core/theater/civic_theater_stage.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ]
        
        print("🚀 Starting Streamlit server...")
        print("🌐 Open your browser to: http://localhost:8501")
        
        subprocess.run(cmd, env=os.environ)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and have activated the virtual environment")
        return 1
    except Exception as e:
        print(f"❌ Error launching theater: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
