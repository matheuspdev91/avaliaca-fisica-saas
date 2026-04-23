from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_treino_descricao'),
    ]

    # `token` is already created in `0001_initial`. This migration remains only
    # to preserve numbering in existing environments.
    operations = []
