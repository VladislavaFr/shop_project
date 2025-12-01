import os
from django.core.wsgi import get_wsgi_application

# Устанавливаем модуль настроек по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')

# Создаём WSGI-приложение
application = get_wsgi_application()
