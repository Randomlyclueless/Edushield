from django import forms
from .models import UploadedFile

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')

        # ✅ Check if file is None
        if not file:
            raise forms.ValidationError("No file uploaded.")

        # ✅ Validate PDF extension (case-insensitive)
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")

        # ✅ Restrict file size (e.g., max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 5MB.")

        return file


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            raise forms.ValidationError("No file uploaded.")

        # ✅ Allowed extensions (case-insensitive)
        allowed_extensions = ['.csv', '.txt', '.docx']
        if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only CSV, TXT, or DOCX files are allowed.")

        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 5MB.")

        return file


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            raise forms.ValidationError("No file uploaded.")

        # ✅ Allowed image formats (case-insensitive)
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only JPG, JPEG, or PNG images are allowed.")

        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 5MB.")

        return file