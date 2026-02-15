from django.contrib import admin
from .models import AvaliacaoFisica


class AvaliacaoFisicaAdmin(admin.ModelAdmin):
    list_display = (
    'nome',
    'peso',
    'sexo',
    'criado_em'
)
    
    search_fields = ('nome',)
    list_filter = ('sexo', 'criado_em')
    ordering = ('-criado_em',)

    #Formulário

    readonly_fields = (
    'criado_em',
    )
fieldsets = (
    ('Dados Pessoais', {
        'fields': ('nome', 'sexo', 'data_nascimento')
    }),
    ('Dados Antropométricos', {
        'fields':('altura', 'peso'),
        'classes': ('wide',),
    }),
    ('Dobras cutâneas (mm)',{
        'fields': (
            'triceps', 'subescapular', 'peitoral',
            'axilar_media', 'supra_iliaca', 
            'abdome_dobra', 'coxa_dobra'
        )
    }),
    ('Circunferência (cm)', {
        'fields': (
            'ombro', 'torax', 'cintura', 'abdome_circ',
            'quadril', 'braco_e', 'braco_d', 'coxa_e', 'coxa_d',
            'panturrilha_e', 'panturrilha_d',
        )
    }),
    ('Resultados', {
        'fields': (
            'percentual_gordura_formatado',
            'massa_gorda_formatado', 
            'massa_magra_formatado',

        )

    }),
)
admin.site.register(AvaliacaoFisica, AvaliacaoFisicaAdmin)


