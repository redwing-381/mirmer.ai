# Enterprise Contact Form Setup

## Overview

The enterprise contact form allows potential customers to reach out for custom pricing and enterprise features directly from the pricing page.

## How It Works

1. **User clicks "Contact Sales"** on the Enterprise pricing card
2. **Modal opens** with a contact form
3. **User fills out** required information (name, email, company, etc.)
4. **Form submits** to `/api/enterprise/contact`
5. **Two emails are sent**:
   - Confirmation email to the submitter
   - Notification email to admin (configured in `.env`)

## Configuration

Make sure your `.env` file has the following SendGrid configuration:

```bash
# Email Service Configuration (SendGrid)
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
SENDGRID_FROM_NAME=Mirmer AI
ADMIN_EMAIL=your-admin-email@yourdomain.com
```

### Getting SendGrid API Key

1. Sign up at [SendGrid.com](https://sendgrid.com/) (free tier: 100 emails/day)
2. Go to Settings → API Keys
3. Create a new API key with "Full Access"
4. Copy the key and add it to your `.env` file

### Verify Sender Email

Before sending emails, verify your sender email in SendGrid:

1. Go to Settings → Sender Authentication
2. Click "Verify a Single Sender"
3. Fill in your details and verify the email
4. Use this verified email as `SENDGRID_FROM_EMAIL`

## Testing

### Test the Email Service

```bash
cd backend
uv run python test_sendgrid.py
```

This will send a test email to verify SendGrid is configured correctly.

### Test the Contact Form

1. Start the backend: `cd backend && uv run uvicorn main:app --reload --port 8001`
2. Start the frontend: `cd frontend && npm run dev`
3. Navigate to the landing page
4. Scroll to the pricing section
5. Click "Contact Sales" on the Enterprise card
6. Fill out and submit the form
7. Check your email for the confirmation

## Form Fields

### Required Fields
- **Name**: Contact person's name
- **Email**: Contact email address
- **Company**: Company name
- **Company Size**: Dropdown selection (1-10, 11-50, 51-200, 201-1000, 1000+)
- **Message**: Inquiry details

### Optional Fields
- **Phone**: Contact phone number
- **Use Case**: How they plan to use Mirmer AI

## Email Templates

### Confirmation Email (to submitter)
- Subject: "Thank you for your interest in Mirmer AI Enterprise"
- Contains: Welcome message, what to expect, timeline for response

### Admin Notification (to admin)
- Subject: "New Enterprise Inquiry from [Company Name]"
- Contains: All form details, contact information, inquiry message

## Troubleshooting

### Emails not sending?

1. Check if `SENDGRID_API_KEY` is set in `.env`
2. Verify sender email in SendGrid dashboard
3. Check backend logs for errors
4. Test with `test_sendgrid.py`

### Form not submitting?

1. Check browser console for errors
2. Verify backend is running on port 8001
3. Check network tab for API response
4. Verify CORS is configured correctly

## Production Checklist

- [ ] SendGrid API key configured
- [ ] Sender email verified in SendGrid
- [ ] Admin email set to correct address
- [ ] Test form submission end-to-end
- [ ] Check spam folder for test emails
- [ ] Monitor SendGrid dashboard for delivery rates
- [ ] Set up domain authentication (recommended)

## Next Steps

After receiving an enterprise inquiry:

1. Admin receives notification email
2. Review inquiry details
3. Respond within 1-2 business days (as promised in confirmation email)
4. Follow up with custom pricing and demo

## Support

For issues with the contact form or email delivery, check:
- Backend logs: `backend/main.py` logs
- SendGrid Activity Feed: SendGrid Dashboard → Activity
- Email service logs: `backend/email_service.py` logs
