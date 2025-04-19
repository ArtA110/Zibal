.PHONY: build up down restart shell calculate_transaction_summaries


build:
	docker-compose build


up:
	docker-compose up -d


down:
	docker-compose down


restart: down up


shell:
	docker-compose exec backend sh

calculate_transaction_summaries:
	docker-compose exec backend python core/manage.py calculate_transaction_summaries

