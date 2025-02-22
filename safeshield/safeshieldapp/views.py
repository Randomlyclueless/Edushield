from django.shortcuts import render
from django.http import JsonResponse
import joblib
import numpy as np
from .models import Ticket
from .utils import send_intrusion_alert, block_ip
model = joblib.load(r"C:\Users\SAINATH\OneDrive\saipython\Pictures\Documents\GitHub\Edushield\safeshield\model\random_forest_model.pkl")
def detect_intrusion(request):
    if request.method == 'POST':
        # Extract data from request
        data = request.POST.getlist('features')  # Example format
        features = np.array(data, dtype=np.float32).reshape(1, -1)

        # Predict using AI Model
        prediction = model.predict(features)[0]  # Get single prediction

        if prediction != 0:  # Attack detected
            attack_type = f"Attack Type {prediction}"
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

            # Create a security ticket
            ticket = Ticket.objects.create(
                description="Suspicious activity detected",
                severity="High",
                status="Open",
                attack_type=attack_type,
                ip_address=ip_address
            )

            # Send Email Alert
            send_intrusion_alert(ticket.id, attack_type, ip_address)

            # Block Attacker IP
            block_ip(ip_address)

            return JsonResponse({'message': '🚨 Intrusion detected!', 'ticket_id': ticket.id})

        return JsonResponse({'message': '✅ No threats detected'})



# Create your views here.
def home(request):
    return render(request, 'home.html')