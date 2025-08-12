#!/usr/bin/env python3
"""
Startup script for CV Chequer FastAPI application.
Handles configuration validation and server startup.
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main startup function."""
    print("🚀 Starting CV Chequer API Server...")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("   Make sure to configure your AWS credentials.")
        print("   You can create a .env file with:")
        print("   AWS_ACCESS_KEY_ID=your_access_key")
        print("   AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("   AWS_REGION=us-east-1")
        print("   AWS_BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0")
        print()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"📍 Server will start on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"📖 ReDoc Documentation: http://{host}:{port}/redoc")
    print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
