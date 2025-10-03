#!/usr/bin/env python3
"""
Setup script for the backend application.
This script helps set up the environment without including venv in version control.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path('.env')
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# Google API Configuration\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            f.write("\n# Replace 'your_google_api_key_here' with your actual Google API key\n")
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your actual Google API key")
    else:
        print("✅ .env file already exists")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path('venv')
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Created virtual environment")
    else:
        print("✅ Virtual environment already exists")

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    
    # Determine the correct pip executable
    if os.name == 'nt':  # Windows
        pip_exe = 'venv/Scripts/pip'
    else:  # Unix/Linux/macOS
        pip_exe = 'venv/bin/pip'
    
    subprocess.run([pip_exe, 'install', '-r', 'requirements.txt'], check=True)
    print("✅ Dependencies installed")

def main():
    """Main setup function."""
    print("🚀 Setting up backend environment...")
    
    try:
        create_env_file()
        create_virtual_environment()
        install_dependencies()
        
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Edit .env file and add your Google API key")
        print("2. Activate virtual environment:")
        
        if os.name == 'nt':  # Windows
            print("   Windows: venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("   macOS/Linux: source venv/bin/activate")
        
        print("3. Run the server: python main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
