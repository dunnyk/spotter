migrations:
	python manage.py makemigrations
migrate:
	python3 manage.py migrate
collectstatic:
	python manage.py collectstatic
server:
	python3 manage.py runserver
superuser:
	python manage.py createsuperuser
shell:
	python3 manage.py shell