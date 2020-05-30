from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput # criar form de login
from blog.models import Usuario

class ResgistroDeUsuario(UserCreationForm):
    # Herda do formulário de registro padrão do django
    class Meta:
        # define o model com o qual esse formulário irá interagir e os seus fields
        model = User
        fields = ['username','password1','password2']

class RegistroDePerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome','email','idade','genero','escolaridade','curso','nacionalidade']

class AtualizarUsuario(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class AtualizarPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome','email','idade','genero','escolaridade','curso','nacionalidade']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Usuário'}))
    # username = forms.EmailField(widget=TextInput(attrs={'class':'validate','placeholder': 'Usuário'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Senha'}))
