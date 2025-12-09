from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction
from .models import *


class CustomUserCreationForm(forms.ModelForm):
    """Formulário para criação de usuários (usado em admin ou registro)."""
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'country', 'state', 'city', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Formulário de atualização do usuário."""
    password = ReadOnlyPasswordHashField(label="Senha")

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'country', 'state', 'city', 'role', 'is_active', 'is_staff']


# VOLUNTÁRIO
# =============================
class VolunteerRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Defina sua senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    accept_announcements = forms.BooleanField(
        label="Aceitar receber avisos?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'country', 'state', 'city']
        labels = {
            'username': 'Nome',
            'email': 'E-mail',
            'phone_number': 'Telefone',
            'country': 'País',
            'state': 'Estado',
            'city': 'Cidade',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.VOLUNTEER
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            PersonProfile.objects.create(
                user=user,
                name=user.username,
                cpf=self.cleaned_data['cpf'],
                accept_announcements=self.cleaned_data['accept_announcements']
            )
        return user



# =============================
# ONG
# =============================
class OngRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Defina sua senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    cnpj = forms.CharField(
        label="CNPJ",
        max_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    site = forms.URLField(
        label="Site (opcional)",
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Endereço",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    description = forms.CharField(
        label="Descrição da ONG",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'country', 'state', 'city']
        labels = {
            'username': 'Nome da ONG',
            'email': 'E-mail de contato',
            'phone_number': 'Telefone',
            'country': 'País',
            'state': 'Estado',
            'city': 'Cidade',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.ONG
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            OngProfile.objects.create(
                user=user,
                ong_name=user.username,
                cnpj=self.cleaned_data['cnpj'],
                site=self.cleaned_data.get('site'),
                address=self.cleaned_data.get('address'),
                description=self.cleaned_data.get('description')
            )
        return user



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PostAnnouncementForm(forms.ModelForm):
    class Meta:
        model = PostAnnouncement
        fields = ['title', 'description', 'photo', 'status', 'link_forms']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    # Campo de categorias (muitos-para-muitos)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    def save(self, commit=True, ong=None):
        post = super().save(commit=False)

        if ong is not None:
            post.ong = ong

        if commit:
            post.save()
            self.save_m2m()

        return post


# ============================================
# FORM: PostFeed
# ============================================
class PostFeedForm(forms.ModelForm):
    class Meta:
        model = PostFeed
        fields = ['description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True, ong=None):
        feed = super().save(commit=False)
        if ong is not None:
            feed.ong = ong
        if commit:
            feed.save()
            
        return feed


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva um comentário...'
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
