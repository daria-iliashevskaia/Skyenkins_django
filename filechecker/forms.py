from django import forms

from filechecker.models import File
from users.forms import StyleFormMixin


class UploadFileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]


class DetailFileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]


class UpdateFileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file"]

