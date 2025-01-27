from django import forms

class LinkForm(forms.Form):
    original_url = forms.URLField(label='Оригинальный URL', widget=forms.URLInput(attrs={'placeholder': 'Вставьте длинную ссылку'}))
