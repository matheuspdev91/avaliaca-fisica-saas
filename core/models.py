from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    cref = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


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
    criado_em = models.DateTimeField(auto_now_add=True)
    percentual_gordura = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.nome} - {self.criado_em.strftime('%d/%m/%Y')}"

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    @property
    def percentual(self):
        try:
            adip = self.adipometria

            soma = (
                float(adip.peito or 0) +
                float(adip.axilar_media or 0) +
                float(adip.triciptal or 0) +
                float(adip.subescapular or 0) +
                float(adip.abdominal or 0) +
                float(adip.supra_iliaca or 0) +
                float(adip.coxa or 0)
            )

            idade = self.idade

            if self.sexo == 'M':
                densidade = (
                    1.112
                    - (0.00043499 * soma)
                    + (0.00000055 * soma ** 2)
                    - (0.00028826 * idade)
                )
            else:
                densidade = (
                    1.097
                    - (0.00046971 * soma)
                    + (0.00000056 * soma ** 2)
                    - (0.00012828 * idade)
                )

            gordura = ((4.95 / densidade) - 4.50) * 100
            return round(gordura, 2)

        except Exception:
            return None

    # 🔥 AGORA CORRETAMENTE DENTRO DA CLASSE
    
    @property
    def massa_gorda(self):
        percentual = self.percentual
        if percentual is not None:
            return round(float(self.peso) * (percentual / 100), 2)
        return None

    @property
    def massa_magra(self):
        mg = self.massa_gorda
        if mg is not None:
            return round(float(self.peso) - mg, 2)
        return None


    @property
    def massa_residual(self):
        if self.sexo == 'F':
            return round(float(self.peso) * 0.241,2)
        else:
            return round(float(self.peso) * 0.269,2)


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

    def __str__(self):
        return f'Circunferências - Avaliação {self.avaliacao.id}'


class Adipometria(models.Model):
    avaliacao = models.OneToOneField(
        AvaliacaoFisica,
        on_delete=models.CASCADE,
        related_name='adipometria'
    )

    triciptal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    subescapular = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    supra_iliaca = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    coxa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peito = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    axilar_media = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'Adipometria - Avaliação {self.avaliacao.id}'
