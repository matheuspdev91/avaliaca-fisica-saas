from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
from .models import Aluno, Treino

from .models import (
    AvaliacaoFisica, VideoExercicio, VariacaoExercicio,
    AvaliacaoCrianca, AvaliacaoIdoso, Treino
)
from .forms import (
    CriarTreinoForm,
    AvaliacaoFisicaForm,
    CircunferenciaForm,
    AdipometriaForm,
    AvaliacaoCriancaForm,
    AvaliacaoIdosoForm,
    ExercicioTreinoFormSet,
    TreinoForm,
)

User = get_user_model()


# =========================
# HOME
# =========================
def home(request):
    if request.user.is_authenticated:
        return redirect('core:avaliacoes')
    return render(request, 'core/home.html')


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')

    email = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=email, password=password)

    if user:
        login(request, user)
        return redirect('core:avaliacoes')

    messages.error(request, 'Email ou senha invalidos')
    return render(request, 'core/login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('core:login')


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ja existe')
            return render(request, 'core/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('core:avaliacoes')

    return render(request, 'core/register.html')


# =========================
# CRIAR AVALIACAO (CORE)
# =========================
@login_required
def criar_avaliacao(request):
    if request.method == 'POST':
        avaliacao_form = AvaliacaoFisicaForm(request.POST)
        circ_form = CircunferenciaForm(request.POST)
        adip_form = AdipometriaForm(request.POST)
        crianca_form = AvaliacaoCriancaForm(request.POST)
        idoso_form = AvaliacaoIdosoForm(request.POST)

        tipo = request.POST.get('tipo')

        if avaliacao_form.is_valid() and circ_form.is_valid() and adip_form.is_valid():
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()

            circ = circ_form.save(commit=False)
            circ.avaliacao = avaliacao
            circ.save()

            adip = adip_form.save(commit=False)
            adip.avaliacao = avaliacao
            adip.save()

            if tipo == 'crianca' and crianca_form.is_valid():
                crianca = crianca_form.save(commit=False)
                crianca.avaliacao = avaliacao
                crianca.save()

            elif tipo == 'idoso' and idoso_form.is_valid():
                idoso = idoso_form.save(commit=False)
                idoso.avaliacao = avaliacao
                idoso.save()

            return redirect('core:avaliacoes')

    else:
        avaliacao_form = AvaliacaoFisicaForm()
        circ_form = CircunferenciaForm()
        adip_form = AdipometriaForm()
        crianca_form = AvaliacaoCriancaForm()
        idoso_form = AvaliacaoIdosoForm()

    return render(request, 'core/criar_avaliacao.html', {
        'avaliacao_form': avaliacao_form,
        'circ_form': circ_form,
        'adip_form': adip_form,
        'crianca_form': crianca_form,
        'idoso_form': idoso_form,
    })


# =========================
# LISTAR
# =========================
@login_required
def avaliacoes(request):
    avaliacoes = AvaliacaoFisica.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

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

    composicao = calcular_composicao(avaliacao)

    return render(request, 'core/dashboard.html', {
        'avaliacao': avaliacao,
        'composicao': composicao
    })


# =========================
# EDITAR
# =========================
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

        if avaliacao_form.is_valid() and circ_form.is_valid() and adip_form.is_valid():
            avaliacao_form.save()
            circ_form.save()
            adip_form.save()

            return redirect('core:detalhe_avaliacao', id=avaliacao.id)

    else:
        avaliacao_form = AvaliacaoFisicaForm(instance=avaliacao)
        circ_form = CircunferenciaForm(instance=circ)
        adip_form = AdipometriaForm(instance=adip)

    return render(request, 'core/criar_avaliacao.html', {
        'avaliacao_form': avaliacao_form,
        'circ_form': circ_form,
        'adip_form': adip_form,
    })


# =========================
# EXCLUIR
# =========================
@login_required
def excluir_avaliacao(request, id):
    avaliacao = get_object_or_404(
        AvaliacaoFisica,
        id=id,
        usuario=request.user
    )

    avaliacao.delete()
    return redirect('core:avaliacoes')


# =========================
# FITFLIX
# =========================
@login_required
def fitflix(request):
    videos = VideoExercicio.objects.prefetch_related('variacoes').all()
    return render(request, 'core/fitflix.html', {'exercicios': videos})


# =========================
# CRIAR EXERCICIO (FITFLIX)
# =========================
@login_required
def criar_exercicio(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        grupo_muscular = request.POST.get('grupo_muscular')
        imagem = request.FILES.get('imagem')
        gif = request.FILES.get('gif')

        exercicio = VideoExercicio.objects.create(
            nome=nome,
            grupo_muscular=grupo_muscular,
            imagem=imagem
        )

        if gif:
            VariacaoExercicio.objects.create(
                exercicio=exercicio,
                nome='Padrao',
                gif=gif
            )

        messages.success(request, 'Exercicio criado com sucesso!')
        return redirect('core:fitflix')

    return render(request, 'core/criar_exercicio.html')

# ==================
# ALUNO
# ==================
def grafico_aluno(request, usuario_id):
    return render(request, 'core/grafico_aluno.html')


# =================
# AVALIACAO CRIANCA
# =================
def criar_avaliacao_crianca(request):
    if request.method == 'POST':
        avaliacao_form = AvaliacaoFisicaForm(request.POST)
        form = AvaliacaoCriancaForm(request.POST)

        if avaliacao_form.is_valid() and form.is_valid():
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()

            crianca = form.save(commit=False)
            crianca.avaliacao = avaliacao
            crianca.save()

            return redirect('core:avaliacoes')

    else:
        avaliacao_form = AvaliacaoFisicaForm()
        form = AvaliacaoCriancaForm()

    return render(request, 'core/criar_avaliacao_crianca.html', {
        'avaliacao_form': avaliacao_form,
        'form': form
    })


# ================
# AVALIACAO IDOSO
# ================
def criar_avaliacao_idoso(request):
    if request.method == 'POST':
        avaliacao_form = AvaliacaoFisicaForm(request.POST)
        circ_form = CircunferenciaForm(request.POST)
        form = AvaliacaoIdosoForm(request.POST)

        if avaliacao_form.is_valid() and form.is_valid() and circ_form.is_valid():
            avaliacao = avaliacao_form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.save()

            circ = circ_form.save(commit=False)
            circ.avaliacao = avaliacao
            circ.save()

            idoso = form.save(commit=False)
            idoso.avaliacao = avaliacao
            idoso.save()

            return redirect('core:avaliacoes')

    else:
        avaliacao_form = AvaliacaoFisicaForm()
        circ_form = CircunferenciaForm()
        form = AvaliacaoIdosoForm()

    return render(request, 'core/criar_avaliacao_idoso.html', {
        'avaliacao_form': avaliacao_form,
        'circ_form': circ_form,
        'form': form
    })


# ===============
# ESCOLHER TIPO
# ===============
def escolher_tipo(request):
    return render(request, 'core/escolher_tipo.html')


# ==================
# TREINO
# ==================
def treino_detail(request, treino_id):
    treino = get_object_or_404(
        Treino, 
        id=treino_id,
        aluno__usuario=request.user
    )
    itens = treino.exercicios.all().order_by('ordem')

    return render(request, 'core/treino_detail.html', {
        'treino': treino,
        'itens': itens
    })


@login_required
def editar_treino(request, treino_id):
    treino = get_object_or_404(
        Treino.objects.select_related('aluno'),
        id=treino_id,
        aluno__usuario=request.user,
    )

    if request.method == 'POST':
        form = TreinoForm(request.POST, instance=treino)
        formset = ExercicioTreinoFormSet(request.POST, instance=treino, prefix='exercicios')

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                treino = form.save()
                ordem = 1
                for exercicio_form in formset.forms:
                    if not hasattr(exercicio_form, 'cleaned_data') or not exercicio_form.cleaned_data:
                        continue

                    if exercicio_form.cleaned_data.get('DELETE'):
                        continue

                    exercicio = exercicio_form.save(commit=False)

                    if not exercicio.exercicio_id or not exercicio.variacao_id:
                        continue

                    exercicio.treino = treino
                    exercicio.ordem = ordem
                    exercicio.save()
                    ordem += 1

                for exercicio in formset.deleted_objects:
                    exercicio.delete()

                formset.save_m2m()

            messages.success(request, 'Treino atualizado com sucesso!')
            return redirect('core:treino_detail', treino_id=treino.id)
    else:
        form = TreinoForm(instance=treino)
        formset = ExercicioTreinoFormSet(instance=treino, prefix='exercicios')

    return render(request, 'core/criar_treino.html', {
        'form': form,
        'formset': formset,
        'treino': treino,
        'modo_edicao': True,
    })


# ==================
# CALCULO DE DOBRAS
# ==================
def calcular_composicao(avaliacao):
    adip = avaliacao.adipometria

    if not adip:
        return None

    soma = (
        (adip.tricipital or 0) +
        (adip.subescapular or 0) +
        (adip.supra_iliaca or 0) +
        (adip.coxa or 0) +
        (adip.abdominal or 0) +
        (adip.peito or 0) 
    )

    peso = avaliacao.peso or 0
    if soma == 0:
        return None

    percentual = soma * Decimal('0.153')
    massa_gorda = (percentual / 100) * peso

    if avaliacao.sexo == 'M':
        percentual_residual = Decimal('0.24')
    else:
        percentual_residual = Decimal('0.20')

    massa_residual = peso * percentual_residual
    massa_magra = peso - (massa_gorda + massa_residual)

    return {
        "percentual": round(percentual, 2),
        "massa_gorda": round(massa_gorda, 2),
        "massa_magra": round(massa_magra, 2),
        "massa_residual": round(massa_residual)
    }

# =====================
# FIT FLIX
# ====================

@login_required
def fitflix(request):
    from django.db.models import Prefetch

    # Buscar todos os exercicios com suas variações
    exercicios = VideoExercicio.objects.prefetch_related('variacoes').all()

    # Mapeamento de sinônimos para nomes padronizados
    sinonimos = {
        'peito': 'Peito',
        'peitoral': 'Peito',
        'costas': 'Costas',
        'dorsal': 'Costas',
        'pernas': 'Pernas',
        'inferiores': 'Pernas',
        'ombros': 'Ombros',
        'ombro': 'Ombros',
        'deltoide': 'Ombros',
        'biceps': 'Biceps',
        'bíceps': 'Biceps',
        'triceps': 'Triceps',
        'tríceps': 'Triceps',
        'abdomen': 'Abdomen',
        'abdômen': 'Abdomen',
        'core': 'Abdomen',
    }

    # Agrupar exercicios
    grupos_dict = {}
    for ex in exercicios:
        grupo_lower = ex.grupo_muscular.lower()

        # Padronizar o nome do grupo
        if grupo_lower in sinonimos:
            nome_padrao = sinonimos[grupo_lower]
        else:
            nome_padrao = ex.grupo_muscular.title()

        if nome_padrao not in grupos_dict:
            grupos_dict[nome_padrao] = {
                'nome': nome_padrao,
                'exercicios': []
            }
        grupos_dict[nome_padrao]['exercicios'].append(ex)

    # Ordem personalizada dos grupos
    ordem = ['Peito', 'Costas', 'Pernas', 'Ombros', 'Biceps', 'Triceps', 'Abdomen']

    # Criar lista ordenada
    grupos = []
    for nome in ordem:
        if nome in grupos_dict:
            grupos.append(grupos_dict[nome])
            del grupos_dict[nome]

    # Adicionar grupos restantes
    for nome, dados in grupos_dict.items():
        grupos.append(dados)

    return render(request, 'core/fitflix.html', {
        'grupos': grupos,
        'todos_exercicios': exercicios,
    })


    # CRIAR TREINO
@login_required
def criar_treino(request):
    if request.method == 'POST':
        form = CriarTreinoForm(request.POST, usuario=request.user)
        if form.is_valid():
            treino = Treino.objects.create(
                nome=form.cleaned_data['nome'],
                aluno=form.cleaned_data['aluno'],
            )
            return redirect('core:editar_treino', treino.id)
    else:
        form = CriarTreinoForm(usuario=request.user)

    return render(request, 'core/criar_treino.html', {
        'form': form,
        'modo_edicao': False,
    })


#--PAINEL DO ALUNO--

def painel_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    treinos = Treino.objects.filter(aluno=aluno)

    return render(request, 'core/painel_aluno.html', {
        'aluno': aluno,
        'treinos': treinos
    })
