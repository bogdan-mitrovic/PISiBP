#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Set default settings module
    settings_module = 'mysite.settings'  # Default to Docker settings

    # Check if "-l" flag is passed to use local settings
    if '-l' in sys.argv:
        settings_module = 'mysite.settings_local'
        # Remove the flag from sys.argv to avoid confusing Django's execute_from_command_line
        sys.argv.remove('-l')

    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
