from django.shortcuts import render
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
from django.shortcuts import render, redirect
from .forms import PDFUploadForm, DocumentUploadForm, ImageUploadForm
from .models import UploadedFile

def upload_file(request):
    pdf_form = PDFUploadForm()
    doc_form = DocumentUploadForm()
    image_form = ImageUploadForm()

    if request.method == "POST":
        if "pdf_upload" in request.POST:
            pdf_form = PDFUploadForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                file_instance = pdf_form.save(commit=False)
                file_instance.file_type = 'pdf'
                file_instance.save()
                return redirect('upload_file')

        elif "doc_upload" in request.POST:
            doc_form = DocumentUploadForm(request.POST, request.FILES)
            if doc_form.is_valid():
                file_instance = doc_form.save(commit=False)
                file_instance.file_type = 'doc'
                file_instance.save()
                return redirect('upload_file')

        elif "image_upload" in request.POST:
            image_form = ImageUploadForm(request.POST, request.FILES)
            if image_form.is_valid():
                file_instance = image_form.save(commit=False)
                file_instance.file_type = 'image'
                file_instance.save()
                return redirect('upload_file')

    files = UploadedFile.objects.all()
    return render(request, "home.html", {
        "pdf_form": pdf_form,
        "doc_form": doc_form,
        "image_form": image_form,
        "files": files
    })


# ✅ Home View (For Testing)
def home(request):
    return render(request, 'home.html')

def user_login(request):  # Renamed function to avoid conflict
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
def upload(request):
    return render(request,'upload.html')



