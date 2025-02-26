from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
import pyotp

# ✅ Custom User Model with MFA (Two-Factor Authentication)
class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    mfa_secret = models.CharField(max_length=32, default=pyotp.random_base32)  # MFA Secret Key

    groups = models.ManyToManyField(Group, blank=True, related_name="user_profiles")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="user_profiles")




    def verify_mfa(self, otp_code):
        """Verify MFA OTP Code"""
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(otp_code)

    def __str__(self):
        return self.username


# ✅ Model to store detected intrusions
class Intrusion(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto set the timestamp
    ip_address = models.GenericIPAddressField()  # Stores the attacker's IP address
    threat_level = models.CharField(max_length=20, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ], default='Low')  # Defines the severity of the threat
    description = models.TextField()  # Detailed description of the attack

    def __str__(self):
        return f"Intrusion from {self.ip_address} - {self.threat_level} at {self.timestamp}"


# ✅ Model to store generated tickets for incidents
class Ticket(models.Model):
    intrusion = models.ForeignKey(Intrusion, on_delete=models.CASCADE)  # Links ticket to an intrusion
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the ticket is created
    status = models.CharField(max_length=20, choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed')
    ], default='Open')  # Status of the ticket
    resolution = models.TextField(blank=True, null=True)  # Stores resolution details if closed

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"


# ✅ Model to store uploaded files with validation
class UploadedFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Document File'),
        ('image', 'Image File'),
    ]

    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate file types"""
        valid_extensions = {
            'pdf': ['.pdf'],
            'doc': ['.csv', '.txt', '.docx'],
            'image': ['.jpg', '.jpeg', '.png'],
        }
        extension = self.file.name.split('.')[-1].lower()
        if not any(self.file.name.endswith(ext) for ext in valid_extensions[self.file_type]):
            raise ValidationError(f"Invalid file format for {self.file_type} files.")

    def __str__(self):
        return self.file.name
