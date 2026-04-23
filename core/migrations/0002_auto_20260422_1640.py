from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    # `descricao` already exists in `0001_initial`. Keeping this migration as a
    # no-op preserves the deployed history without trying to add the column again.
    operations = []
