
docker-run:
	docker compose -f docker-compose.yml up --watch

docker-stop:
	docker-compose down -v --rmi 'all'

.PHONY: docker-run docker-stop
