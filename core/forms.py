from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import (
    Adipometria,
    Aluno,
    AvaliacaoCrianca,
    AvaliacaoFisica,
    AvaliacaoIdoso,
    Circunferencia,
    ExercicioTreino,
    Treino,
    VariacaoExercicio,
    VideoExercicio,
)

User = get_user_model()


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


class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['nome']
        labels = {
            'nome': 'Nome do treino',
        }


class CriarTreinoForm(forms.Form):
    nome = forms.CharField(
        label='Nome do treino',
        max_length=100,
    )
    aluno = forms.ModelChoiceField(
        label='Aluno',
        queryset=Aluno.objects.none(),
        empty_label='Selecione um aluno',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['aluno'].queryset = Aluno.objects.filter(user=user).order_by('nome')


class CriarAlunoForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'telefone', 'data_nascimento', 'objetivo', 'observacoes']
        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de nascimento',
            'objetivo': 'Objetivo',
            'observacoes': 'Observacoes',
        }
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'objetivo': forms.TextInput(attrs={'placeholder': 'Ex: Ganho de massa muscular'}),
            'observacoes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Informacoes adicionais'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].required = False
        self.fields['objetivo'].required = False
        self.fields['observacoes'].required = False

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ja existe um usuario cadastrado com este email.')
        return email


class ExercicioTreinoForm(forms.ModelForm):
    class Meta:
        model = ExercicioTreino
        fields = [
            'exercicio',
            'variacao',
            'series',
            'repeticoes',
            'descanso',
            'carga',
        ]
        labels = {
            'exercicio': 'Exercício',
            'variacao': 'Variação',
            'series': 'Séries',
            'repeticoes': 'Repetições',
            'descanso': 'Descanso (segundos)',
            'carga': 'Carga',
        }
        widgets = {
            'exercicio': forms.Select(),
            'variacao': forms.Select(),
            'series': forms.NumberInput(attrs={'min': 1}),
            'repeticoes': forms.NumberInput(attrs={'min': 1}),
            'descanso': forms.NumberInput(attrs={'min': 0}),
            'carga': forms.TextInput(attrs={'placeholder': 'Ex: 20kg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercicio'].queryset = VideoExercicio.objects.order_by('nome')
        self.fields['variacao'].queryset = VariacaoExercicio.objects.select_related('exercicio').order_by(
            'exercicio__nome', 'nome'
        )


ExercicioTreinoFormSet = inlineformset_factory(
    Treino,
    ExercicioTreino,
    form=ExercicioTreinoForm,
    extra=1,
    can_delete=True,
)
