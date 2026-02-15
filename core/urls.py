from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('avaliacoes/nova/', views.criar_avaliacao, name='criar_avaliacao'),
    path('avaliacoes/<int:id>/', views.detalhe_avaliacao, name='detalhe_avaliacao'),
    path('avaliacoes/<int:id>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacoes/<int:id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),

    # 🔥 DASHBOARD COM ID
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),
]
