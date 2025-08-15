#!/usr/bin/env python3
"""
Setup script for OpenFDA Drug Data Analysis project
"""

import os
import sys
import subprocess


def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        "Data Source",
        "plots",
        "example_plots",
        "output"
    ]
    
    print("Creating directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")


def run_tests():
    """Run the test suite"""
    print("\nRunning tests...")
    try:
        subprocess.check_call([sys.executable, "test_openfda_analysis.py"])
        print("✓ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Some tests failed: {e}")
        return False


def run_example():
    """Run the example script"""
    print("\nRunning example analysis...")
    try:
        subprocess.check_call([sys.executable, "example_usage.py"])
        print("✓ Example analysis completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Example analysis failed: {e}")
        return False


def check_data_files():
    """Check if OpenFDA data files are available"""
    data_dir = "Data Source"
    expected_files = [f"drug-label-{i:04d}-of-0009.json" for i in range(1, 10)]
    
    print(f"\nChecking for OpenFDA data files in '{data_dir}'...")
    
    if not os.path.exists(data_dir):
        print(f"✗ Data directory '{data_dir}' not found")
        return False
    
    missing_files = []
    for file_name in expected_files:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            missing_files.append(file_name)
    
    if missing_files:
        print(f"✗ Missing {len(missing_files)} data files:")
        for file_name in missing_files[:3]:  # Show first 3
            print(f"   - {file_name}")
        if len(missing_files) > 3:
            print(f"   ... and {len(missing_files) - 3} more")
        print("\nNote: You can still run the example script with synthetic data")
        return False
    else:
        print("✓ All OpenFDA data files found")
        return True


def main():
    """Main setup function"""
    print("OpenFDA Drug Data Analysis - Setup Script")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("\nSetup failed at requirements installation")
        return False
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Check for data files
    data_available = check_data_files()
    
    # Step 4: Run tests
    if not run_tests():
        print("\nWarning: Some tests failed, but setup will continue")
    
    # Step 5: Run example (optional)
    print("\nWould you like to run the example analysis? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            run_example()
    except KeyboardInterrupt:
        print("\nSkipping example analysis")
    
    # Final summary
    print("\n" + "=" * 50)
    print("Setup Summary:")
    print("✓ Python packages installed")
    print("✓ Directories created")
    print("✓ Tests executed")
    
    if data_available:
        print("✓ OpenFDA data files found")
        print("\nYou can now run:")
        print("  - jupyter notebook OpenFDA_DrugEndPointAnalysis.ipynb")
        print("  - python example_usage.py")
    else:
        print("! OpenFDA data files not found")
        print("\nYou can still run:")
        print("  - python example_usage.py (uses synthetic data)")
        print("  - Download OpenFDA data files to 'Data Source' directory")
    
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()