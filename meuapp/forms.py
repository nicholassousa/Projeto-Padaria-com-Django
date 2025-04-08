from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Pedido


class RegistroForm(forms.ModelForm):
    primeiro_nome = forms.CharField(label='Primeiro nome', max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Primeiro nome'}))
    sobre_nome = forms.CharField(label='Sobre-nome', max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Sobre-nome'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    class Meta:
        model = User
        fields = ['primeiro_nome', 'sobre_nome', 'email', 'password']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['produto', 'quantidade']


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # devemos usar o username para o email, pois o campo username é obrigatório, esta biblioteca usa o email como username
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    remember_me = forms.BooleanField(label='Manter conectado', required=False)


