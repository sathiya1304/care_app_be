"""OTP service via Fast2SMS API — replaces sendOTP.php."""

import requests
from flask import current_app


def send_otp(mobile: str, otp: str) -> dict:
    """Send OTP via Fast2SMS. Returns the API response dict."""
    api_key = current_app.config.get("FAST2SMS_API_KEY", "")
    if not api_key:
        return {"error": "Fast2SMS API key not configured"}

    payload = {
        "sender_id": "CINGO",
        "message": otp,
        "variables_values": f"{otp}|",
        "route": "dlt",
        "numbers": mobile,
    }
    headers = {
        "authorization": api_key,
        "accept": "*/*",
        "cache-control": "no-cache",
        "content-type": "application/json",
    }
    try:
        resp = requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            json=payload,
            headers=headers,
            timeout=30,
        )
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}
