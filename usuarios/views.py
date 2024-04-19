from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        users = User.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Este usuário já esta cadastrado no sistema.')
            return redirect('/usuarios/cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não conferem.')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha tem que possuir pelo menos 6 caracteres.')
            return redirect('/usuarios/cadastro')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )
            
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso.')
            return redirect('/usuarios/login')
        
        except:
            messages.add_message(request, constants.ERROR, 
                                 'Erro inesperado do sistema, entre em contato com o administrador do sistema.')
            return redirect('/usuarios/cadastro')
        
def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('senha')
        
        if not username or not password:
            messages.add_message(request, constants.ERROR, 'Informe usuário e senha.')
            return redirect('/usuarios/login')
        
        user = auth.authenticate(request, username=username, password=password)
        
        if user:
            auth.login(user)
            return redirect('/pacientes/home')
        
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
        return redirect('/usuarios/login')
    
def logout_view(request):
    auth.logout(request)
    return redirect('usuarios/login')