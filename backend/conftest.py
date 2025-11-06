"""
Configuração do pytest para o projeto ihelp.
"""
import os

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ihelp.settings')
django.setup()
