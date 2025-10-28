"""Test admin API endpoint"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# First login as admin
print("Logging in as admin...")
login_response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "lothar",
    "password": "Admin@123"
})

if login_response.status_code == 200:
    token = login_response.json()['access']
    print("✅ Login successful")
    
    # Test admin questions endpoint
    print("\nFetching admin questions...")
    headers = {"Authorization": f"Bearer {token}"}
    questions_response = requests.get(f"{BASE_URL}/admin/questions/", headers=headers)
    
    print(f"Status: {questions_response.status_code}")
    
    if questions_response.status_code == 200:
        data = questions_response.json()
        print(f"Response type: {type(data)}")
        
        if isinstance(data, dict):
            print(f"Keys: {data.keys()}")
            if 'results' in data:
                print(f"Questions count (paginated): {len(data['results'])}")
                print(f"Total count: {data.get('count', 'N/A')}")
            else:
                print(f"Response data: {data}")
        elif isinstance(data, list):
            print(f"Questions count (direct array): {len(data)}")
            if len(data) > 0:
                print(f"First question type: {data[0].get('question_type')}")
                print(f"Sample question: {data[0].get('text', '')[:50]}...")
        
        print("\n✅ API working correctly")
    else:
        print(f"❌ Failed: {questions_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
