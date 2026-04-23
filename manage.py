#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')

    import django
    django.setup()

    # 🔧 FIX: marca migration quebrada como aplicada
    try:
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                SELECT 'core', '0006_remove_exerciciotreino_nome', NOW()
                WHERE NOT EXISTS (
                    SELECT 1 FROM django_migrations
                    WHERE app='core' AND name='0006_remove_exerciciotreino_nome'
                );
            """)
    except Exception as e:
        print("Migration fix skipped:", e)

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()