from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if email and senha:
            messages.success(request, 'Login simulado com sucesso! (frontend apenas)')
            return redirect('home')
        else:
            messages.error(request, 'Preencha e-mail e senha.')
    return render(request, 'core/login.html')


def cadastro_pessoa(request):
    if request.method == 'POST':
        nome = request.POST.get('nomeCompleto')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')

        if not all([nome, email, cpf, senha, confirmar]):
            messages.error(request, 'Preencha os campos obrigatórios.')
        elif senha != confirmar:
            messages.error(request, 'As senhas não coincidem.')
        else:
            messages.success(request, 'Cadastro de Pessoa simulado! (frontend apenas)')
            return redirect('home')

    return render(request, 'core/cadastro_pessoa.html')


def cadastro_ong(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')
        termos = request.POST.get('termos')  # 'on' se marcado

        if not all([nome, cnpj, email, senha, confirmar]):
            messages.error(request, 'Preencha os campos obrigatórios.')
        elif senha != confirmar:
            messages.error(request, 'As senhas não coincidem.')
        elif termos != 'on':
            messages.error(request, 'É necessário aceitar os termos.')
        else:
            messages.success(request, 'Cadastro de ONG simulado! (frontend apenas)')
            return redirect('home')

    return render(request, 'core/cadastro_ong.html')
