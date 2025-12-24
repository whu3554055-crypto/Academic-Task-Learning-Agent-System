"""
Windows Compatibility Test Script for ATLAS

Run this script to verify your Windows environment is properly configured.
"""

import sys
import os
import platform
from pathlib import Path

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_result(test_name, passed, details=""):
    """Print test result with color coding."""
    status = "[PASS]" if passed else "[FAIL]"
    color_code = "\033[92m" if passed else "\033[91m"  # Green or Red
    reset_code = "\033[0m"

    print(f"{color_code}{status}{reset_code} - {test_name}")
    if details:
        print(f"       {details}")

def test_python_version():
    """Test Python version."""
    print_section("Python Version Check")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Current version: {version_str}")
    
    passed = version.major >= 3 and version.minor >= 9
    print_result("Python 3.9+ required", passed, 
                f"Found: {version_str}")
    return passed

def test_platform():
    """Test platform detection."""
    print_section("Platform Detection")
    system = platform.system()
    print(f"Operating System: {system}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    passed = system in ["Windows", "Linux", "Darwin"]
    print_result("Supported platform", passed, system)
    return passed

def test_asyncio_support():
    """Test asyncio support."""
    print_section("Asyncio Support")
    try:
        import asyncio
        
        # Test event loop policy on Windows
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            print("WindowsSelectorEventLoopPolicy set successfully")
        
        # Create a simple async test
        async def test():
            return True
        
        result = asyncio.run(test())
        print_result("Async/await functionality", result)
        return result
    except Exception as e:
        print_result("Async/await functionality", False, str(e))
        return False

def test_dependencies():
    """Test required dependencies."""
    print_section("Dependencies Check")
    
    dependencies = [
        ("langgraph", "LangGraph framework"),
        ("openai", "OpenAI client"),
        ("pydantic", "Pydantic models"),
        ("dotenv", "Environment variables"),
        ("rich", "Rich console output"),
    ]
    
    all_passed = True
    for module_name, description in dependencies:
        try:
            __import__(module_name.replace("-", "_"))
            print_result(description, True)
        except ImportError as e:
            print_result(description, False, f"Install with: pip install {module_name}")
            all_passed = False
    
    return all_passed

def test_file_paths():
    """Test file path handling."""
    print_section("File Path Handling")
    
    try:
        # Test Path operations
        current_dir = Path(__file__).parent.resolve()
        data_dir = current_dir / "data"
        
        print(f"Project directory: {current_dir}")
        print(f"Data directory: {data_dir}")
        
        # Check if directories exist
        print_result("Project directory exists", current_dir.exists())
        print_result("Data directory exists", data_dir.exists())
        
        # Check sample files
        sample_files = ["profile.json", "calendar.json", "task.json"]
        files_exist = True
        for filename in sample_files:
            filepath = data_dir / filename
            exists = filepath.exists()
            print_result(f"Sample file: {filename}", exists)
            if not exists:
                files_exist = False
        
        return files_exist
    except Exception as e:
        print_result("File path operations", False, str(e))
        return False

def test_env_file():
    """Test environment file."""
    print_section("Environment Configuration")
    
    env_path = Path(__file__).parent / ".env"
    env_example_path = Path(__file__).parent / ".env.example"
    
    print_result(".env.example exists", env_example_path.exists())
    
    if env_path.exists():
        print_result(".env file exists", True)
        
        # Check if API key is set
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY", "")
            
            if api_key and api_key != "your_api_key_here":
                print_result("API key configured", True, "Key found (hidden)")
                return True
            else:
                print_result("API key configured", False, 
                           "Edit .env and add your API key")
                return False
        except Exception as e:
            print_result("Environment loading", False, str(e))
            return False
    else:
        print_result(".env file exists", False, 
                   "Copy .env.example to .env and configure")
        return False

def test_encoding():
    """Test UTF-8 encoding support."""
    print_section("Encoding Support")
    
    try:
        # Test UTF-8 string handling
        test_string = "ATLAS - 学术助手 - Академический помощник"
        encoded = test_string.encode('utf-8')
        decoded = encoded.decode('utf-8')
        
        passed = test_string == decoded
        print_result("UTF-8 encoding/decoding", passed)
        
        if passed:
            print(f"       Test string: {test_string}")
        
        return passed
    except Exception as e:
        print_result("UTF-8 encoding/decoding", False, str(e))
        return False

def main():
    """Run all compatibility tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "ATLAS Windows Compatibility Test Suite" + " " * 12 + "║")
    print("╚" + "═" * 58 + "╝")
    
    tests = [
        ("Platform Detection", test_platform),
        ("Python Version", test_python_version),
        ("Asyncio Support", test_asyncio_support),
        ("Dependencies", test_dependencies),
        ("File Paths", test_file_paths),
        ("Environment Config", test_env_file),
        ("Encoding Support", test_encoding),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] in {test_name}: {e}")
            results.append((test_name, False))

    # Summary
    print_section("Test Summary")

    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)

    for test_name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print("\n" + "-" * 60)
    print(f"Total: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\nAll tests passed! Your system is ready for ATLAS.")
        print("\nNext steps:")
        print("  1. Run: run.bat (or python main.py)")
        print("  2. Enter your academic request")
        print("  3. Get personalized assistance!")
    else:
        print("\nWARNING: Some tests failed. Please fix the issues above.")
        print("\nHelpful resources:")
        print("  - See WINDOWS_TROUBLESHOOTING.md for solutions")
        print("  - Try running: run.bat for automatic setup")

    print("=" * 60 + "\n")

    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
