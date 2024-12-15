# Установка и запуск
## Запуск локально

установка зависимостей
```shell
make install
```

запуск с числом потоков по умолчанию
```shell
make run
```
или запуск с определенным числом потоко
```shell
make run 5
```


## Запуск через докер

```shell
make docker-build
```

запуск с числом потоков по умолчанию
```shell
make docker-run
```
или запуск с определенным числом потоков
```shell
make docker-run 5
```

# Как пользоваться
## интерфейс
приложение имеет консольный псевдографический интерфейс
- В верхней части консоли находится состояние приложения, которое обновляется раз в секунду
- в центре находится лог на 8 строк который обновляется по мере работы приложения
- в нижней части находится строка для ввода комманд

## команды
add 10 - добавить задание длительностью 10 сек
add 10 5 - добавить задание длительностью 10 и приоритетом 5
exit - завершить работу дождавшись завершения всех заданий которые уже находятся в процессе исполнения

## приоритеты
по умолчанию приоритет 99
чем меньше значение приоритета - тем раньше задание попадет в обработку