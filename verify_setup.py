#!/usr/bin/env python
"""
Setup verification script
Run this to check if everything is configured correctly
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print result"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    if not exists:
        print(f"  → File not found!")
    return exists

def check_env_var(var_name, description):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    exists = value is not None
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {var_name}")
    if exists:
        print(f"  → Value: {value}")
    else:
        print(f"  → Not set")
    return exists

def main():
    print("="*60)
    print("SETUP VERIFICATION")
    print("="*60)
    print()
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    print()
    
    # Check .env file
    print("1. Checking .env file...")
    print("-" * 60)
    env_exists = check_file_exists(".env", ".env file")
    
    if env_exists:
        print("\n  Contents of .env:")
        try:
            with open(".env", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        print(f"  {line}")
        except Exception as e:
            print(f"  Error reading .env: {e}")
    print()
    
    # Load .env if it exists
    if env_exists:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✓ Loaded environment variables from .env")
        except ImportError:
            print("✗ python-dotenv not installed!")
            print("  Run: pip install python-dotenv")
            return False
        print()
    
    # Check environment variables
    print("2. Checking environment variables...")
    print("-" * 60)
    creds_path_set = check_env_var("GOOGLE_APPLICATION_CREDENTIALS", "Firebase credentials path")
    db_url_set = check_env_var("FIREBASE_DATABASE_URL", "Firebase database URL")
    print()
    
    # Check Firebase credentials file
    print("3. Checking Firebase credentials file...")
    print("-" * 60)
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if cred_path:
        # Expand path
        cred_path = os.path.expandvars(cred_path)
        cred_path = os.path.expanduser(cred_path)
        
        cred_exists = check_file_exists(cred_path, "Firebase admin SDK key")
        
        if cred_exists:
            # Try to read it as JSON
            try:
                import json
                with open(cred_path, 'r') as f:
                    cred_data = json.load(f)
                    print(f"  ✓ Valid JSON file")
                    print(f"  → Project ID: {cred_data.get('project_id', 'N/A')}")
                    print(f"  → Type: {cred_data.get('type', 'N/A')}")
            except json.JSONDecodeError:
                print(f"  ✗ Invalid JSON file!")
                cred_exists = False
            except Exception as e:
                print(f"  ✗ Error reading file: {e}")
                cred_exists = False
    else:
        cred_exists = False
        print("✗ GOOGLE_APPLICATION_CREDENTIALS not set in environment")
    print()
    
    # Check Python packages
    print("4. Checking required packages...")
    print("-" * 60)
    packages = [
        "firebase_admin",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
    ]
    
    all_packages_installed = True
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_packages_installed = False
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    checks = {
        ".env file exists": env_exists,
        "GOOGLE_APPLICATION_CREDENTIALS set": creds_path_set,
        "Firebase key file exists": cred_exists,
        "All packages installed": all_packages_installed,
    }
    
    all_passed = all(checks.values())
    
    for check, passed in checks.items():
        status = "PASS ✓" if passed else "FAIL ✗"
        print(f"{check:40} {status}")
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All checks passed!")
        print("\nYou can now run:")
        print("  python test_backend.py")
        print("  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nQuick fixes:")
        
        if not env_exists:
            print("\n1. Create .env file:")
            print("   - Create a file named '.env' in the project root")
            print("   - Add this content:")
            print("     GOOGLE_APPLICATION_CREDENTIALS=C:\\dev\\paradox\\firebase-adminsdk-key.json")
            print("     FIREBASE_DATABASE_URL=https://your-project.firebaseio.com")
        
        if not cred_exists:
            print("\n2. Download Firebase Admin SDK key:")
            print("   - Go to https://console.firebase.google.com")
            print("   - Select your project")
            print("   - Go to Project Settings → Service Accounts")
            print("   - Click 'Generate New Private Key'")
            print("   - Save as 'firebase-adminsdk-key.json' in project root")
        
        if not all_packages_installed:
            print("\n3. Install missing packages:")
            print("   pip install -r requirements.txt")
        
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)