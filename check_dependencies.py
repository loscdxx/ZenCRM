"""
Check if all required dependencies are installed.
"""
import importlib
import sys

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
        importlib.import_module(package)
        print(f"✅ {package} is installed")
    except ImportError:
        missing_packages.append(package)
        print(f"❌ {package} is NOT installed")

if missing_packages:
    print("\n⚠️ Missing packages detected. Install them with:")
    print(f"pip install {' '.join(missing_packages)}")
else:
    print("\n✅ All required packages are installed")