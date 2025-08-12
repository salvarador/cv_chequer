#!/usr/bin/env python3
"""
Installation script for CV Chequer dependencies.
Checks Python version and installs required packages.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install requirements from requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt file not found!")
        return False
    
    print("📦 Installing dependencies...")
    print("   This may take a few minutes...")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All dependencies installed successfully!")
            return True
        else:
            print("❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_aws_credentials():
    """Check if AWS credentials are configured."""
    print("\n🔑 Checking AWS credentials...")
    
    # Check environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if aws_access_key and aws_secret_key:
        print("✅ AWS credentials found in environment variables")
        return True
    
    # Check .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print("✅ .env file found - checking for AWS credentials...")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'AWS_ACCESS_KEY_ID' in content and 'AWS_SECRET_ACCESS_KEY' in content:
                print("✅ AWS credentials found in .env file")
                return True
    
    # Check AWS CLI
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ AWS CLI credentials configured")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  AWS credentials not found!")
    print("   Please configure your AWS credentials using one of these methods:")
    print("   1. Environment variables:")
    print("      export AWS_ACCESS_KEY_ID=your_access_key")
    print("      export AWS_SECRET_ACCESS_KEY=your_secret_key")
    print("      export AWS_REGION=us-east-1")
    print()
    print("   2. Create a .env file:")
    print("      AWS_ACCESS_KEY_ID=your_access_key")
    print("      AWS_SECRET_ACCESS_KEY=your_secret_key")
    print("      AWS_REGION=us-east-1")
    print("      AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0")
    print()
    print("   3. AWS CLI configuration:")
    print("      aws configure")
    print()
    
    return False

def main():
    """Main installation function."""
    print("🔧 CV Chequer Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check AWS credentials
    aws_configured = check_aws_credentials()
    
    print("\n" + "=" * 50)
    if aws_configured:
        print("🎉 Installation completed successfully!")
        print("\n🚀 You can now start the API server:")
        print("   python start_api.py")
        print("\n📚 Or run the test suite:")
        print("   python api_example.py")
        print("\n💡 Visit http://localhost:8000/docs for interactive API documentation")
    else:
        print("⚠️  Installation completed with warnings!")
        print("   Please configure your AWS credentials before using the application.")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()
