import os
from app import create_app

print('flasky.py', os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
