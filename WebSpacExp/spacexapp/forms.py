from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload CSV File")
class FolderSelectionForm(forms.Form):
    folder_path = forms.CharField(label="Путь к папке", widget=forms.TextInput(attrs={'placeholder': 'Введите путь к папке'}))
