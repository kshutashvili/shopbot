RUN=python3 manage.py

run:
	$(RUN) runserver 0.0.0.0:8000

makemigrations:
	$(RUN) makemigrations

migrate:
	$(RUN) migrate

collectstatic:
	$(RUN) collectstatic --noinput

pip_install:
	pip install -r requirements.txt

create_admin:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | $(RUN) shell
