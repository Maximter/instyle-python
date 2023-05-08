from django import forms


class AvatarForm(forms.Form):
    photo = forms.ImageField(allow_empty_file=False, label='Аватар',)
