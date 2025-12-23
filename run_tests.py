#!/usr/bin/env python3
"""
Simple test runner for the FastAPI application
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from fastapi.testclient import TestClient
    from app import app

    def run_tests():
        client = TestClient(app)

        print("Running FastAPI tests...")

        # Test 1: Get activities
        print("Test 1: GET /activities")
        response = client.get("/activities")
        if response.status_code == 200:
            activities = response.json()
            print(f"✓ Found {len(activities)} activities")
        else:
            print(f"✗ Failed with status {response.status_code}")

        # Test 2: Signup
        print("Test 2: POST /activities/Basketball Team/signup")
        response = client.post("/activities/Basketball Team/signup", params={"email": "pytest@test.com"})
        if response.status_code == 200:
            print("✓ Signup successful")
        else:
            result = response.json()
            print(f"Response: {result}")

        # Test 3: Unregister
        print("Test 3: DELETE /activities/Art Club/unregister")
        response = client.delete("/activities/Art Club/unregister", params={"email": "lucas@mergington.edu"})
        if response.status_code == 200:
            print("✓ Unregister successful")
        else:
            result = response.json()
            print(f"Response: {result}")

        # Test 4: Error case - non-existent activity
        print("Test 4: POST /activities/NonExistent/signup")
        response = client.post("/activities/NonExistent/signup", params={"email": "test@test.com"})
        if response.status_code == 404:
            print("✓ Error handling works for non-existent activity")
        else:
            print(f"✗ Expected 404, got {response.status_code}")

        print("Basic tests completed!")

    if __name__ == "__main__":
        run_tests()

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure FastAPI and dependencies are installed")
    sys.exit(1)