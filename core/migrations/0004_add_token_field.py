from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_treino_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='treino',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]