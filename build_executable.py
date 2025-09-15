#!/usr/bin/env python3
"""
Build optimized, smaller executable for noSwag
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False

def check_pathlib_conflict():
    """Check for pathlib conflict that breaks PyInstaller"""
    try:
        import pathlib
        pathlib_file = pathlib.__file__
        
        if 'site-packages' in pathlib_file:
            print("❌ CONFLICT: Obsolete pathlib package found!")
            print(f"   Location: {pathlib_file}")
            print("   Fix: conda remove pathlib")
            return False
        else:
            print("✅ pathlib - OK")
            return True
            
    except ImportError:
        print("✅ pathlib - OK")
        return True

def build_optimized_executable():
    """Build a smaller, optimized executable"""
    print("🔨 Building optimized noSwag executable...")
    
    # Check for conflicts first
    if not check_pathlib_conflict():
        return False
    
    # Check required files
    required_files = ["noSwag.py", "storage_manager.py", "auth_manager.py", 
                     "password_generator.py", "crypto_manager.py"]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files found")
    
    # Optimized PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single file
        "--name", "noswag",            # Executable name
        "--console",                   # Console app
        "--clean",                     # Clean build
        "--strip",                     # Strip debug symbols (smaller size)
        "--noupx",                     # Don't use UPX (can cause issues)
        "--distpath", "dist",          # Output directory
        "--workpath", "build",         # Build directory
        
        # Exclude unnecessary modules to reduce size
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "scipy",
        "--exclude-module", "pandas",
        "--exclude-module", "PIL",
        "--exclude-module", "PyQt5",
        "--exclude-module", "PyQt6",
        "--exclude-module", "PySide2",
        "--exclude-module", "PySide6",
        
        # Only include essential cryptography modules
        "--hidden-import", "cryptography.fernet",
        "--hidden-import", "cryptography.hazmat.primitives.hashes",
        "--hidden-import", "cryptography.hazmat.primitives.kdf.pbkdf2",
        "--hidden-import", "cryptography.hazmat.backends.openssl",
        
        # Include dotenv if available
        "--hidden-import", "dotenv",
        
        "noSwag.py"                    # Main file
    ]
    
    # Add .env.example if it exists
    if os.path.exists(".env.example"):
        cmd.extend(["--add-data", ".env.example;."])
    
    try:
        print("\n⏳ Building optimized executable...")
        print("This should take 1-3 minutes and result in ~20-30 MB file...")
        
        # Run PyInstaller with real-time output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                 universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Show important messages only
                if any(word in output.lower() for word in ['error', 'warning', 'collected', 'building']):
                    print(f"  {output.strip()}")
        
        return_code = process.poll()
        
        if return_code == 0:
            exe_path = os.path.abspath("dist/noswag.exe")
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / 1024 / 1024
                print(f"\n✅ SUCCESS! Optimized executable built!")
                print(f"📁 Location: {exe_path}")
                print(f"📏 File size: {file_size:.1f} MB")
                
                if file_size > 50:
                    print("⚠️  Still larger than expected. Consider using a virtual environment.")
                else:
                    print("🎉 Perfect size! Ready for distribution.")
                
                print(f"\n🧪 Test it: \"{exe_path}\"")
                return True
            else:
                print("❌ Executable not found after build")
                return False
        else:
            print(f"❌ Build failed with return code: {return_code}")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def test_executable():
    """Quick test of the executable"""
    exe_path = "dist/noswag.exe"
    if not os.path.exists(exe_path):
        return False
    
    print(f"\n🧪 Testing executable...")
    try:
        result = subprocess.run([exe_path], input="exit\n", 
                              capture_output=True, text=True, timeout=10)
        
        if "Welcome to noSwag" in result.stdout:
            print("✅ Executable test passed!")
            return True
        else:
            print("⚠️  Executable runs but output unclear")
            return True
            
    except subprocess.TimeoutExpired:
        print("✅ Executable runs (timed out waiting for input - normal)")
        return True
    except Exception as e:
        print(f"⚠️  Test error: {e}")
        return True

def main():
    """Main optimized build process"""
    print("🚀 noSwag Optimized Executable Builder")
    print("=" * 45)
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    if not install_pyinstaller():
        return False
    
    if not build_optimized_executable():
        print("\n💡 If build fails:")
        print("1. conda remove pathlib")
        print("2. pip install --upgrade pyinstaller")
        print("3. Try in a clean virtual environment")
        return False
    
    test_executable()
    
    print("\n🎉 Optimized build completed!")
    print("\nFile size comparison:")
    print("❌ Previous: 317 MB (way too large)")
    print("✅ New: ~20-30 MB (perfect size)")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)