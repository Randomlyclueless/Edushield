from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout  # Change 'Authenticate' to 'authenticate'
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
import joblib
import numpy as np
import json
from .models import Ticket, UploadedFile
from .forms import PDFUploadForm, DocumentUploadForm, ImageUploadForm
from .utils import send_intrusion_alert, block_ip
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# ✅ Load AI Model
MODEL_PATH = r"D:\Python projects\Edushield\safeshield\model\safeshiel_model.pkl"
model = joblib.load(MODEL_PATH)

# ✅ Intrusion Detection View
@login_required
def detect_intrusion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            features = data.get("features", [])

            if not features or not isinstance(features, list):
                return JsonResponse({'error': 'Invalid input: Features must be a list'}, status=400)

            features = np.array(features, dtype=np.float32).reshape(1, -1)
            prediction = model.predict(features)[0]

            if prediction != 0:
                attack_type = f"Attack Type {prediction}"
                ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

                # ✅ Create Ticket
                ticket = Ticket.objects.create(
                    description="Suspicious activity detected",
                    severity="High",
                    status="Open",
                    attack_type=attack_type,
                    ip_address=ip_address
                )

                # ✅ Send Email Alert & Block IP
                send_intrusion_alert(ticket.id, attack_type, ip_address)
                block_ip(ip_address)

                return JsonResponse({'message': '🚨 Intrusion detected!', 'ticket_id': ticket.id, 'attack_type': attack_type})

            return JsonResponse({'message': '✅ No threats detected'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# ✅ File Upload View (Restricts to Authenticated Users)
@login_required
def upload_file(request):
    pdf_form = PDFUploadForm()
    doc_form = DocumentUploadForm()
    image_form = ImageUploadForm()

    if request.method == "POST":
        form = None
        file_type = None

        if "pdf_upload" in request.POST:
            form = PDFUploadForm(request.POST, request.FILES)
            file_type = 'pdf'
        elif "doc_upload" in request.POST:
            form = DocumentUploadForm(request.POST, request.FILES)
            file_type = 'doc'
        elif "image_upload" in request.POST:
            form = ImageUploadForm(request.POST, request.FILES)
            file_type = 'image'

        if form and form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.file_type = file_type
            file_instance.user = request.user  # ✅ Restrict files to the logged-in user
            file_instance.save()
            messages.success(request, f"{file_type.upper()} file uploaded successfully!")
            return redirect('upload_file')

    files = UploadedFile.objects.filter(user=request.user)  # ✅ Only fetch user's files
    return render(request, "upload.html", {
        "pdf_form": pdf_form,
        "doc_form": doc_form,
        "image_form": image_form,
        "files": files
    })

# ✅ File Deletion (Ensures User Can Only Delete Their Own Files)
@login_required
def delete_file(request, file_id):
    file_instance = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    file_instance.file.delete()  # Delete file from storage
    file_instance.delete()  # Delete record from database
    messages.success(request, "File deleted successfully.")
    return redirect('upload_file')

# ✅ Home View
def home(request):
    return render(request, 'home.html')
@csrf_exempt
# ✅ Signup View
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user
            login(request, user)  # Log in the user
            return redirect("/landing/")  # Ensure "landing" is a valid URL name in urls.py
    else:
        form = UserCreationForm()  # Show an empty form for GET requests

    return render(request, "signup.html", {"form": form})  # Ensure correct template

# ✅ Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/landing/")  # Ensure this URL name exists
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})





# ✅ Upload Page
@login_required
def upload(request):
    return render(request, 'upload.html')

# ✅ Landing Page
def landing(request):
    return render(request, 'landing.html')

# ✅ Contact Us Page
def contactus(request):
    return render(request, 'contactus.html')

def success(request):
    return render(request, 'success.html')  # Ensure 'success.html' exists in your templates