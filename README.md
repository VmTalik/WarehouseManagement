# Warehouse Management

### Описание
Веб-сервис, предоставляющий REST API для управления процессами на складе. 
С помощью данного API можно управлять товарами, складскими запасами и заказами.

### Запуск сервиса
1. Поднять инфраструктуру
   ``` commandline
   docker-compose up -d
   ```
2. Для доступа к документации API перейти по ссылке http://127.0.0.1:8000/docs

### Запуск тестов
1. Поднять инфраструктуру
   ``` commandline
   docker-compose -f docker-compose.test.yaml up -d
   ```
2. Запустить тесты внутри контейнера
   ``` commandline
   docker exec -it <container_id> /bin/bash
   ```
   ``` commandline
   pytest -v -s tests/
   ```