"""Synthetic examples for demonstrating the Phase 0 prototype.

The examples are fictional and should not be treated as real reports or customer data.
"""

SAMPLE_MESSAGES = {
    "Neutral business note": {
        "message": (
            "Hello, the draft agenda for tomorrow's supplier meeting is ready. "
            "Please review it when convenient and send comments before 3 p.m."
        ),
        "url": "",
    },
    "Changed payment details": {
        "message": (
            "URGENT: I am the supplier account manager. Our bank account number has changed. "
            "Transfer today's invoice immediately to the new account and do not call the office."
        ),
        "url": "",
    },
    "OTP request": {
        "message": (
            "This is customer care. Your wallet will be suspended today. "
            "Reply with the OTP and PIN you just received so we can verify your account."
        ),
        "url": "",
    },
    "Suspicious verification link": {
        "message": (
            "Final warning! Verify your payment account now using the secure link below."
        ),
        "url": "https://secure-login-verify-account.example.com/update",
    },
    "Raw IP address": {
        "message": "Open the portal below and sign in before the invoice can be released.",
        "url": "http://192.0.2.10/verify",
    },
}
