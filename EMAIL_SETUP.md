# Email Configuration Guide for LaunchConnect

## Quick Start: Development (Console Backend)

By default, the application uses Django's console email backend in development. This means emails will print to the terminal/console instead of being actually sent.

**No configuration needed!** Just run your server and emails will appear in the console.

---

## Option 1: Gmail SMTP (Recommended for Testing)

### Setup Steps:

1. **Enable 2-Factor Authentication on Gmail:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification if not already enabled

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password
   - Copy this password (you'll need it)

3. **Update `.env` file:**
```
USE_SMTP=true
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

4. **Restart Django server:**
```bash
python manage.py runserver
```

Now emails will be sent via Gmail SMTP!

---

## Option 2: SendGrid (Production Ready)

### Setup Steps:

1. **Sign up for SendGrid:**
   - Go to https://sendgrid.com
   - Create free account

2. **Get API Key:**
   - Log in to SendGrid dashboard
   - Go to Settings → API Keys
   - Create new API key
   - Copy the key

3. **Install SendGrid Django package:**
```bash
pip install sendgrid-django
```

4. **Update `.env` file:**
```
USE_SMTP=true
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=SG.xxxxx...
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

5. **Add to `requirements.txt`:**
```
sendgrid-django
```

---

## Option 3: AWS SES (Scalable Production)

### Setup Steps:

1. **Create AWS Account and verify email:**
   - Go to AWS Console
   - Navigate to Simple Email Service (SES)
   - Verify your sender email address

2. **Create IAM credentials:**
   - Go to IAM → Users
   - Create new user with SES permissions
   - Generate access keys

3. **Install django-ses:**
```bash
pip install django-ses
```

4. **Update `.env` file:**
```
EMAIL_BACKEND=django_ses.SESBackend
AWS_SES_REGION_NAME=us-east-1
AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

## Option 4: Mailgun (Simple Production)

### Setup Steps:

1. **Sign up for Mailgun:**
   - Go to https://www.mailgun.com
   - Create free account

2. **Get credentials from dashboard:**
   - Domain
   - API key

3. **Install django-mailgun:**
```bash
pip install django-mailgun
```

4. **Update `.env` file:**
```
EMAIL_BACKEND=django_mailgun.MailgunBackend
MAILGUN_ACCESS_KEY=key-xxxxx
MAILGUN_SERVER_NAME=mg.your-domain.com
DEFAULT_FROM_EMAIL=noreply@your-domain.com
```

---

## Testing Email Verification in Development

### Using Gmail SMTP:

1. **Add temporary print statement in `users/views.py`:**

```python
def send_verification_email(user, request):
    token = str(uuid.uuid4())
    user.email_verification_token = token
    user.save()
    
    verification_link = request.build_absolute_uri(f'/verify-email/{token}/')
    
    # For development - Print to console
    print(f"\n{'='*80}")
    print(f"Email Verification Link for {user.email}:")
    print(f"{verification_link}")
    print(f"{'='*80}\n")
    
    # Send actual email
    send_mail(...)
```

2. **Register a user:**
   - Go to `/register/`
   - Fill in form with test email
   - Check console/terminal for verification link
   - Click link to verify

---

## Testing Commands

### Test email configuration: ```bash
python manage.py shell
```

Then in the shell:
```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body',
    'your-email@gmail.com',  # From email
    ['recipient@example.com'],  # To email
    fail_silently=False,
)
```

If no errors, your email is configured correctly!

---

## Production Checklist

- [ ] Change `DEBUG=False` in `.env`
- [ ] Update `SECRET_KEY` to a strong random value
- [ ] Use SendGrid, AWS SES, or Mailgun (not Gmail)
- [ ] Set up proper domain for emails
- [ ] Add ALLOWEDHOST domains
- [ ] Enable HTTPS only
- [ ] Set up email bounce handling
- [ ] Monitor email delivery rates

---

## Troubleshooting

### Gmail says "Less secure app access"
- This message is outdated
- You MUST use App Passwords (16-character), not your regular password

### "CommandError: SMTP auth extension not supported by server"
- Check `EMAIL_USE_TLS=true` is set
- Verify `EMAIL_PORT=587` (not 25 or 465)

### Emails not being sent
- Verify `.env` file is loaded: Check Django console at startup
- Send test email using Django shell command above
- Check spam/junk folder

### "SMTPAuthenticationError: Invalid credentials"
- Verify your email and app password
- For Gmail: Use 16-char app password, not your regular password

---

## Next Steps

1. Choose email provider above
2. Update `.env` file with credentials
3. Restart Django server
4. Test by registering a user
5. Check that verification email is sent
6. Click verification link to complete setup

Happy coding! 🚀
