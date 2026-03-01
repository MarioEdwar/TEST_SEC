from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# ملف بيخزن بيانات العملاء
LICENSES_FILE = "licenses.json"

# لو الملف مش موجود، نعمله
if not os.path.exists(LICENSES_FILE):
    with open(LICENSES_FILE, "w") as f:
        json.dump({}, f)


def load_licenses():
    with open(LICENSES_FILE, "r") as f:
        return json.load(f)


def save_licenses(data):
    with open(LICENSES_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ===============================
# نقطة التحقق - البرنامج بيسأل هنا
# ===============================
@app.route("/check", methods=["POST"])
def check_license():
    data = request.json
    key = data.get("license_key")

    if not key:
        return jsonify({"status": "invalid", "message": "مفيش license key"}), 400

    licenses = load_licenses()

    if key not in licenses:
        return jsonify({"status": "invalid", "message": "الكود ده مش موجود"}), 404

    license = licenses[key]

    # لو متوقف يدوياً
    if not license.get("active", True):
        return jsonify({"status": "blocked", "message": "اللايسنس اتوقف"}), 403

    # لو عنده تاريخ انتهاء
    expiry = license.get("expiry")
    if expiry:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        if datetime.now() > expiry_date:
            return jsonify({"status": "expired", "message": "اللايسنس انتهى"}), 403

    return jsonify({"status": "valid", "message": "شغال تمام"}), 200


# ===============================
# إضافة عميل جديد
# ===============================
@app.route("/add", methods=["POST"])
def add_license():
    data = request.json
    admin_password = data.get("password")

    # باسورد المدير - غيره لباسورد خاص بيك
    if admin_password != "MY_SECRET_PASSWORD":
        return jsonify({"message": "مش مسموح"}), 403

    key = data.get("license_key")
    expiry = data.get("expiry")  # مثال: "2025-12-31"
    client_name = data.get("client_name", "")

    if not key:
        return jsonify({"message": "لازم تبعت license_key"}), 400

    licenses = load_licenses()
    licenses[key] = {
        "client_name": client_name,
        "expiry": expiry,
        "active": True,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    save_licenses(licenses)

    return jsonify({"message": "اتضاف بنجاح", "key": key}), 200


# ===============================
# إيقاف عميل
# ===============================
@app.route("/block", methods=["POST"])
def block_license():
    data = request.json
    if data.get("password") != "MY_SECRET_PASSWORD":
        return jsonify({"message": "مش مسموح"}), 403

    key = data.get("license_key")
    licenses = load_licenses()

    if key not in licenses:
        return jsonify({"message": "مش موجود"}), 404

    licenses[key]["active"] = False
    save_licenses(licenses)

    return jsonify({"message": "اتوقف بنجاح"}), 200


# ===============================
# تفعيل عميل تاني
# ===============================
@app.route("/unblock", methods=["POST"])
def unblock_license():
    data = request.json
    if data.get("password") != "MY_SECRET_PASSWORD":
        return jsonify({"message": "مش مسموح"}), 403

    key = data.get("license_key")
    licenses = load_licenses()

    if key not in licenses:
        return jsonify({"message": "مش موجود"}), 404

    licenses[key]["active"] = True
    save_licenses(licenses)

    return jsonify({"message": "اتفعّل بنجاح"}), 200


# ===============================
# عرض كل العملاء
# ===============================
@app.route("/list", methods=["POST"])
def list_licenses():
    data = request.json
    if data.get("password") != "MY_SECRET_PASSWORD":
        return jsonify({"message": "مش مسموح"}), 403

    licenses = load_licenses()
    return jsonify(licenses), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
