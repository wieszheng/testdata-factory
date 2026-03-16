import requests
import json

# Test 1: Simple request
data = {
    "count": 1,
    "types": ["phone"],
    "custom_rules": [
        {"name": "test", "pattern": r"\d{3}"}
    ]
}

print("Sending:", json.dumps(data))
r = requests.post('http://localhost:8003/api/generate', json=data)
print("Response:", r.json())
