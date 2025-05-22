"""
Fix common issues with the Flask application.
"""
import os
import sys
import importlib
import subprocess

def check_python_path():
    """Check if the current directory is in PYTHONPATH."""
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        print(f"⚠️ Current directory not in PYTHONPATH. Adding {current_dir}")
        sys.path.insert(0, current_dir)
        return True
    else:
        print("✅ Current directory is in PYTHONPATH")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'sqlalchemy',
        'click',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is NOT installed")
    
    if missing_packages:
        print("\n⚠️ Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        return True
    else:
        print("✅ All required packages are installed")
        return False

def check_api_directory():
    """Check if the API directory exists and has all required files."""
    api_dir = os.path.join('crm_app', 'api')
    
    if not os.path.exists(api_dir):
        print(f"❌ API directory not found: {api_dir}")
        print("⚠️ Creating API directory...")
        os.makedirs(api_dir, exist_ok=True)
        return True
    else:
        print(f"✅ API directory exists: {api_dir}")
    
    required_files = ['__init__.py', 'customers.py', 'deals.py']
    missing_files = []
    
    for file in required_files:
        file_path = os.path.join(api_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
            print(f"❌ Missing file: {file_path}")
    
    if missing_files:
        print("⚠️ Some API files are missing. Please check the implementation.")
        return True
    else:
        print("✅ All API files exist")
        return False

def check_static_directory():
    """Check if the static directory exists and has all required subdirectories."""
    static_dir = os.path.join('crm_app', 'static')
    
    if not os.path.exists(static_dir):
        print(f"❌ Static directory not found: {static_dir}")
        print("⚠️ Creating static directory...")
        os.makedirs(static_dir, exist_ok=True)
        return True
    else:
        print(f"✅ Static directory exists: {static_dir}")
    
    required_dirs = ['css', 'js', 'images']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = os.path.join(static_dir, dir_name)
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)
            print(f"❌ Missing directory: {dir_path}")
            print(f"⚠️ Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    if missing_dirs:
        return True
    else:
        print("✅ All static subdirectories exist")
        return False

def check_logo_files():
    """Check if the logo files exist."""
    logo_paths = [
        os.path.join('crm_app', 'static', 'images', 'snake_logo.svg'),
        os.path.join('crm_app', 'static', 'images', 'snake_logo_small.svg')
    ]
    
    missing_logos = []
    
    for path in logo_paths:
        if not os.path.exists(path):
            missing_logos.append(path)
            print(f"❌ Missing logo file: {path}")
    
    if missing_logos:
        print("⚠️ Logo files are missing. Please check the implementation.")
        return True
    else:
        print("✅ All logo files exist")
        return False

def main():
    """Run all checks and fixes."""
    print("🔍 Running application checks and fixes...\n")
    
    fixed_python_path = check_python_path()
    fixed_dependencies = check_dependencies()
    fixed_api_dir = check_api_directory()
    fixed_static_dir = check_static_directory()
    fixed_logo_files = check_logo_files()
    
    if any([fixed_python_path, fixed_dependencies, fixed_api_dir, fixed_static_dir, fixed_logo_files]):
        print("\n⚠️ Some issues were fixed. Try running your application again.")
    else:
        print("\n✅ No issues found. Your application should be ready to run.")
    
    print("\nTo run your application, use:")
    print("cd /Users/carlos.cabrera/Desktop")
    print("source new_venv/bin/activate")
    print("python app.py")

if __name__ == "__main__":
    main()