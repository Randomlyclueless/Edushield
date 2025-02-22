from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
import joblib
import numpy as np
import json
from .models import Ticket
from .utils import send_intrusion_alert, block_ip
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings

# ✅ Load the AI model once at startup
MODEL_PATH = r"D:\Python projects\Edushield\safeshield\model\safeshiel_model.pkl"
model = joblib.load(MODEL_PATH)

def detect_intrusion(request):
    if request.method == 'POST':
        try:
            # ✅ Parse JSON data from request
            data = json.loads(request.body.decode('utf-8'))
            features = data.get("features", [])

            # ✅ Validate input features
            if not features or not isinstance(features, list):
                return JsonResponse({'error': 'Invalid input: Features must be a list'}, status=400)

            features = np.array(features, dtype=np.float32).reshape(1, -1)

            # ✅ Predict using AI Model
            prediction = model.predict(features)[0]  # Get single prediction

            if prediction != 0:  # Attack detected
                attack_type = f"Attack Type {prediction}"
                ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

                # ✅ Create a security ticket
                ticket = Ticket.objects.create(
                    description="Suspicious activity detected",
                    severity="High",
                    status="Open",
                    attack_type=attack_type,
                    ip_address=ip_address
                )

                # ✅ Send Email Alert
                send_intrusion_alert(ticket.id, attack_type, ip_address)

                # ✅ Block Attacker IP
                block_ip(ip_address)

                return JsonResponse({'message': '🚨 Intrusion detected!', 'ticket_id': ticket.id, 'attack_type': attack_type})

            return JsonResponse({'message': '✅ No threats detected'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# ✅ Home View (For Testing)
def home(request):
    return render(request, 'home.html')

def user_login(request):  # Renamed function to avoid conflict
    return render(request, 'login.html')

