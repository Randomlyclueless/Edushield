from django import forms
from .models import UploadedFile

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return file

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_extensions = ['.csv', '.txt', '.docx']
        if not any(file.name.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only CSV, TXT, or DOCX files are allowed.")
        return file

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if not any(file.name.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only JPG, JPEG, or PNG images are allowed.")
        return file

