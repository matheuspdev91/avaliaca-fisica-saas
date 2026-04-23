from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treino',
            name='descricao',
            field=models.TextField(default=''),
        ),
    ]