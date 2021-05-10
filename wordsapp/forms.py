from django import forms


class UserForm(forms.Form):
    translate = forms.CharField(help_text="Введите перевод слова")
