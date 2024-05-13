# FORMS.PY
from django import forms
from .models import Orden

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['primer_nombre', 'apellido', 'correo']