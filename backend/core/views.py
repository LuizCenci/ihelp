from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import *
from .models import PostAnnouncement, Role


def home(request):
    """Página inicial com anúncios abertos."""
    anuncios = PostAnnouncement.objects.filter(status='ABERTA').order_by('-created_at')
    context = {'anuncios': anuncios}
    return render(request, 'core/home.html', context)


def post_page(request, id):
    """Visualizar detalhes de um anúncio."""
    anuncio = get_object_or_404(PostAnnouncement, pk=id)
    return render(request, 'core/anuncio_view.html', {'anuncio': anuncio})


def login_view(request):
    """View para login de usuários."""
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
    """View para logout de usuários."""
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('ihelp:home')


def cadastro_pessoa(request):
    """Cadastro de voluntário."""
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
    """Cadastro de ONG."""
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
    """Página de escolha entre voluntário e ONG."""
    return render(request, 'core/cadastro_escolha.html')


@login_required
def criacao_post_vaga(request):
    """Criação de anúncio/vaga (apenas para ONGs)."""
    if getattr(request.user, 'role', None) != Role.ONG:
        messages.error(request, 'Apenas ONGs podem criar postagens.')
        return redirect('ihelp:home')
    
    if request.method == "POST":
        form = PostAnnouncementForm(request.POST)
        if form.is_valid():
            form.save(ong=request.user)
            messages.success(request, 'Post criado com sucesso!')
            return redirect('ihelp:home')
    else:
        form = PostAnnouncementForm()

    return render(request, 'core/criacao_post_vaga.html', {'form': form})
