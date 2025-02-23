import random
import requests
from django.conf import settings
from django.core.cache import cache  # To store OTP temporarily

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(phone_number):
    """Send OTP via Fast2SMS and store it in cache."""
    otp = generate_otp()
    message = f"Your OTP is {otp}. It is valid for 5 minutes."

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": phone_number
    }
    headers = {
        "authorization": settings.FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if data.get("return", False):
            cache.set(f"otp_{phone_number}", otp, timeout=300)  # Store OTP for 5 minutes
            return {"success": True, "message": "OTP sent successfully"}
        else:
            return {"success": False, "message": "Failed to send OTP"}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def verify_otp(phone_number, user_otp):
    """Verify if the entered OTP matches the stored one."""
    stored_otp = cache.get(f"otp_{phone_number}")

    if stored_otp and stored_otp == user_otp:
        cache.delete(f"otp_{phone_number}")  # Remove OTP after successful verification
        return {"success": True, "message": "OTP verified successfully"}
    else:
        return {"success": False, "message": "Invalid or expired OTP"}
