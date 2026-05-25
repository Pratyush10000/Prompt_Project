"""
WSGI entry point for Gunicorn.

Launch:
    gunicorn --chdir /path/to/phq9_app wsgi:app --bind 0.0.0.0:5000 --workers 2
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import create_app

app = create_app()
