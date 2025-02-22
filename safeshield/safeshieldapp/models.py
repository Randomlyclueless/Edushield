from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import pyotp

# Model to store detected intrusions
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


# Model to store generated tickets for incidents
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
from django.core.exceptions import ValidationError

# Model to store uploaded files
from django.db import models

class UploadedFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Document File'),
        ('image', 'Image File'),
    ]

    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
