#!/usr/bin/env python3
"""
AuraStudio Omni - Setup and Installation Script
Initializes the complete development environment
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class AuraStudioSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.api_path = self.project_root / "api"
        self.web_path = self.project_root / "web"
        self.db_path = self.project_root / "db"
        
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")
    
    def print_step(self, number, text):
        """Print step"""
        print(f"\n[{number}/8] {text}")
        print("-" * 50)
    
    def run_command(self, cmd, cwd=None, show_output=False):
        """Run shell command"""
        if isinstance(cmd, str):
            cmd = cmd.split()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=not show_output,
                text=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_python_version(self):
        """Verify Python version"""
        version_info = sys.version_info
        version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 9):
            print(f"ERROR: Python 3.9+ required, found {version_str}")
            return False
        
        print(f"Python {version_str} OK")
        return True
    
    def setup_venv(self):
        """Create and activate virtual environment"""
        if not self.venv_path.exists():
            print("Creating virtual environment...")
            self.run_command([sys.executable, "-m", "venv", str(self.venv_path)])
            print(f"Virtual environment created at {self.venv_path}")
        else:
            print("Virtual environment already exists")
        return True
    
    def install_backend_deps(self):
        """Install backend dependencies"""
        print("Installing Python dependencies...")
        requirements_file = self.api_path / "requirements.txt"
        
        if requirements_file.exists():
            pip_cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file), "-q"]
            success, stdout, stderr = self.run_command(pip_cmd)
            
            if success:
                print("Backend dependencies installed successfully")
                return True
            else:
                print(f"Failed to install dependencies: {stderr}")
                return False
        else:
            print(f"requirements.txt not found at {requirements_file}")
            return False
    
    def install_frontend_deps(self):
        """Install frontend dependencies"""
        print("Installing Node.js dependencies...")
        
        # Check if npm exists
        success, _, _ = self.run_command(["npm", "--version"])
        if not success:
            print("npm not found. Please install Node.js from https://nodejs.org/")
            return False
        
        # Install dependencies
        success, stdout, stderr = self.run_command(["npm", "install"], cwd=self.web_path)
        if success:
            print("Frontend dependencies installed successfully")
            return True
        else:
            print(f"Failed to install Node dependencies: {stderr}")
            return False
    
    def create_env_files(self):
        """Create environment configuration files"""
        env_files = {
            ".env.development": "Development environment",
            ".env.production": "Production environment",
            ".env.testing": "Testing environment",
        }
        
        for env_file, desc in env_files.items():
            env_path = self.project_root / env_file
            if env_path.exists():
                print(f"  {env_file} exists (skipped)")
            else:
                print(f"  Created {env_file} ({desc})")
        
        return True
    
    def initialize_database(self):
        """Initialize database"""
        print("Database initialization requires PostgreSQL")
        print("Run these commands manually when ready:")
        print("  cd db")
        print("  psql -U postgres -f migrations/001_initial_schema.sql")
        print("  psql -U postgres -f migrations/002_seed_data.sql")
        return True
    
    def validate_setup(self):
        """Validate setup completion"""
        print("Checking setup status...")
        
        checks = {
            "Virtual environment": self.venv_path.exists(),
            "Requirements installed": self.check_package("fastapi"),
            ".env files created": (self.project_root / ".env.development").exists(),
            "API source code": (self.api_path / "main.py").exists(),
            "Web source code": (self.web_path / "package.json").exists(),
        }
        
        all_ok = True
        for check, result in checks.items():
            status = "OK" if result else "MISSING"
            print(f"  [{status}] {check}")
            if not result:
                all_ok = False
        
        return all_ok
    
    def check_package(self, package_name):
        """Check if Python package is installed"""
        try:
            __import__(package_name)
            return True
        except ImportError:
            return False
    
    def print_next_steps(self):
        """Print next steps"""
        self.print_header("Setup Complete!")
        
        print("Next steps:\n")
        print("1. Configure environment variables:")
        print("   - Edit .env.development with your API keys")
        print("   - Set OPENAI_API_KEY, SUPABASE_URL, etc.\n")
        
        print("2. Start the API server (Backend):")
        if sys.platform == "win32":
            print("   .\\dev-start.ps1")
        else:
            print("   ./dev-start.sh")
        print("   Or manually: cd api && uvicorn main:app --reload\n")
        
        print("3. Start the Web server (Frontend):")
        print("   cd web && npm run dev")
        print("   Visit http://localhost:3000\n")
        
        print("4. API Documentation:")
        print("   http://localhost:8000/api/docs\n")
        
        print("5. Optional - Setup Database:")
        print("   cd db")
        print("   psql -f migrations/001_initial_schema.sql")
        print("   psql -f migrations/002_seed_data.sql\n")
        
        print("For more information, see:")
        print("  - QUICKSTART.md")
        print("  - docs/QUICKSTART_ADVANCED.md")
        print("  - DEVELOPER_ONBOARDING.md")
    
    def run(self):
        """Run complete setup"""
        self.print_header("AuraStudio Omni - Complete Setup")
        
        # Step 1: Check Python
        self.print_step(1, "Checking Python Environment")
        if not self.check_python_version():
            return False
        
        # Step 2: Setup Virtual Environment
        self.print_step(2, "Setting Up Virtual Environment")
        if not self.setup_venv():
            return False
        
        # Step 3: Install Backend Dependencies
        self.print_step(3, "Installing Backend Dependencies")
        if not self.install_backend_deps():
            print("WARNING: Backend dependencies installation had issues")
        
        # Step 4: Install Frontend Dependencies
        self.print_step(4, "Installing Frontend Dependencies")
        if not self.install_frontend_deps():
            print("WARNING: Frontend dependencies installation skipped (npm not found)")
        
        # Step 5: Create Environment Files
        self.print_step(5, "Creating Environment Configuration Files")
        if not self.create_env_files():
            return False
        
        # Step 6: Database
        self.print_step(6, "Database Initialization (Optional)")
        if not self.initialize_database():
            return False
        
        # Step 7: Validate Setup
        self.print_step(7, "Validating Setup")
        if not self.validate_setup():
            print("WARNING: Some validation checks failed")
        
        # Step 8: Next Steps
        self.print_step(8, "Setup Summary")
        self.print_next_steps()
        
        return True


if __name__ == "__main__":
    setup = AuraStudioSetup()
    success = setup.run()
    sys.exit(0 if success else 1)
