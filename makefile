.PHONY: build up down restart shell


build:
	docker-compose build


up:
	docker-compose up -d


down:
	docker-compose down


restart: down up


shell:
	docker-compose exec backend sh



