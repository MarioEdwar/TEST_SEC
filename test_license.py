import requests

SERVER = "https://attractive-charisma-production.up.railway.app"
PASSWORD = "MY_SECRET_PASSWORD"

# ==============================
# 1. إضافة عميل جديد
# ==============================
print("بنضيف عميل جديد...")
response = requests.post(f"{SERVER}/add", json={
    "password": PASSWORD,
    "license_key": "CLIENT001",
    "client_name": "عميل تجريبي",
    "expiry": "2026-12-31"
})
print("النتيجة:", response.json())

# ==============================
# 2. التحقق من العميل
# ==============================
print("\nبنتحقق من اللايسنس...")
response = requests.post(f"{SERVER}/check", json={
    "license_key": "CLIENT001"
})
print("النتيجة:", response.json())