from django import forms
from .models import Scan
class BarcodeForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = "__all__"
        widgets = {
            'shelf': forms.TextInput(attrs={'type': 'hidden'}),
        }

class ScanCode(forms.Form):
    # shelf = forms.CharField(label = "Shelf name or number")
    barcode = forms.ImageField(label = "Upload Image to scan",required=False)
    barcode_manually  =forms.CharField(label = "Scan Code or Manually add",required = False)
    qty = forms.IntegerField()
