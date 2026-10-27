import sys
import os

# Garante que o Apache encontre os módulos da pasta raiz do projeto
sys.path.insert(0, os.path.dirname(__file__))

# Importa a instância do Flask do seu app.py com o nome padrão exigido ('application')
from app import app as application