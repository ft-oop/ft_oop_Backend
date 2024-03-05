NAME = APP
DOCKER_COMPOSE = ./docker-compose.yml

all :
	docker-compose -f ${DOCKER_COMPOSE} build --no-cache
	make up
up:
	docker-compose -f ${DOCKER_COMPOSE} up -d

down:
	docker-compose -f ${DOCKER_COMPOSE} down

clean:
	make down
	docker system prune -af

fclean:
	make clean
	docker-compose -f ${DOCKER_COMPOSE} down --volumes

re:
	make fclean
	make all