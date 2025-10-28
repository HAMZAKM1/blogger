from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------------
# ✅ Register Form
# -----------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create a password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password'
            }),
        }


# -----------------------------
# ✅ Edit Profile Form (includes avatar, bio, social_link)
# -----------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio', 'social_link']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us something about you...'
            }),
            'social_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website or social media link'
            }),
        }
