from django.forms import ModelForm
from .models import ReviewImport

class ReviewImportForm(ModelForm):
    class Meta:
        model = ReviewImport
        fields = ('csv_file',)