#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cernyrobin_django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def exit_handler(sig, frame):
    print("Exiting..")

    from api.models import Job

    for job in Job.objects.all():
        job.delete()

    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

if __name__ == '__main__':
    main()