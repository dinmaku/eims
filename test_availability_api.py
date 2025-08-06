#!/usr/bin/env python3

import requests
import json

# Test the availability API endpoints
BASE_URL = "http://127.0.0.1:5001"

def test_availability_api():
    print("Testing Availability API...")
    
    # Test 1: Check if the endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/api/supplier/availability")
        print(f"GET /api/supplier/availability - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists but requires authentication (expected)")
        elif response.status_code == 200:
            print("✅ Endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing GET endpoint: {e}")
    
    # Test 2: Check if the table exists by trying to create a test record
    test_data = {
        "date": "2025-01-15",
        "is_available": False,
        "reason": "Test unavailability"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/supplier/availability", 
                               json=test_data,
                               headers={"Content-Type": "application/json"})
        print(f"POST /api/supplier/availability - Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists but requires authentication (expected)")
        elif response.status_code == 200:
            print("✅ Endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing POST endpoint: {e}")

if __name__ == "__main__":
    test_availability_api() 