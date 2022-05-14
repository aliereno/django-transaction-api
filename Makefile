connect-docker:
	docker-compose -f docker-compose.yml exec app bash
migrate:
	docker-compose -f docker-compose.yml exec app bash -c "python manage.py migrate"
makemigrations:
	docker-compose -f docker-compose.yml exec app bash -c "python manage.py makemigrations"
up:
	docker-compose up -d
