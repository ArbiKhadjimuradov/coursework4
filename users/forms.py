from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser
from .services import FormClean


class ProfileForm(FormClean, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте имя пользователя',
            'help_text': "!@@@@@"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш email',
            'help_text': "!@@@@@"
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш телефон'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите страну'
        })

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'avatar', 'country',)
        exclude = ('password1', 'password2')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_user = CustomUser.objects.get(password=password)
        return password_user.password

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким username уже существует.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким Email уже существует.")

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр!")
        return phone_number

    def clean(self):
        """Валидация на проверку полей (чтобы не было запрещзенных слов)"""
        super().clean()


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })


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

    def clean(self):
        """Валидация данных сообщения (не должны иметь запрещенные слова)"""
        cleaned_data = super().clean()