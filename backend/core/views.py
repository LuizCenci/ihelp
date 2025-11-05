from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

def home(request):
    anuncios = Post.objects.filter(status='ABERTA').order_by('-id')
    print(anuncios)
    context = {'anuncios': anuncios}
    return render(request, 'core/home.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if email and senha:
            user = authenticate(request, username=email, password=senha)
            if user:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso!')
                return redirect('ihelp:home')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')
        else:
            messages.error(request, 'Preencha e-mail e senha.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('ihelp:home')


def cadastro_pessoa(request):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro de voluntário realizado com sucesso!")
            return redirect('ihelp:home')
    else:
        form = VolunteerRegisterForm()
    return render(request, 'core/cadastro_pessoa.html', {'form': form})


def cadastro_ong(request):
    if request.method == 'POST':
        form = OngRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro de ONG realizado com sucesso! Aguarde aprovação.")
            return redirect('ihelp:home')
    else:
        form = OngRegisterForm()
    return render(request, 'core/cadastro_ong.html', {'form': form})

def cadastro_escolha(request):
    return render(request, 'core/cadastro_escolha.html')

@login_required
def criacao_post_vaga(request):
    if getattr(request.user, 'role', None) != Role.ONG:
        messages.error(request, 'Apenas ONGs podem criar postagens.')
        return redirect('ihelp:home')
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(ong=request.user)
            messages.success(request, 'Post criado com sucesso!')
            return redirect('ihelp:home')
    
    else:
        form = PostForm()

    return render(request, 'core/criacao_post_vaga.html', {'form': form})
