#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(BASE_DIR, 'allunbot/.env'))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get("ENVIORMENT") )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
