# backend/test_sendgrid.py
from email_service import email_service

# Test sending a confirmation email
result = email_service.send_enterprise_inquiry_confirmation(
    email="solaimuthu006@gmail.com",
    name="Test User"
)

print(f"Email sent: {result}")
