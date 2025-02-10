from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите свою почту'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-select'
        })

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр!")
        return phone_number

    def clean(self):
        """Валидация данных сообщения (не должны иметь запрещенные слова)"""
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        banned_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        for word in banned_words:
            if word in username.lower():
                self.add_error(
                    "username",
                    f'Нельзя использовать слово "{word.title()}" в поле username.',
                )
            if word in email.lower():
                self.add_error(
                    "email",
                    f'Нельзя использовать слово "{word.title()}" в email.',
                )