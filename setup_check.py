#!/usr/bin/env python3
"""
AWS Setup Verification Script
Run this to diagnose AWS credential and service access issues.
"""

import os
import sys
from config import print_config_info, get_aws_session, validate_aws_services


def check_dependencies():
    """Check if required Python packages are installed"""
    print("Checking Python dependencies...")
    
    required_packages = ['boto3', 'tabulate', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - NOT INSTALLED")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✓ All required packages are installed")
    return True


def check_aws_credentials():
    """Check various ways AWS credentials might be configured"""
    print("\nChecking AWS credential sources...")
    
    # Check environment variables
    env_creds = {
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'AWS_SESSION_TOKEN': os.getenv('AWS_SESSION_TOKEN'),
        'AWS_REGION': os.getenv('AWS_REGION'),
        'AWS_PROFILE': os.getenv('AWS_PROFILE')
    }
    
    print("Environment variables:")
    for key, value in env_creds.items():
        if value:
            display_value = value if key == 'AWS_REGION' or key == 'AWS_PROFILE' else f"***{value[-4:]}"
            print(f"  ✓ {key}: {display_value}")
        else:
            print(f"  ✗ {key}: Not set")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("  ✓ .env file found")
    else:
        print("  ✗ .env file not found")
    
    # Check for AWS CLI credentials
    aws_config_dir = os.path.expanduser('~/.aws')
    if os.path.exists(aws_config_dir):
        print(f"  ✓ AWS CLI config directory found: {aws_config_dir}")
        
        credentials_file = os.path.join(aws_config_dir, 'credentials')
        config_file = os.path.join(aws_config_dir, 'config')
        
        if os.path.exists(credentials_file):
            print(f"  ✓ AWS credentials file found: {credentials_file}")
        else:
            print(f"  ✗ AWS credentials file not found: {credentials_file}")
            
        if os.path.exists(config_file):
            print(f"  ✓ AWS config file found: {config_file}")
        else:
            print(f"  ✗ AWS config file not found: {config_file}")
    else:
        print(f"  ✗ AWS CLI config directory not found: {aws_config_dir}")


def suggest_fixes():
    """Suggest ways to fix common credential issues"""
    print("\n" + "="*60)
    print("SUGGESTED FIXES FOR AWS CREDENTIAL ISSUES")
    print("="*60)
    
    print("\n1. SET ENVIRONMENT VARIABLES:")
    print("   export AWS_ACCESS_KEY_ID=your_access_key_here")
    print("   export AWS_SECRET_ACCESS_KEY=your_secret_key_here")
    print("   export AWS_REGION=us-east-1")
    
    print("\n2. CREATE .env FILE:")
    print("   Create a .env file in this directory with:")
    print("   AWS_ACCESS_KEY_ID=your_access_key_here")
    print("   AWS_SECRET_ACCESS_KEY=your_secret_key_here")
    print("   AWS_REGION=us-east-1")
    
    print("\n3. CONFIGURE AWS CLI:")
    print("   aws configure")
    print("   (This will prompt for your credentials)")
    
    print("\n4. USE IAM ROLES (if running on EC2/Lambda):")
    print("   Attach an appropriate IAM role to your instance")
    
    print("\n5. REQUIRED AWS PERMISSIONS:")
    print("   Your AWS user/role needs the following permissions:")
    print("   - textract:DetectDocumentText")
    print("   - bedrock:InvokeModel")
    print("   - bedrock:ListFoundationModels")
    
    print("\n6. BEDROCK MODEL ACCESS:")
    print("   Make sure you have enabled model access in AWS Bedrock console:")
    print("   AWS Console > Bedrock > Model access > Enable Claude models")


def main():
    print("AWS CV Analyzer Setup Verification")
    print("="*50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check AWS credentials
    check_aws_credentials()
    
    if not deps_ok:
        print("\n✗ Please install missing dependencies first")
        return False
    
    print("\nTesting AWS connection...")
    print_config_info()
    
    try:
        print("\nValidating AWS services...")
        validate_aws_services()
        print("\n✓ SUCCESS: AWS setup is working correctly!")
        print("You can now run the CV analyzer.")
        return True
        
    except Exception as e:
        print(f"\n✗ AWS setup error: {e}")
        suggest_fixes()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
