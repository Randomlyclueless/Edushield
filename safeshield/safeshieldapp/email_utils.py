from django.core.mail import send_mail
from django.conf import settings

def send_access_email(user_email):
    """Function to send email when someone accesses Safespace."""
    subject = "Access to Safespace"
    message = f"Hello,\n\nThis is a notification that {user_email} has accessed Safespace."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]  # You can send it to a list of recipients if needed

    send_mail(subject, message, from_email, recipient_list)
