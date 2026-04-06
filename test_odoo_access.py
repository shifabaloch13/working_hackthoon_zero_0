"""Test if Odoo is accessible"""
import requests
import time

print("Waiting for Odoo to start...")
print("=" * 60)

for i in range(10):
    try:
        response = requests.get("http://localhost:8069", timeout=5)
        print(f"Attempt {i+1}: Status {response.status_code}")
        if response.status_code == 200:
            print("✅ Odoo is accessible!")
            break
    except requests.exceptions.ConnectionError:
        print(f"Attempt {i+1}: Connection refused, waiting...")
    except requests.exceptions.Timeout:
        print(f"Attempt {i+1}: Timeout, Odoo is still loading...")
    except Exception as e:
        print(f"Attempt {i+1}: Error - {e}")
    
    time.sleep(5)

print("=" * 60)
