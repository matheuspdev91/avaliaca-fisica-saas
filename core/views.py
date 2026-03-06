from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
User = get_user_model()


from .models import AvaliacaoFisica
from .forms import (
    AvaliacaoFisicaForm,
    CircunferenciaForm,
    AdipometriaForm
)

# =========================
# HOME
# =========================
def home(request):
    return render(request, 'core/home.html')


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == 'GET':
        return render(request, 'core/login.html')

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_page = request.GET.get('next')

        
        if not username or not password:
            messages.error(request, 'Preencha usuário e senha.')
            return render(request, 'core/login.html')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem vindo, {user.username}!')

            if next_page:
                return redirect(next_page)
            return redirect('avaliacoes')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'core/login.html', {
                'username': username
            })
     


#===========================

@login_required
def criar_avaliacao(request):
    if request.method == 'POST':
        avaliacao_form = AvaliacaoFisicaForm(request.POST)
        circ_form = CircunferenciaForm(request.POST)
        adip_form = AdipometriaForm(request.POST)

        if (
            avaliacao_form.is_valid() and
            circ_form.is_valid() and
            adip_form.is_valid()
        ):
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()

            circ = circ_form.save(commit=False)
            circ.avaliacao = avaliacao
            circ.save()

            adip = adip_form.save(commit=False)
            adip.avaliacao = avaliacao
            adip.save()

            return redirect('grafico_usuario', usuario_id= request.user.id)

    else:
        avaliacao_form = AvaliacaoFisicaForm()
        circ_form = CircunferenciaForm()
        adip_form = AdipometriaForm()

    return render(request, 'core/criar_avaliacao.html', {
        'avaliacao_form': avaliacao_form,
        'circ_form': circ_form,
        'adip_form': adip_form,
    })
    

    

# =========================
# GRÁFICO
# =========================
def grafico_aluno(request, usuario_id):
    avaliacoes = AvaliacaoFisica.objects.filter(
        usuario=request.user
    ).order_by('-id')
    
    if not avaliacoes.exists():
        return redirect('criar_avaliacao')
    
    avaliacao_atual = avaliacoes.first()

    return render(request, 'core/grafico_aluno.html',{
        'avaliacao_atual': avaliacao_atual
    })
# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # ✅ VALIDAÇÕES (uma por vez, com return imediato)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
            return render(request, 'core/register.html', {
                'username': username,
                'email': email
            })

        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return render(request, 'core/register.html', {
                'username': username,
                'email': email
            })

        if password != password_confirm:
            messages.error(request, 'As senhas não são iguais.')
            return render(request, 'core/register.html', {
                'username': username,
                'email': email
            })

        if len(password) < 6:
            messages.error(request, 'A senha deve ter no mínimo 6 dígitos.')
            return render(request, 'core/register.html', {
                'username': username,
                'email': email
            })

        # ✅ SE CHEGOU AQUI, TUDO ESTÁ OK → CRIA O USUÁRIO
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')  # ✅ 'success' (2 c)
            return redirect('avaliacoes')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar a conta: {str(e)}')
            return render(request, 'core/register.html', {
                'username': username,
                'email': email
            })

    return render(request, 'core/register.html')


# =========================
# LISTAR AVALIAÇÕES
# =========================
@login_required
def avaliacoes(request):
    avaliacoes = (
        AvaliacaoFisica.objects
        .filter(usuario=request.user)
        .order_by('-criado_em')
        .order_by('-criado_em')
    )

    return render(request, 'core/avaliacoes.html', {
        'avaliacoes': avaliacoes
    })


# =========================
# DETALHE
# =========================
@login_required
def detalhe_avaliacao(request, id):
    avaliacao = get_object_or_404(
        AvaliacaoFisica,
        id=id,
        usuario=request.user
    )

    return render(request, 'core/detalhe_avaliacao.html', {
        'avaliacao': avaliacao
    })


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request, id):
    avaliacao = get_object_or_404(
        AvaliacaoFisica,
        id=id,
        usuario=request.user
    )

    return render(request, 'core/dashboard.html', {
        'avaliacao': avaliacao
    })


#========================

# EDITAR

#========================
@login_required
def editar_avaliacao(request, id):
    avaliacao = get_object_or_404(
        AvaliacaoFisica,
        id=id,
        usuario=request.user
    )

    circ = avaliacao.circunferencias
    adip = avaliacao.adipometria

    if request.method == 'POST':
        avaliacao_form = AvaliacaoFisicaForm(request.POST, instance=avaliacao)
        circ_form = CircunferenciaForm(request.POST, instance=circ)
        adip_form = AdipometriaForm(request.POST, instance=adip)

        if (
            avaliacao_form.is_valid() and
            circ_form.is_valid() and
            adip_form.is_valid()
        ):
            avaliacao = avaliacao_form.save()
            circ_form.save()
            adip_form.save()

            return redirect('detalhe_avaliacao', id=avaliacao.id)

    else:
        avaliacao_form = AvaliacaoFisicaForm(instance=avaliacao)
        circ_form = CircunferenciaForm(instance=circ)
        adip_form = AdipometriaForm(instance=adip)

    return render(request, 'core/criar_avaliacao.html', {
        'avaliacao_form': avaliacao_form,
        'circ_form': circ_form,
        'adip_form': adip_form,
    })


#========================

# EXCLUIOR

@login_required
def excluir_avaliacao(request, id):
    avaliacao = get_object_or_404(
        AvaliacaoFisica,
        id=id,
        usuario=request.user
    )

    avaliacao.delete()
    return redirect('avaliacoes')


#=========================