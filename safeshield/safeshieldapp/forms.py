from django import forms
from .models import GovernmentDocument, GeneralDocument, ImageUpload

class GovernmentDocumentForm(forms.ModelForm):
    class Meta:
        model = GovernmentDocument
        fields = ['title', 'file']

class GeneralDocumentForm(forms.ModelForm):
    class Meta:
        model = GeneralDocument
        fields = ['title', 'file']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'file']
