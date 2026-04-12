from datetime import date

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_aluno_data_nascimento_remove_aluno_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='telefone',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='data_nascimento',
            field=models.DateField(default=date(2000, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='objetivo',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aluno',
            name='observacoes',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
