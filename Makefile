dev:
	poetry run flask --app documents_merger:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) documents_merger:app

install:
	poetry install

lint:
	poetry run flake8

.PHONY: install lint start dev