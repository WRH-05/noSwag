#!/usr/bin/env python3
"""
Build standalone executable for noSwag
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_executable():
    """Build standalone executable"""
    print("🔨 Building noSwag executable...")
    
    # Check if required files exist
    required_files = ["noSwag.py", "storage_manager.py", "auth_manager.py", 
                     "password_generator.py", "crypto_manager.py"]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # PyInstaller command with all dependencies
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file
        "--name", "noswag",            # Executable name
        "--console",                   # Console app
        "--clean",                     # Clean build
        "--distpath", "dist",          # Output directory
        "--workpath", "build",         # Build directory
        "--add-data", ".env.example;.", # Include .env.example
        "--hidden-import", "cryptography",
        "--hidden-import", "dotenv",
        "noSwag.py"                    # Main file
    ]
    
    try:
        print("Building executable... This may take a few minutes.")
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print(f"📁 Location: {os.path.abspath('dist/noswag.exe')}")
        print(f"📏 File size: {os.path.getsize('dist/noswag.exe') / 1024 / 1024:.1f} MB")
        print("\n🎉 To use globally:")
        print("1. Add the 'dist' folder to your system PATH")
        print("2. Or copy noswag.exe to a folder already in PATH (like C:\\Windows\\System32)")
        print("\n✅ Test the executable:")
        print("   dist\\noswag.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all Python modules are installed:")
        print("   pip install cryptography python-dotenv")
        print("2. Check that all .py files are in the current directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_executable():
    """Test the built executable"""
    exe_path = "dist/noswag.exe"
    if os.path.exists(exe_path):
        print("\n🧪 Testing executable...")
        try:
            result = subprocess.run([exe_path, "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Executable test passed!")
            else:
                print("⚠️ Executable runs but may have issues")
        except subprocess.TimeoutExpired:
            print("⚠️ Executable test timed out (this might be normal for interactive apps)")
        except Exception as e:
            print(f"⚠️ Could not test executable: {e}")

if __name__ == "__main__":
    success = install_pyinstaller() and build_executable()
    
    if success:
        test_executable()
        print("\n🎉 Build completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Build failed. Check the errors above.")
        sys.exit(1)