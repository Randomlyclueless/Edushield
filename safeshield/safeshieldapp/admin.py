from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Intrusion, Ticket

admin.site.register(Intrusion)
admin.site.register(Ticket)

