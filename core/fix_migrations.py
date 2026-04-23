from django.db import connection


def fix_broken_migration():
    """
    Marca migration problemática como aplicada direto no banco
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            SELECT 'core', '0006_remove_exerciciotreino_nome', NOW()
            WHERE NOT EXISTS (
                SELECT 1 FROM django_migrations
                WHERE app='core' AND name='0006_remove_exerciciotreino_nome'
            );
        """)