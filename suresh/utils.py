from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_notification_email(user, subject, template, context=None):
    if not user.settings.email_notifications:
        return False
    
    if context is None:
        context = {}
    context['user'] = user
    
    # Render HTML content
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False 