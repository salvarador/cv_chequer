#!/usr/bin/env python3
"""
Startup script for CV Chequer Frontend

This script starts the React Vite development server for the CV Chequer frontend application.
Ensures proper environment setup and dependency management.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_node_version():
    """Check if Node.js is installed and meets minimum version requirements."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        logger.info(f"✓ Node.js version: {version}")
        
        # Extract major version number
        major_version = int(version.lstrip('v').split('.')[0])
        if major_version < 18:
            logger.error(f"✗ Node.js version {version} is too old. Please install Node.js 18 or newer.")
            return False
            
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("✗ Node.js is not installed. Please install Node.js 18 or newer.")
        return False

def check_npm():
    """Check if npm is available."""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        logger.info(f"✓ npm version: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("✗ npm is not installed. Please install npm.")
        return False

def install_dependencies(frontend_dir):
    """Install frontend dependencies if node_modules doesn't exist."""
    node_modules_dir = frontend_dir / 'node_modules'
    
    if not node_modules_dir.exists():
        logger.info("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            logger.info("✓ Frontend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to install dependencies: {e}")
            return False
    else:
        logger.info("✓ Frontend dependencies already installed")
    
    return True

def create_env_file(frontend_dir):
    """Create .env file if it doesn't exist."""
    env_file = frontend_dir / '.env'
    env_example = frontend_dir / '.env.example'
    
    if not env_file.exists():
        if env_example.exists():
            logger.info("📝 Creating .env file from .env.example...")
            with open(env_example, 'r') as src:
                content = src.read()
            with open(env_file, 'w') as dst:
                dst.write(content)
            logger.info("✓ .env file created")
        else:
            logger.info("📝 Creating default .env file...")
            default_env = """# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# App Configuration
VITE_APP_NAME=CV Chequer
VITE_APP_VERSION=1.0.0
"""
            with open(env_file, 'w') as f:
                f.write(default_env)
            logger.info("✓ Default .env file created")
    else:
        logger.info("✓ .env file exists")

def start_dev_server(frontend_dir):
    """Start the Vite development server."""
    logger.info("🚀 Starting frontend development server...")
    logger.info("📱 Frontend will be available at: http://localhost:3000")
    logger.info("🔗 Make sure the backend API is running at: http://localhost:8000")
    logger.info("⚡ Press Ctrl+C to stop the server")
    
    try:
        # Use npm run dev to start the development server
        subprocess.run(['npm', 'run', 'dev'], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        logger.info("\n🛑 Frontend server stopped by user")
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Failed to start frontend server: {e}")
        return False
    
    return True

def main():
    """Main function to start the frontend application."""
    # Get the project root directory
    project_root = Path(__file__).parent
    frontend_dir = project_root / 'frontend'
    
    logger.info("🎯 Starting CV Chequer Frontend")
    logger.info(f"📁 Project root: {project_root}")
    logger.info(f"📁 Frontend directory: {frontend_dir}")
    
    # Check if frontend directory exists
    if not frontend_dir.exists():
        logger.error(f"✗ Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    # Check system requirements
    if not check_node_version():
        sys.exit(1)
    
    if not check_npm():
        sys.exit(1)
    
    # Setup environment
    create_env_file(frontend_dir)
    
    # Install dependencies
    if not install_dependencies(frontend_dir):
        sys.exit(1)
    
    # Start development server
    if not start_dev_server(frontend_dir):
        sys.exit(1)

if __name__ == "__main__":
    main()
