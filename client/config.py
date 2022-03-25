'''
Файл конфигурации бота
'''

import os
import sys

import django


# Токен бота
TOKEN = '5140675106:AAHe5IaSOlAnjS4ExKJ7DL_qGZ2yHQP3hx8'

PARENT_PACKAGE = '..'
# Папка Django проекта
APP_PACKAGE = 'server'
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(PARENT_DIR, APP_PACKAGE)

# Интеграция бота и Django
sys.path.append(PARENT_DIR)
sys.path.append(APP_DIR)
sys.path[0], sys.path[-1] = sys.path[-1], sys.path[0]

# Подключения Django-проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
