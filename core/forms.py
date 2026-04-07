from django import forms
from .models import (
    AvaliacaoFisica,
    Circunferencia,
    Adipometria,
    AvaliacaoCrianca,
    AvaliacaoIdoso
)


class AvaliacaoFisicaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoFisica
        exclude = ('usuario', 'criado_em')


class CircunferenciaForm(forms.ModelForm):
    class Meta:
        model = Circunferencia
        exclude = ('avaliacao',)


class AdipometriaForm(forms.ModelForm):
    class Meta:
        model = Adipometria
        exclude = ('avaliacao',)


class AvaliacaoCriancaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoCrianca
        exclude = ('avaliacao',)


class AvaliacaoIdosoForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoIdoso
        field = '__all__'
        exclude = ('avaliacao',)

class CircunferenciaForm(forms.ModelForm):
    class Meta:
        model = Circunferencia
        exclude = ['avaliacao']
        