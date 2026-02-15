from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('avaliacoes')
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, 'core/login.html')



#===========================

# @login_required
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

            avaliacao.percentual_gordura = avaliacao.percentual
            avaliacao.save()

            return redirect('avaliacoes')

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
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe.")
        else:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            login(request, user)
            return redirect('avaliacoes')  # CORRIGIDO

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