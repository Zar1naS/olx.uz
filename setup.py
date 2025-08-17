#!/usr/bin/env python3
"""
Setup script for OLX.uz Django project

This script helps you set up the project quickly by:
1. Installing required packages
2. Running migrations
3. Creating initial data
4. Creating a superuser (optional)
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up OLX.uz Django Project")
    print("=" * 50)
    
    # Check if Python is available
    try:
        import django
        print(f"✅ Django {django.get_version()} found")
    except ImportError:
        print("❌ Django not found. Please install it first:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    # Populate initial data
    if not run_command("python manage.py populate_data", "Populating initial data"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the development server: python manage.py runserver")
    print("3. Visit http://127.0.0.1:8000 to see your site")
    print("4. Admin panel: http://127.0.0.1:8000/admin")
    print("\n📋 Demo credentials:")
    print("Username: demo_user")
    print("Password: demo123")
    
    # Ask if user wants to create a superuser
    create_super = input("\n🤔 Do you want to create a superuser now? (y/n): ").lower().strip()
    if create_super in ['y', 'yes']:
        subprocess.run("python manage.py createsuperuser", shell=True)
    
    print("\n🎊 All done! Your OLX.uz clone is ready to use!")

if __name__ == "__main__":
    main()
