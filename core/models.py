from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import AbstractUser


# ========================
# USUÁRIO
# ========================
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    cref = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# ========================
# AVALIAÇÃO BASE (ADULTO)
# ========================
class AvaliacaoFisica(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    data_nascimento = models.DateField()

    altura = models.DecimalField(max_digits=4, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    objetivo = models.TextField(blank=True)
    percentual_gordura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.criado_em.strftime('%d/%m/%Y')}"

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def imc(self):
        try:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        except:
            return None


# ========================
# CIRCUNFERÊNCIAS
# ========================
class Circunferencia(models.Model):
    avaliacao = models.OneToOneField(
        AvaliacaoFisica,
        on_delete=models.CASCADE,
        related_name='circunferencias'
    )
    ombros = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    torax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cintura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    abdome = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    quadril = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    braco_direito = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    braco_esquerdo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    coxa_direita = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    coxa_esquerda = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    panturrilha_direita = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    panturrilha_esquerda = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


# ========================
# ADIPOMETRIA
# ========================
class Adipometria(models.Model):
    avaliacao = models.OneToOneField(
        'AvaliacaoFisica',
        on_delete=models.CASCADE,
        related_name='adipometria'
    )

    tricipital = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    subescapular = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    supra_iliaca = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    coxa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peito = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    axilar_media = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Adipometria - Avaliação {self.avaliacao.id}'


# ========================
# CRIANÇA
# ========================
class AvaliacaoCrianca(models.Model):
    avaliacao = models.OneToOneField(
        AvaliacaoFisica,
        on_delete=models.CASCADE,
        related_name='crianca'
    )

    coordenacao = models.CharField(max_length=20)
    equilibrio_segundos = models.FloatField()
    flexoes = models.IntegerField()
    agilidade_tempo = models.FloatField()
    salto_horizontal = models.FloatField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Criança - {self.avaliacao.nome}"

    @property
    def imc(self):
        return self.avaliacao.imc

    @property
    def classificacao_imc(self):
        imc = self.imc
        if imc is None:
            return None
        if imc < 14:
            return "Baixo peso"
        elif imc < 18:
            return "Normal"
        elif imc < 22:
            return "Sobrepeso"
        return "Obesidade"

    @property
    def classificacao_altura(self):
        altura = float(self.avaliacao.altura)
        idade = self.avaliacao.idade
        if idade < 10 and altura < 1.2:
            return "Baixa estatura"
        return "Adequado"

    @property
    def nivel_motor(self):
        if self.flexoes < 5:
            return 'Baixo'
        elif self.flexoes < 10:
            return 'Moderado'
        return 'Bom'


# ========================
# IDOSO
# ========================
class AvaliacaoIdoso(models.Model):
    avaliacao = models.OneToOneField(
        AvaliacaoFisica,
        on_delete=models.CASCADE,
        related_name='idoso'
    )

    sentar_levantar = models.IntegerField()
    tug_tempo = models.FloatField()
    equilibrio_segundos = models.FloatField()
    caminhada_6min = models.IntegerField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Idoso - {self.avaliacao.nome}"

    @property
    def panturrilha_media(self):
        try:
            circ = self.avaliacao.circunferencias
            valores = [
                circ.panturrilha_direita,
                circ.panturrilha_esquerda
            ]
            valores_validos = [float(v) for v in valores if v]
            if not valores_validos:
                return None
            return round(sum(valores_validos) / len(valores_validos), 2)
        except:
            return None

    @property
    def diagnostico_sarcopenia(self):
        pant = self.panturrilha_media
        if pant is None:
            return 'Sem dados'
        if pant < 31:
            return 'Risco de sarcopenia'
        return 'Normal'

    @property
    def classificacao_risco_queda(self):
        if self.tug_tempo > 12:
            return "Alto"
        elif self.tug_tempo > 9:
            return "Moderado"
        return "Baixo"

    @property
    def diagnostico_funcional(self):
        if self.diagnostico_sarcopenia == 'Risco de sarcopenia' or self.tug_tempo > 12:
            return "Alto risco funcional"
        elif self.tug_tempo > 9:
            return "Risco moderado"
        return "Baixo risco"


# ========================
# FIT FLIX
# ========================
class VideoExercicio(models.Model):
    nome = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='exercicios/imagem/', null=True, blank=True)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class VariacaoExercicio(models.Model):
    exercicio = models.ForeignKey(
        VideoExercicio,
        on_delete=models.CASCADE,
        related_name='variacoes'
    )
    nome = models.CharField(max_length=100)
    gif = models.ImageField(upload_to='exercicios/gif/')
    grupo_muscular = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.exercicio.nome} - {self.nome}"


class Aluno(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome


class Treino(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.aluno.nome}"


class ExercicioTreino(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(VideoExercicio, on_delete=models.CASCADE)
    variacao = models.ForeignKey(VariacaoExercicio, on_delete=models.CASCADE)
    series = models.IntegerField()
    repeticoes = models.IntegerField()
    descanso = models.IntegerField(help_text='em segundos')
    carga = models.CharField(max_length=50, blank=True)
    ordem = models.IntegerField()

    def __str__(self):
        return f"{self.treino.nome} - {self.exercicio.nome}"