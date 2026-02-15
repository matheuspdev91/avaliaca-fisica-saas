from django import forms
from .models import AvaliacaoFisica, Circunferencia, Adipometria


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
