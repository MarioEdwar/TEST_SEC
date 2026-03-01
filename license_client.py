import requests
import sys
import os

# ضع هنا رابط السيرفر بتاعك بعد ما ترفعه
SERVER_URL = "https://YOUR_SERVER_URL/check"

# المفتاح الخاص بالعميل ده - كل عميل عنده مفتاح مختلف
LICENSE_KEY = "CLIENT_KEY_HERE"


def check_license():
    try:
        response = requests.post(SERVER_URL, json={"license_key": LICENSE_KEY}, timeout=10)
        data = response.json()

        if data.get("status") == "valid":
            return True
        else:
            print("البرنامج مش مفعّل:", data.get("message"))
            return False

    except Exception:
        # لو مش قادر يوصل للسيرفر
        print("مش قادر يتحقق من اللايسنس، تأكد من النت")
        return False


def protect():
    if not check_license():
        print("البرنامج هيقفل دلوقتي.")
        sys.exit(1)  # البرنامج بيقفل


# =============================
# استخدمها في أول سطر في برنامجك
# =============================
if __name__ == "__main__":
    protect()
    print("البرنامج شغال تمام ✅")
    # باقي كود البرنامج هنا
