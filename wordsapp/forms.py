from django import forms


class UserForm(forms.Form):
    name = forms.CharField(help_text="Введите перевод слова")
