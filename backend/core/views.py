from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import *
from .models import PostAnnouncement, Role

#LOGIN, LOGOUT E CADASTRO
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if email and senha:
            user = authenticate(request, username=email, password=senha)
            if user:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso!')
                return redirect('ihelp:home_feed')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')
        else:
            messages.error(request, 'Preencha e-mail e senha.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('ihelp:home_feed')


def cadastro_pessoa(request):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro de voluntário realizado com sucesso!")
            return redirect('ihelp:home_feed')
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
            return redirect('ihelp:home_feed')
    else:
        form = OngRegisterForm()
    return render(request, 'core/cadastro_ong.html', {'form': form})

def cadastro_escolha(request):
    return render(request, 'core/cadastro_escolha.html')

#HOME DE FEED E ANUNCIO
def home_feed(request):
    posts = (
        PostFeed.objects
        .select_related('ong')
        .prefetch_related('comments__user')
        .order_by('-created_at')
    )

    comment_form = CommentForm()

    return render(request, 'core/home_feed.html', {
        'posts': posts,
        'comment_form': comment_form
    })

def home_vagas(request):
    """Visualizar anúncios."""

    anuncios = PostAnnouncement.objects.filter(status='ABERTA').order_by('-id')
    
    selected_ods = request.GET.getlist('ods')
    context = {'anuncios': anuncios,'ods_categories': Category.objects.order_by('name'), 'selected_ods': [str(i) for i in selected_ods],}
    return render(request, 'core/home.html', context)

#VISUALIZAÇÃO DE POST
def post_page(request, id):
    anuncio = get_object_or_404(PostAnnouncement, id=id)

    already_applied = False
    if request.user.is_authenticated and request.user.role == "VOLUNTEER":
        already_applied = Application.objects.filter(
            post=anuncio,
            volunteer=request.user,
        ).exists()
    print("User atual:", request.user.id, request.user.email)
    print("Applications desse user:", Application.objects.filter(volunteer=request.user))
    print("Existe para este post?", Application.objects.filter(volunteer=request.user, post=anuncio).exists())

    context = {
    'anuncio': anuncio,
    'already_applied': already_applied,}
    

    return render(request, 'core/anuncio_view.html', context)

@login_required
def confirmar_candidatura(request, id):
    anuncio = get_object_or_404(PostAnnouncement, id=id)

    Application.objects.get_or_create(
        post=anuncio,
        volunteer=request.user,
        defaults={'status': 'PENDENTE'},
    )

    return redirect('ihelp:post_page', id=anuncio.id)

#BUSCA POR ANUNCIO
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


#CRUD DE ANUNCIO
@login_required
def criacao_post_vaga(request):
    if getattr(request.user, 'role', None) != Role.ONG:
        messages.error(request, 'Apenas ONGs podem criar postagens.')
        return redirect('ihelp:home_vagas')
    
    if request.method == "POST":
        form = PostAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(ong=request.user)
            messages.success(request, 'Post criado com sucesso!')
            return redirect('ihelp:home_vagas')
    
    else:
        form = PostAnnouncementForm()

    return render(request, 'core/criacao_post_vaga.html', {'form': form})


@login_required
def editar_post_vaga(request, id):

    if getattr(request.user, 'role', None) != Role.ONG:
        messages.error(request, 'Apenas ONGs podem editar postagens.')
        return redirect('ihelp:home_vagas')
    

    post = get_object_or_404(PostAnnouncement, id=id)
    print(request.user.is_authenticated)
    print(request.user == post.ong)
    if post.ong != request.user:
        messages.error(request, 'Você não tem permissão para editar este post.')
        return redirect('ihelp:home_vagas')

    # Construir o form
    if request.method == 'POST':
        form = PostAnnouncementForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.ong = request.user
            post.save()
            form.save_m2m()   # salva categorias
            messages.success(request, 'Post editado com sucesso!')
            return redirect('ihelp:home_vagas')

    else:
        form = PostAnnouncementForm(instance=post, initial={
            'categories': post.categories.all()
        })

    return render(request, 'core/editar_post_vaga.html', {
        'form': form,
        'item_id': id
    })

@login_required
def deletar_post_vaga(request, id):

    # Apenas ONGs podem excluir
    if getattr(request.user, 'role', None) != Role.ONG:
        messages.error(request, 'Apenas ONGs podem excluir postagens.')
        return redirect('ihelp:home_vagas')

    post = get_object_or_404(PostAnnouncement, id=id)

    # ONG só pode excluir seus próprios posts
    if post.ong != request.user:
        messages.error(request, 'Você não tem permissão para excluir este post.')
        return redirect('ihelp:home_vagas')

    # Confirmar exclusão
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deletado com sucesso!')
        return redirect('ihelp:home_vagas')

    return render(request, 'core/deletar_post_vaga.html', {
        'post': post,
        'id':id
    })

#CRUD DE FEED - SEM UPDATE
@login_required
def criar_post_feed(request):
    if request.user.role != Role.ONG:
        messages.error(request, "Apenas ONGs podem criar posts no feed.")
        return redirect('ihelp:home_feed')

    if request.method == 'POST':
        form = PostFeedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(ong=request.user)
            messages.success(request, "Post criado com sucesso!")
            return redirect('ihelp:home_feed')
    else:
        form = PostFeedForm()

    return render(request, 'core/criacao_post_feed.html', {
        'form': form
    })

@login_required
def comentar_post(request, post_id):
    post = get_object_or_404(PostFeed, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.user = request.user
            comentario.post = post
            comentario.save()
            return redirect('ihelp:home_feed')

    return redirect('ihelp:home_feed')

@login_required
def deletar_post_feed(request, id):
    post = get_object_or_404(PostFeed, id=id)

    if post.ong != request.user:
        messages.error(request, "Você não pode deletar este post.")
        return redirect('ihelp:home_feed')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post apagado!")
        return redirect('ihelp:home_feed')

    return render(request, 'core/deletar_post_feed.html', {'post': post})


@login_required
def visualizar_candidaturas(request):
    user = request.user

    if user.role == "ONG":
        applications = Application.objects.filter(
            post__ong=user
        ).order_by('status', 'application_date') 
    else:  
        applications = Application.objects.filter(
            volunteer=user
        ).order_by('-application_date')

    context = {
        'applications': applications,
        'is_ong': user.role == "ONG",
    }
    return render(request, 'core/visualizar_candidaturas.html', context)


@login_required
def aceitar_candidatura(request, id):
    app = get_object_or_404(Application, id=id)

    # garantir que só a ONG dona da vaga possa mudar
    if app.post.ong != request.user:
        messages.error(request, "Você não pode editar este post.")
        return redirect('ihelp:home_feed')

    app.status = 'ACEITA'
    app.save()
    return redirect('ihelp:visualizar_candidaturas')


@login_required
def recusar_candidatura(request, id):
    app = get_object_or_404(Application, id=id)

    if app.post.ong != request.user:
        messages.error(request, "Você não pode editar este post.")
        return redirect('ihelp:home_feed')
    app.status = 'RECUSADA'
    app.save()
    return redirect('ihelp:visualizar_candidaturas')

@login_required
def deletar_candidatura(request, id):
    app = get_object_or_404(Application, id=id)

    if app.volunteer != request.user:
        messages.error(request, "Você não pode deletar esta candidatura.")
        return redirect('ihelp:home_feed')

    app.delete()
    return redirect('ihelp:visualizar_candidaturas')


@login_required
def visualizar_meus_anuncios(request):
    """Visualizar anúncios da ONG logada."""
    user = request.user

    if user.role != Role.ONG:
        messages.error(request, "Apenas ONGs podem acessar esta página.")
        return redirect('ihelp:home_vagas')

    anuncios = PostAnnouncement.objects.filter(ong=user).order_by('-created_at')

    context = {
        'anuncios': anuncios,
    }
    return render(request, 'core/visualizar_meus_anuncios.html', context)
