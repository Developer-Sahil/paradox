"""
Diagnostic script to test backend modules individually
Run with: python test_backend.py
"""

import sys
import traceback

def test_imports():
    """Test if all modules can be imported"""
    modules = [
        'backend.main',
        'backend.dependencies',
        'backend.models.post',
        'backend.models.product',
        'backend.models.project',
        'backend.models.metric',
        'backend.models.vault',
        'backend.models.arena',
        'backend.models.tool',
        'backend.models.admin',
        'backend.routers.main',
        'backend.routers.writings',
        'backend.routers.products',
        'backend.routers.projects',
        'backend.routers.systems',
        'backend.routers.vault',
        'backend.routers.arena',
        'backend.routers.metrics',
        'backend.routers.work',
        'backend.routers.admin',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except Exception as e:
            print(f"✗ {module}")
            print(f"  Error: {e}")
            failed.append((module, e))
    
    if failed:
        print("\n" + "="*60)
        print("FAILED IMPORTS - DETAILS:")
        print("="*60)
        for module, error in failed:
            print(f"\n{module}:")
            traceback.print_exception(type(error), error, error.__traceback__)
        return False
    else:
        print("\n✓ All modules imported successfully!")
        return True

def test_firebase():
    """Test Firebase connection"""
    try:
        from firebase_utils import get_firestore_client
        db = get_firestore_client()
        print("\n✓ Firebase connection successful!")
        print(f"  Database type: {type(db)}")
        return True
    except Exception as e:
        print("\n✗ Firebase connection failed!")
        print(f"  Error: {e}")
        traceback.print_exc()
        return False

def test_fastapi_app():
    """Test if FastAPI app can be created"""
    try:
        from backend.main import app
        print("\n✓ FastAPI app created successfully!")
        print(f"  Title: {app.title}")
        print(f"  Version: {app.version}")
        print(f"  Routes: {len(app.routes)}")
        
        # List all routes
        print("\n  Available routes:")
        for route in app.routes:
            if hasattr(route, 'path'):
                methods = getattr(route, 'methods', [])
                print(f"    {', '.join(methods):10} {route.path}")
        
        return True
    except Exception as e:
        print("\n✗ FastAPI app creation failed!")
        print(f"  Error: {e}")
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("BACKEND DIAGNOSTIC TEST")
    print("="*60)
    
    results = {
        'imports': test_imports(),
        'firebase': test_firebase(),
        'fastapi': test_fastapi_app()
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for test, passed in results.items():
        status = "PASSED ✓" if passed else "FAILED ✗"
        print(f"{test.upper():15} {status}")
    
    all_passed = all(results.values())
    print("="*60)
    
    if all_passed:
        print("\n✓ All tests passed! Backend should work correctly.")
        print("\nYou can now run:")
        print("  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n✗ Some tests failed. Fix the errors above before running the server.")
        sys.exit(1)

if __name__ == "__main__":
    main()