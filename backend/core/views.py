from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import *
from .models import PostAnnouncement, Role

def home(request):
    anuncios = PostAnnouncement.objects.filter(status='ABERTA').order_by('-created_at')
    context = {'anuncios': anuncios}
    return render(request, 'core/home.html', context)

    """Visualizar feed de postagens."""
    return redirect('ihelp:home_vagas')


def home_vagas(request):
    """Visualizar anúncios."""

    anuncios = PostAnnouncement.objects.filter(status='ABERTA').order_by('-id')
    
    selected_ods = request.GET.getlist('ods')
    context = {'anuncios': anuncios,'ods_categories': Category.objects.order_by('name'), 'selected_ods': [str(i) for i in selected_ods],}
    return render(request, 'core/home.html', context)

def post_page(request, id):
    anuncio = get_object_or_404(PostAnnouncement, pk=id)
    return render(request, 'core/anuncio_view.html', {'anuncio': anuncio})


def search(request):
    search_term = request.GET.get('q', '').strip()
    ods = request.GET.getlist('ods', '')
    
    anuncios  = PostAnnouncement.objects.all()

    if search_term:
        anuncios =anuncios.filter(
            Q(
                Q(title__icontains = search_term) | Q(description__icontains = search_term) | 
                Q(ong__ong_profile__ong_name__icontains=search_term) | Q(ong__city__icontains=search_term)   
            ), status ='ABERTA'
        ).order_by('-id')

    do_filter_ods = ods and '' not in ods
    if do_filter_ods:
        print(ods)
        anuncios = anuncios.filter(categories__id__in=ods)

    anuncios = anuncios.distinct()
    context = {"page_title":f'Pesquisa por "{search_term}"', "search_term": search_term, "anuncios":anuncios,}
    return render(request, 'core/search_result.html', context)

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
        form = PostAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(ong=request.user)
            messages.success(request, 'Post criado com sucesso!')
            return redirect('ihelp:home')
    
    else:
        form = PostAnnouncementForm()

    return render(request, 'core/criacao_post_vaga.html', {'form': form})
