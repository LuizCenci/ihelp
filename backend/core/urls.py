from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastro/pessoa/', views.cadastro_pessoa, name='cadastro_pessoa'),
    path('cadastro/ong/', views.cadastro_ong, name='cadastro_ong'),
]
