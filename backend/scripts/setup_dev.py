#!/usr/bin/env python3
"""
Development environment setup script for A-EMS backend services.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return None

def setup_virtual_environment():
    """Setup Python virtual environment."""
    print("Setting up Python virtual environment...")
    
    # Create virtual environment
    run_command("python -m venv venv")
    
    # Activate virtual environment (Windows)
    if os.name == 'nt':
        activation_script = "venv\\Scripts\\activate"
    else:
        activation_script = "source venv/bin/activate"
    
    print(f"Virtual environment created. Activate with: {activation_script}")

def install_dependencies():
    """Install Python dependencies for all services."""
    print("Installing Python dependencies...")
    
    services = [
        "api_gateway",
        "services/auth_service",
        "services/sales_service",
        "services/finance_service",
        "services/hr_service",
        "services/products_service",
        "services/risk_service",
        "services/reports_service",
        "services/ai_service"
    ]
    
    # Install shared dependencies first
    shared_requirements = [
        "fastapi[all]==0.104.1",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic[email]==2.5.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "httpx==0.25.2",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "structlog==23.2.0",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1"
    ]
    
    for requirement in shared_requirements:
        result = run_command(f"pip install {requirement}")
        if result:
            print(f"Installed: {requirement}")
    
    # Install service-specific dependencies
    for service in services:
        requirements_file = Path(service) / "requirements.txt"
        if requirements_file.exists():
            print(f"Installing dependencies for {service}")
            run_command(f"pip install -r {requirements_file}")

def setup_environment_files():
    """Setup environment configuration files."""
    print("Setting up environment files...")
    
    # Main .env.example
    env_content = """# Database Configuration
DATABASE_URL=postgresql://aems_user:aems_password@localhost:5432/aems_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Service Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO

# API Gateway Configuration
API_GATEWAY_HOST=0.0.0.0
API_GATEWAY_PORT=8000

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email Configuration (Optional)
SMTP_SERVER=localhost
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=noreply@aems.com

# DeepSeek AI Configuration
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_API_URL=https://api.deepseek.com

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("Created .env.example file")
    print("Copy .env.example to .env and update with your configuration")

def create_database_structure():
    """Create database structure documentation."""
    print("Creating database structure...")
    
    # This would typically run migrations
    # For now, just create a placeholder
    print("Database migrations ready. Run migrations with:")
    print("python -c \"from shared.database.migrations.migration_manager import create_service_migration_manager; create_service_migration_manager('auth').migrate_all()\"")

def main():
    """Main setup function."""
    print("Setting up A-EMS Backend Development Environment")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Setup steps
    setup_virtual_environment()
    install_dependencies()
    setup_environment_files()
    create_database_structure()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate virtual environment")
    print("2. Copy .env.example to .env and configure")
    print("3. Setup PostgreSQL database")
    print("4. Run: python scripts/run_tests.py")
    print("5. Start services with Docker Compose")

if __name__ == "__main__":
    main()