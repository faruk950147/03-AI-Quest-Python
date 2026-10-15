 Django Commands
Maintainers may review the code and request additional changes.
# Create a virtual environment
python -m venv .venv
# Install Django
python -m pip install Django
# Check Django version
python -m django --version
# Create a project
django-admin startproject mysite .
# Create an app
python manage.py startapp polls
# Run the development server
python manage.py runserver
# Check project configuration
python manage.py check
# Create migrations
python manage.py makemigrations
# Apply migrations
python manage.py migrate
# Show migrations
python manage.py showmigrations
# Show SQL for a migration
python manage.py sqlmigrate polls 0001
# Open the Django shell
python manage.py shell
# Create a superuser
python manage.py createsuperuser
# Run tests
python manage.py test
# Collect static files
python manage.py collectstatic