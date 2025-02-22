import smtplib
from email.mime.text import MIMEText
import os

def send_intrusion_alert(ip_address, threat_level):
    """
    Sends an email alert when an intrusion is detected.

    :param ip_address: The suspicious IP address.
    :param threat_level: The severity of the detected intrusion.
    """
    sender_email = os.getenv("EMAIL_USER")  # Use environment variable
    receiver_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    sender_password = os.getenv("EMAIL_PASS")  # Use environment variable

    subject = "🚨 Intrusion Detected: High Alert!"
    message = f"""
    ⚠️ Intrusion Alert!
    IP Address: {ip_address}
    Threat Level: {threat_level}
    Immediate action is recommended.
    """

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("✅ Intrusion alert email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def block_ip(ip_address):
    """
    Blocks the given IP address using system firewall rules.

    :param ip_address: The suspicious IP address to block.
    """
    try:
        if os.name == "nt":  # Windows
            os.system(f"netsh advfirewall firewall add rule name='Block {ip_address}' dir=in action=block remoteip={ip_address}")
        else:  # Linux
            os.system(f"sudo iptables -A INPUT -s {ip_address} -j DROP")
        
        print(f"🚫 Blocked IP: {ip_address}")
    except Exception as e:
        print(f"❌ Error blocking IP: {e}")
