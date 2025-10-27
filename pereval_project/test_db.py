import os
import django
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pereval_project.settings')  # ← замените 'your_project' на имя вашей папки с settings.py
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print("✅ Подключение к БД успешно!")
        print(cursor.fetchone())
except Exception as e:
    print("❌ Ошибка:", e)