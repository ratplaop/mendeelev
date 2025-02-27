from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Create your forms here.

class RegistrationForm(forms.ModelForm):
    # Поля для пользователя
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    # Новые поля для профиля
    education = forms.CharField(max_length=255, required=False, label="Образование")
    date_of_birth = forms.DateField(required=False, label="Дата рождения", widget=forms.SelectDateWidget(years=range(1900, 2023)))
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    photo = forms.ImageField(required=False, label="Фотография")

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Проверка на существование профиля
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'education': self.cleaned_data['education'],
                    'date_of_birth': self.cleaned_data['date_of_birth'],
                    'phone': self.cleaned_data['phone'],
                    'photo': self.cleaned_data['photo']
                }
            )
            if not created:
                # Если профиль уже существует, обновите его данные
                profile.education = self.cleaned_data['education']
                profile.date_of_birth = self.cleaned_data['date_of_birth']
                profile.phone = self.cleaned_data['phone']
                profile.photo = self.cleaned_data['photo']
                profile.save()
        return user
