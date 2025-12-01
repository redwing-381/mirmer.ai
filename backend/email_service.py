"""
Email service module for sending transactional emails via SendGrid.
Handles enterprise inquiries, notifications, and user alerts.
"""

import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from config import SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME, ADMIN_EMAIL

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending transactional emails using SendGrid."""
    
    def __init__(self):
        """Initialize the email service with SendGrid API key."""
        if not SENDGRID_API_KEY:
            logger.warning("SENDGRID_API_KEY not configured. Email sending will be disabled.")
            self.client = None
        else:
            self.client = SendGridAPIClient(SENDGRID_API_KEY)
        
        self.from_email = Email(SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME)
    
    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """
        Send an email using SendGrid.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML content of the email
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.client:
            logger.warning(f"Email service not configured. Would have sent email to {to_email}")
            return False
        
        try:
            to = To(to_email)
            content = Content("text/html", html_content)
            mail = Mail(self.from_email, to, subject, content)
            
            response = self.client.send(mail)
            
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}. Status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False
    
    def send_enterprise_inquiry_confirmation(self, email: str, name: str) -> bool:
        """
        Send confirmation email to enterprise inquiry submitter.
        
        Args:
            email: Submitter's email address
            name: Submitter's name
            
        Returns:
            True if email was sent successfully
        """
        subject = "Thank you for your interest in Mirmer AI Enterprise"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4ECDC4; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Mirmer AI</h1>
                </div>
                <div class="content">
                    <h2>Thank you for your interest!</h2>
                    <p>Hi {name},</p>
                    <p>Thank you for reaching out to us about Mirmer AI Enterprise. We've received your inquiry and our team will review it shortly.</p>
                    <p>A member of our sales team will contact you within 1-2 business days to discuss:</p>
                    <ul>
                        <li>Your specific use case and requirements</li>
                        <li>Custom pricing options</li>
                        <li>Enterprise features and capabilities</li>
                        <li>Implementation and onboarding process</li>
                    </ul>
                    <p>In the meantime, feel free to explore our platform and documentation.</p>
                    <a href="https://mirmer.ai" class="button">Visit Mirmer AI</a>
                    <p>If you have any urgent questions, please don't hesitate to reply to this email.</p>
                    <p>Best regards,<br>The Mirmer AI Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI. All rights reserved.</p>
                    <p>This is an automated message. Please do not reply directly to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(email, subject, html_content)
    
    def send_enterprise_inquiry_notification(
        self,
        name: str,
        email: str,
        company: str,
        company_size: str,
        phone: Optional[str],
        message: str,
        use_case: Optional[str]
    ) -> bool:
        """
        Send notification to admin team about new enterprise inquiry.
        
        Args:
            name: Submitter's name
            email: Submitter's email
            company: Company name
            company_size: Size of the company
            phone: Optional phone number
            message: Inquiry message
            use_case: Optional use case description
            
        Returns:
            True if email was sent successfully
        """
        subject = f"New Enterprise Inquiry from {company}"
        
        phone_html = f"<p><strong>Phone:</strong> {phone}</p>" if phone else ""
        use_case_html = f"<p><strong>Use Case:</strong> {use_case}</p>" if use_case else ""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #FF6B6B; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .info-box {{ background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #4ECDC4; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 New Enterprise Inquiry</h1>
                </div>
                <div class="content">
                    <h2>Contact Information</h2>
                    <div class="info-box">
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>Company:</strong> {company}</p>
                        <p><strong>Company Size:</strong> {company_size}</p>
                        {phone_html}
                    </div>
                    
                    <h2>Inquiry Details</h2>
                    <div class="info-box">
                        <p><strong>Message:</strong></p>
                        <p>{message}</p>
                        {use_case_html}
                    </div>
                    
                    <p><strong>Action Required:</strong> Please follow up with this inquiry within 1-2 business days.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI Admin Notification</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(ADMIN_EMAIL, subject, html_content)
    
    def send_subscription_expiry_reminder(self, user_email: str, days_remaining: int) -> bool:
        """
        Send reminder email about upcoming subscription expiry.
        
        Args:
            user_email: User's email address
            days_remaining: Number of days until expiry
            
        Returns:
            True if email was sent successfully
        """
        subject = f"Your Mirmer AI subscription expires in {days_remaining} days"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #FFD93D; color: #333; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Subscription Expiry Reminder</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>This is a friendly reminder that your Mirmer AI Pro subscription will expire in <strong>{days_remaining} days</strong>.</p>
                    <p>To continue enjoying unlimited access to our multi-LLM consultation system, please renew your subscription.</p>
                    <a href="https://mirmer.ai/settings" class="button">Renew Subscription</a>
                    <p>If you have any questions or need assistance, please don't hesitate to contact us.</p>
                    <p>Best regards,<br>The Mirmer AI Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def send_payment_failure_notification(self, user_email: str) -> bool:
        """
        Send notification about failed subscription payment.
        
        Args:
            user_email: User's email address
            
        Returns:
            True if email was sent successfully
        """
        subject = "Action Required: Payment Failed for Mirmer AI Subscription"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #FF6B6B; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 24px; background-color: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }
                .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Payment Failed</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>We were unable to process your subscription payment for Mirmer AI Pro.</p>
                    <p>This could be due to:</p>
                    <ul>
                        <li>Insufficient funds</li>
                        <li>Expired payment method</li>
                        <li>Bank security restrictions</li>
                    </ul>
                    <p>Please update your payment information to continue your subscription.</p>
                    <a href="https://mirmer.ai/settings" class="button">Update Payment Method</a>
                    <p>If you need assistance, please contact our support team.</p>
                    <p>Best regards,<br>The Mirmer AI Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def send_usage_limit_alert(self, user_email: str, percentage: int) -> bool:
        """
        Send alert when user reaches usage limit threshold.
        
        Args:
            user_email: User's email address
            percentage: Percentage of limit reached
            
        Returns:
            True if email was sent successfully
        """
        subject = f"You've used {percentage}% of your daily query limit"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #FFD93D; color: #333; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Usage Alert</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>You've used <strong>{percentage}%</strong> of your daily query limit on Mirmer AI.</p>
                    <p>To ensure uninterrupted access, consider upgrading to Pro for higher limits:</p>
                    <ul>
                        <li>100 queries per day (vs 10 on Free)</li>
                        <li>Priority support</li>
                        <li>Advanced features</li>
                    </ul>
                    <a href="https://mirmer.ai/settings" class="button">Upgrade to Pro</a>
                    <p>Your limit will reset at midnight UTC.</p>
                    <p>Best regards,<br>The Mirmer AI Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)
    
    def send_subscription_renewal_confirmation(self, user_email: str, receipt_url: Optional[str] = None) -> bool:
        """
        Send confirmation email for successful subscription renewal.
        
        Args:
            user_email: User's email address
            receipt_url: Optional URL to payment receipt
            
        Returns:
            True if email was sent successfully
        """
        subject = "Your Mirmer AI subscription has been renewed"
        
        receipt_html = f'<a href="{receipt_url}" class="button">View Receipt</a>' if receipt_url else ""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #6BCF7F; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #4ECDC4; color: white; text-decoration: none; border-radius: 4px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Subscription Renewed</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>Your Mirmer AI Pro subscription has been successfully renewed!</p>
                    <p>You can continue enjoying:</p>
                    <ul>
                        <li>100 queries per day</li>
                        <li>Access to all AI models</li>
                        <li>Priority support</li>
                        <li>Advanced features</li>
                    </ul>
                    {receipt_html}
                    <p>Thank you for being a valued member of Mirmer AI!</p>
                    <p>Best regards,<br>The Mirmer AI Team</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Mirmer AI. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(user_email, subject, html_content)


# Global email service instance
email_service = EmailService()
