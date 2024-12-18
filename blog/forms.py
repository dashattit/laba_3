from django import forms
from .models import AddUser
from django.core.validators import RegexValidator, EmailValidator

# форма для регистрации
class AddUserCreatingForm(forms.ModelForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=100,
        widget=forms.TextInput()
    )
    email = forms.CharField(
        label="Почта",
        max_length=100,
        widget=forms.EmailInput(),
        validators=[
            EmailValidator(message="Почта должна содержать обязательный символ @"),
        ]
    )
    first_name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(
                message="Имя должно содержать только кириллические буквы, дефис и пробелы",
            )
        ]
    )
    last_name = forms.CharField(
        label="Фамилия",
        max_length=100,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(
                message="Фамилия должна содержать только кириллические буквы, дефис и пробелы",
            )
        ]
    )
    patronym = forms.CharField(
        label="Отчество",
        max_length=100,
        widget=forms.TextInput(),
        validators=[
            RegexValidator(
                message="Отчество должно содержать только кириллические буквы, дефис и пробелы",
            )
        ]
    )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    # поле для загрузки аватарки
    avatar = forms.ImageField(label="Аватар", required=True, error_messages={'required': "Пожалуйста, загрузите изображение аватара."})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    class Meta:
        model = AddUser
        fields = ("username", "email", "first_name", "last_name", "patronym", "password", "password_confirm", "avatar")

# форма для входа
class AddUserLoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

# форма для редактирования профиля
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = AddUser
        fields = ("first_name", "last_name", "patronym", "email", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = True  # сделаем аватар обязательным