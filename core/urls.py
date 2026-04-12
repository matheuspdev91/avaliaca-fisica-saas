from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('alunos/novo/', views.criar_aluno, name='criar_aluno'),

    # Avaliações
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('avaliacoes/nova/', views.criar_avaliacao, name='criar_avaliacao'),
    path('avaliacoes/<int:id>/', views.detalhe_avaliacao, name='detalhe_avaliacao'),
    path('avaliacoes/<int:id>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacoes/<int:id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),

    # Password Reset
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html"
    ), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Dashboard e Gráficos
    path('usuario/<int:usuario_id>/grafico/', views.grafico_aluno, name='grafico_usuario'),
    path('dashboard/<int:id>/', views.dashboard, name='dashboard'),

    # Criança e Idoso
    path('nova/', views.escolher_tipo, name='escolher_tipo'),
    path('criar/crianca/', views.criar_avaliacao_crianca, name='criar_avaliacao_crianca'),
    path('criar/idoso/', views.criar_avaliacao_idoso, name='criar_avaliacao_idoso'),

    # FitFlix
    path('fitflix/', views.fitflix, name='fitflix'),
    path('fitflix/novo/', views.criar_exercicio, name='criar_exercicio'),

    # Treinos
    path('treino/<int:treino_id>/', views.treino_detail, name='treino_detail'),
    path('treino/<int:treino_id>/editar/', views.editar_treino, name='editar_treino'),
    path('treino/novo/', views.criar_treino, name='criar_treino'),
    path('aluno/<int:aluno_id>/', views.painel_aluno, name='painel_aluno')
]
