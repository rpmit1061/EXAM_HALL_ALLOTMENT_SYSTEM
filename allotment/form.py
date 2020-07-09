from django import forms
from .models import UploadFile, RoomCreate


class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['sessionmonth', 'year', 'file', 'ttfile']


class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = RoomCreate
        fields = ['room_no', 'no_col', 'no_row', 'total_capacity']
