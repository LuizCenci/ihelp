from django.urls import path
from . import views
app_name = 'ihelp'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/pessoa/', views.cadastro_pessoa, name='cadastro_pessoa'),
    path('cadastro/ong/', views.cadastro_ong, name='cadastro_ong'),
    path('cadastro/', views.cadastro_escolha, name='cadastro_escolha'),
    path('criar-anuncio/', views.criacao_post_vaga, name='criacao_post_vaga'),
    path('vagas/<int:id>', views.post_page, name='post_page'),
]
