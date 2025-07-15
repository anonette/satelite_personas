#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

print("🔍 Testing Python imports...")
print(f"📁 Working directory: {current_dir}")
print(f"🐍 Python path includes: {str(current_dir)}")

try:
    print("\n🧪 Testing core.config import...")
    from core.config import get_config
    print("✅ core.config imported successfully")
    
    print("\n🧪 Testing config function...")
    config = get_config()
    print(f"✅ Config loaded: {type(config)}")
    
    print("\n🧪 Testing spectral multiplicity import...")
    from core.personas.spectral_multiplicity_notebook import SpectralMultiplicityPipeline
    print("✅ SpectralMultiplicityPipeline imported successfully")
    
    print("\n🧪 Testing theater stage import...")
    from core.theater.civic_theater_stage import CivicTheaterStage
    print("✅ CivicTheaterStage imported successfully")
    
    print("\n🎉 All imports successful! The system should work correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"📍 Error details: {type(e).__name__}: {str(e)}")
    print("\n🔧 Debugging info:")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {current_dir}")
    print("Python path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"📍 Error details: {type(e).__name__}: {str(e)}")
