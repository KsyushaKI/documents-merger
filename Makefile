dev:
	poetry run flask --app document_hundler:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) document_hundler:app

install:
	poetry install

lint:
	poetry run flake8

.PHONY: install lint start dev