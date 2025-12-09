from django.urls import path
from . import views
app_name = 'ihelp'
urlpatterns = [
    #CADASTRO
    path('cadastro/', views.cadastro_escolha, name='cadastro_escolha'),
    path('cadastro/pessoa/', views.cadastro_pessoa, name='cadastro_pessoa'),
    path('cadastro/ong/', views.cadastro_ong, name='cadastro_ong'),
    #LOGIN
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #HOME
    path('', views.home_feed, name='home_feed'),
    path('vagas/', views.home_vagas, name='home_vagas'),
    #
    path('criar-anuncio/', views.criacao_post_vaga, name='criacao_post_vaga'),
    path('vagas/<int:id>', views.post_page, name='post_page'),
    path('search/', views.search, name='search'),
    path('editar-anuncio/<int:id>', views.editar_post_vaga, name='editar_post_vaga'),
    path('deletar-anuncio/<int:id>', views.deletar_post_vaga, name='deletar_post_vaga'),
    #FEED
    path('criar-post-feed/', views.criar_post_feed, name='criar_post_feed'),
    path('deletar-post-feed/<int:id>', views.deletar_post_feed, name='deletar_post_feed'),
    path('comentario/<int:post_id>/adicionar/', views.comentar_post, name='comentar_post'),
    #CANDIDATURAS
    path('visualizar-candidaturas', views.visualizar_candidaturas, name='visualizar_candidaturas'),
    path('meus-anuncios/', views.visualizar_meus_anuncios, name='visualizar_meus_anuncios'),
    path('vagas/candidatar/<int:id>', views.confirmar_candidatura, name='confirmar_candidatura'),
    path('candidaturas/aprovar/<int:id>', views.aceitar_candidatura, name='aceitar_candidatura'),
    path('candidaturas/recusar/<int:id>', views.recusar_candidatura, name='recusar_candidatura'),
    path('candidaturas/deletar/<int:id>', views.deletar_candidatura, name='deletar_candidatura'),
]

