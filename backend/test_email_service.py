"""
Property-based tests for email service.

Feature: enterprise-features, Property 4: Confirmation emails are sent to submitters
Feature: enterprise-features, Property 5: Admin notifications are sent for new inquiries
Validates: Requirements 1.5, 1.6
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Strategy for generating valid email addresses
@st.composite
def email_addresses(draw):
    """Generate valid email addresses for testing."""
    local_part = draw(st.text(
        min_size=1,
        max_size=20,
        alphabet=st.characters(
            whitelist_categories=('Ll', 'Lu', 'Nd'),
            whitelist_characters='.-_'
        )
    ))
    # Ensure local part doesn't start/end with special chars
    local_part = local_part.strip('.-_')
    assume(len(local_part) > 0)
    
    domain = draw(st.text(
        min_size=1,
        max_size=20,
        alphabet=st.characters(
            whitelist_categories=('Ll', 'Lu', 'Nd'),
            whitelist_characters='-'
        )
    ))
    domain = domain.strip('-')
    assume(len(domain) > 0)
    
    tld = draw(st.sampled_from(['com', 'org', 'net', 'io', 'ai', 'co']))
    
    return f"{local_part}@{domain}.{tld}"


# Strategy for generating valid names
@st.composite
def person_names(draw):
    """Generate valid person names for testing."""
    name = draw(st.text(
        min_size=1,
        max_size=50,
        alphabet=st.characters(
            whitelist_categories=('Ll', 'Lu'),
            whitelist_characters=' -.'
        )
    ))
    name = name.strip()
    assume(len(name) > 0)
    return name


# Strategy for generating company names
@st.composite
def company_names(draw):
    """Generate valid company names for testing."""
    name = draw(st.text(
        min_size=1,
        max_size=100,
        alphabet=st.characters(
            whitelist_categories=('Ll', 'Lu', 'Nd'),
            whitelist_characters=' -.,&'
        )
    ))
    name = name.strip()
    assume(len(name) > 0)
    return name


class TestEnterpriseInquiryEmails:
    """
    Property-based tests for enterprise inquiry email functionality.
    
    **Feature: enterprise-features, Property 4: Confirmation emails are sent to submitters**
    **Feature: enterprise-features, Property 5: Admin notifications are sent for new inquiries**
    **Validates: Requirements 1.5, 1.6**
    """
    
    @given(
        email=email_addresses(),
        name=person_names()
    )
    @settings(max_examples=100)
    def test_confirmation_email_sent_to_submitter(self, email, name):
        """
        Property 4: For any valid enterprise inquiry submission with email and name,
        a confirmation email should be sent to the submitter's email address.
        
        This tests that confirmation emails are reliably sent to all submitters.
        """
        # Mock SendGrid client
        mock_sg_client = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 202  # SendGrid success code
        mock_sg_client.send.return_value = mock_response
        
        with patch('email_service.SENDGRID_API_KEY', 'test_api_key'):
            with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
                # Import after patching
                from email_service import EmailService
                
                # Create email service instance
                service = EmailService()
                
                # Send confirmation email
                result = service.send_enterprise_inquiry_confirmation(email, name)
                
                # Verify email was sent successfully
                assert result is True, "Confirmation email should be sent successfully"
                
                # Verify SendGrid client was called
                mock_sg_client.send.assert_called_once()
                
                # Get the Mail object that was sent
                call_args = mock_sg_client.send.call_args
                mail_obj = call_args[0][0]
                
                # Verify recipient email matches submitter
                assert mail_obj.personalizations[0].tos[0]['email'] == email, \
                    "Confirmation email should be sent to submitter's email"
                
                # Verify subject contains appropriate text
                subject_text = str(mail_obj.subject).lower()
                assert 'enterprise' in subject_text or 'thank' in subject_text, \
                    "Confirmation email should have appropriate subject"
                
                # Verify content contains submitter's name
                content_html = mail_obj.contents[0].content
                assert name in content_html, \
                    "Confirmation email should contain submitter's name"
    
    @given(
        submitter_name=person_names(),
        submitter_email=email_addresses(),
        company=company_names(),
        company_size=st.sampled_from(['1-10', '11-50', '51-200', '201-1000', '1000+']),
        message=st.text(min_size=10, max_size=500)
    )
    @settings(max_examples=100)
    def test_admin_notification_sent_for_inquiry(
        self,
        submitter_name,
        submitter_email,
        company,
        company_size,
        message
    ):
        """
        Property 5: For any valid enterprise inquiry, an admin notification email
        should be sent to the configured admin email address.
        
        This tests that admin notifications are reliably sent for all inquiries.
        """
        # Mock SendGrid client
        mock_sg_client = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 202  # SendGrid success code
        mock_sg_client.send.return_value = mock_response
        
        with patch('email_service.SENDGRID_API_KEY', 'test_api_key'):
            with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
                with patch('email_service.ADMIN_EMAIL', 'admin@test.com'):
                    # Import after patching
                    from email_service import EmailService
                    
                    # Create email service instance
                    service = EmailService()
                    
                    # Send admin notification
                    result = service.send_enterprise_inquiry_notification(
                        name=submitter_name,
                        email=submitter_email,
                        company=company,
                        company_size=company_size,
                        phone=None,
                        message=message,
                        use_case=None
                    )
                    
                    # Verify email was sent successfully
                    assert result is True, "Admin notification should be sent successfully"
                    
                    # Verify SendGrid client was called
                    mock_sg_client.send.assert_called_once()
                    
                    # Get the Mail object that was sent
                    call_args = mock_sg_client.send.call_args
                    mail_obj = call_args[0][0]
                    
                    # Verify recipient is admin email
                    assert mail_obj.personalizations[0].tos[0]['email'] == 'admin@test.com', \
                        "Admin notification should be sent to admin email"
                    
                    # Verify subject contains company name
                    assert company in str(mail_obj.subject), \
                        "Admin notification subject should contain company name"
                    
                    # Verify content contains all inquiry details
                    content_html = mail_obj.contents[0].content
                    assert submitter_name in content_html, \
                        "Admin notification should contain submitter name"
                    assert submitter_email in content_html, \
                        "Admin notification should contain submitter email"
                    assert company in content_html, \
                        "Admin notification should contain company name"
                    assert company_size in content_html, \
                        "Admin notification should contain company size"
                    assert message in content_html, \
                        "Admin notification should contain inquiry message"
    
    @given(
        email=email_addresses(),
        name=person_names()
    )
    @settings(max_examples=100)
    def test_confirmation_email_handles_sendgrid_errors(self, email, name):
        """
        Property: For any enterprise inquiry, if SendGrid fails to send the
        confirmation email, the service should handle the error gracefully
        and return False.
        
        This tests error handling for email sending failures.
        """
        # Mock SendGrid client to raise an exception
        mock_sg_client = MagicMock()
        mock_sg_client.send.side_effect = Exception("SendGrid API error")
        
        with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
            # Import after patching
            from email_service import EmailService
            
            # Create email service instance
            service = EmailService()
            
            # Attempt to send confirmation email
            result = service.send_enterprise_inquiry_confirmation(email, name)
            
            # Verify error was handled gracefully
            assert result is False, \
                "Email service should return False when SendGrid fails"
    
    @given(
        submitter_name=person_names(),
        submitter_email=email_addresses(),
        company=company_names(),
        company_size=st.sampled_from(['1-10', '11-50', '51-200', '201-1000', '1000+']),
        message=st.text(min_size=10, max_size=500),
        phone=st.one_of(st.none(), st.text(min_size=10, max_size=20, alphabet='0123456789+-() ')),
        use_case=st.one_of(st.none(), st.text(min_size=10, max_size=200))
    )
    @settings(max_examples=100)
    def test_admin_notification_includes_optional_fields(
        self,
        submitter_name,
        submitter_email,
        company,
        company_size,
        message,
        phone,
        use_case
    ):
        """
        Property: For any enterprise inquiry with optional fields (phone, use_case),
        the admin notification should include those fields when present.
        
        This tests that optional inquiry data is properly included in notifications.
        """
        # Mock SendGrid client
        mock_sg_client = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_client.send.return_value = mock_response
        
        with patch('email_service.SENDGRID_API_KEY', 'test_api_key'):
            with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
                with patch('email_service.ADMIN_EMAIL', 'admin@test.com'):
                    # Import after patching
                    from email_service import EmailService
                    
                    # Create email service instance
                    service = EmailService()
                    
                    # Send admin notification with optional fields
                    result = service.send_enterprise_inquiry_notification(
                        name=submitter_name,
                        email=submitter_email,
                        company=company,
                        company_size=company_size,
                        phone=phone,
                        message=message,
                        use_case=use_case
                    )
                    
                    # Verify email was sent
                    assert result is True
                    
                    # Get the Mail object
                    call_args = mock_sg_client.send.call_args
                    mail_obj = call_args[0][0]
                    content_html = mail_obj.contents[0].content
                    
                    # Verify optional fields are included when present
                    if phone:
                        assert phone in content_html, \
                            "Admin notification should include phone when provided"
                    
                    if use_case:
                        assert use_case in content_html, \
                            "Admin notification should include use case when provided"
    
    @given(
        email=email_addresses(),
        name=person_names()
    )
    @settings(max_examples=100)
    def test_email_service_without_api_key(self, email, name):
        """
        Property: For any email operation when SENDGRID_API_KEY is not configured,
        the email service should handle it gracefully and return False.
        
        This tests that the service works in development without SendGrid configured.
        """
        with patch('email_service.SENDGRID_API_KEY', None):
            # Import after patching
            from email_service import EmailService
            
            # Create email service instance (should not crash)
            service = EmailService()
            
            # Attempt to send email
            result = service.send_enterprise_inquiry_confirmation(email, name)
            
            # Verify it returns False gracefully
            assert result is False, \
                "Email service should return False when API key is not configured"


class TestNotificationEmails:
    """
    Property-based tests for other notification email functionality.
    """
    
    @given(
        user_email=email_addresses(),
        days_remaining=st.integers(min_value=1, max_value=30)
    )
    @settings(max_examples=100)
    def test_expiry_reminder_contains_days(self, user_email, days_remaining):
        """
        Property: For any subscription expiry reminder, the email should contain
        the number of days remaining.
        
        This tests that expiry reminders include the critical information.
        """
        # Mock SendGrid client
        mock_sg_client = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_client.send.return_value = mock_response
        
        with patch('email_service.SENDGRID_API_KEY', 'test_api_key'):
            with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
                from email_service import EmailService
                
                service = EmailService()
                result = service.send_subscription_expiry_reminder(user_email, days_remaining)
                
                assert result is True
                
                # Verify email contains days remaining
                call_args = mock_sg_client.send.call_args
                mail_obj = call_args[0][0]
                
                # Check subject
                assert str(days_remaining) in str(mail_obj.subject), \
                    "Expiry reminder subject should contain days remaining"
                
                # Check content
                content_html = mail_obj.contents[0].content
                assert str(days_remaining) in content_html, \
                    "Expiry reminder content should contain days remaining"
    
    @given(
        user_email=email_addresses(),
        percentage=st.integers(min_value=80, max_value=100)
    )
    @settings(max_examples=100)
    def test_usage_alert_contains_percentage(self, user_email, percentage):
        """
        Property: For any usage limit alert, the email should contain the
        percentage of limit reached.
        
        This tests that usage alerts include the usage percentage.
        """
        # Mock SendGrid client
        mock_sg_client = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 202
        mock_sg_client.send.return_value = mock_response
        
        with patch('email_service.SENDGRID_API_KEY', 'test_api_key'):
            with patch('email_service.SendGridAPIClient', return_value=mock_sg_client):
                from email_service import EmailService
                
                service = EmailService()
                result = service.send_usage_limit_alert(user_email, percentage)
                
                assert result is True
                
                # Verify email contains percentage
                call_args = mock_sg_client.send.call_args
                mail_obj = call_args[0][0]
                
                # Check subject
                assert str(percentage) in str(mail_obj.subject), \
                    "Usage alert subject should contain percentage"
                
                # Check content
                content_html = mail_obj.contents[0].content
                assert str(percentage) in content_html, \
                    "Usage alert content should contain percentage"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
