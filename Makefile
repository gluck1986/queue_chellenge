install:
	pip install -r requirements.txt
.PHONY: run docker-run

# Извлекаем аргументы для каждой цели отдельно
ARGS_RUN := $(filter-out run,$(MAKECMDGOALS))
ARGS_DOCKER_RUN := $(filter-out docker-run,$(MAKECMDGOALS))

# Если аргументов для run нет, то num_run=1, иначе берем первый
num_run := $(if $(ARGS_RUN),$(firstword $(ARGS_RUN)),1)
# Аналогично для docker-run
num_docker_run := $(if $(ARGS_DOCKER_RUN),$(firstword $(ARGS_DOCKER_RUN)),1)

run:
	python main.py $(num_run)

docker-run:
	docker run --rm -it myapp:latest python main.py $(num_docker_run)
docker-build:
	docker build -t myapp:latest .


# Данный псевдотаргет нужен, чтобы make не ругался на несуществующие цели,
# созданные при вызове типа `make docker-run 10`
%:
	@:

# Этот псевдотаргет нужен, чтобы make не ругался на несуществующие цели
%:
	@: