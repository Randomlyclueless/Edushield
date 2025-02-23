import os
import logging
import json
import joblib
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import PDFUploadForm, DocumentUploadForm, ImageUploadForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Ticket, UploadedFile
from .utils import send_intrusion_alert, block_ip
from django.contrib.auth.decorators import login_required
import phonenumbers
from .sms_utils import send_sms_fast2sms, send_otp, verify_otp
from .email_utils import send_access_email

# Setup logger
logger = logging.getLogger(__name__)

# ✅ Load AI Model
MODEL_PATH = os.getenv('MODEL_PATH', r'D:\Python projects\Edushield\safeshield\model\safeshiel_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError as e:
    logger.error(f"Model file not found at {MODEL_PATH}: {e}")
    raise

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

                ticket = Ticket.objects.create(
                    description="Suspicious activity detected",
                    severity="High",
                    status="Open",
                    attack_type=attack_type,
                    ip_address=ip_address
                )

                send_intrusion_alert(ticket.id, attack_type, ip_address)
                block_ip(ip_address)

                return JsonResponse({'message': 'Intrusion detected!', 'ticket_id': ticket.id, 'attack_type': attack_type})

            return JsonResponse({'message': 'No threats detected'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.exception(f"Error occurred during intrusion detection: {str(e)}")
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

# ✅ Success Page
def success(request):
    return render(request, 'success.html')

# ✅ Register View (Handles User Registration)
def signup(request):
    return render(request, 'signup.html')

# ✅ Login View (Handles User Login)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Log the user in
            return redirect(request.GET.get('next', 'landing'))  # Redirect to intended page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# ✅ Logout View
def logout_view(request):
    auth_logout(request)  # Log the user out
    return redirect('landing')  # Redirect to landing page after logout

# ✅ Dashboard View
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ✅ Knowstat View
def knowstat_view(request):
    return render(request, 'knowstat.html')

# ✅ SMS Sending View
def send_sms_view(request):
    phone_number = request.GET.get("phone")
    message = request.GET.get("message", "Hello from SafeShield!")

    if phone_number:
        try:
            phone_obj = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(phone_obj):
                return JsonResponse({"error": "Invalid phone number"}, status=400)
        except phonenumbers.phonenumberutil.NumberParseException:
            return JsonResponse({"error": "Invalid phone number format"}, status=400)

        response = send_sms_fast2sms(phone_number, message)
        return JsonResponse(response)

    return JsonResponse({"error": "Phone number is required"}, status=400)

# ✅ OTP Views
def send_otp_view(request):
    phone_number = request.GET.get("phone")

    if phone_number:
        response = send_otp(phone_number)
        return JsonResponse(response)

    return JsonResponse({"success": False, "message": "Phone number is required"}, status=400)

def verify_otp_view(request):
    phone_number = request.GET.get("phone")
    user_otp = request.GET.get("otp")

    if phone_number and user_otp:
        response = verify_otp(phone_number, user_otp)
        return JsonResponse(response)

    return JsonResponse({"success": False, "message": "Phone number and OTP are required"}, status=400)

# ✅ Safespace Access View
def safespace_view(request):
    user_email = request.user.email  # Get the user's email
    send_access_email(user_email)  # Send the access email

    return render(request, 'safeshieldapp/safespace.html')  # Render the Safespace page
