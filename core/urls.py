from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
print("ESTOU NO CORE URLS CERTO")
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
    path(
        "meu-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),




    # 🔥 DASHBOARD COM ID
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),
    path('usuario/<int:usuario_id>/grafico/', views.grafico_aluno, name='grafico_usuario')
]
