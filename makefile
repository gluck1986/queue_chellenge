install:
	pip install -r requirements.txt

.PHONY: run

# Извлекаем все цели, которые были указаны после run
ARGS := $(filter-out run,$(MAKECMDGOALS))
# Если ARGS не пуст, берем первый элемент. Иначе используем 1.
num := $(if $(ARGS),$(firstword $(ARGS)),1)

run:
	@echo "Using num = $(num)"
	python main.py $(num)

# Этот псевдотаргет нужен, чтобы make не ругался на несуществующие цели
%:
	@: