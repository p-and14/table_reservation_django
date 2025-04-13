# Table Reservation
Cервис бронирования столиков в ресторане
________
## Stack:
- python 3.13.2
- pydantic 2.11.2
- django 5.2
- djangorestframework 3.16.0
- drf-spectacular 0.28.0
- pytest 8.3.5
- postgres
________
## Project launch:
1. Создать виртуальное окружение.
2. Установить зависимости:
> pip install -r requirements.txt
3. Создать ".env" файл на примере ".env.example".
4. Создать БД:
   1. Установить к себе на компьютер по инструкции из [официальной документации](https://www.postgresql.org/download/). 
   2. Установить docker-контейнер с уже готовой и настроенной СУБД. 
    > docker run --name tr-postgres -e POSTGRES_PASSWORD=postgres -e TZ=Europe/Moscow -p 5432:5432 -d postgres
5. Применить все миграции:
> python manage.py migrate
6. Запуск приложения:
> python manage.py runserver

## Project launch with Docker:
1. Создать ".env" файл на примере ".env.example".
2. Запустить команду:
> docker compose up -d

## Swagger URL:
> api/schema/swagger-ui/
