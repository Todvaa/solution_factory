# solution_factory
## Стэк
- Django
- Celery
- Flower
- Redis
- PostgreSql
## Описание
Сервис для рассылки сообщений клиентам. Создание новой рассылки реализовано с помощью API. 
Полная документация API доступна после запуска проекта по адресу http://localhost:8000/docs/.
При создании нового объекта "рассылка", всем подходящим под фильтр клиентам будет отправлено "сообщение", если 
дата и время запуска "рассылки" наступило по локальному времени "клиента". В случае когда время еще не наступило,
"сообщение" отправится автоматически по наступлению. Если по каким-то причинам сообщения не были доставлены до 
даты и времени  окончания "рассылки", "сообщения" клиентам доставлены не будут.
Для отслеживания состояния задач по отправке сообщений после запуска проекта доступен интерфейс flower по адресу
http://localhost:5555/. 
В проекте настроен docker-compose, что упрощает начало работы

Сущность "рассылка" имеет атрибуты:
- уникальный id рассылки
- дата и время запуска рассылки
- текст сообщения для доставки клиенту
- фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
- дата и время окончания рассылки  

Сущность "клиент" имеет атрибуты:
- уникальный id клиента
- номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
- код мобильного оператора
- тег (произвольная метка)
- часовой пояс

Сущность "сообщение" имеет атрибуты:
- уникальный id сообщения
- дата и время создания (отправки)
- статус отправки
- id рассылки, в рамках которой было отправлено сообщение
- id клиента, которому отправили


## Запуск
1. Установить:
* <a href=https://www.docker.com/get-started>Docker</a>
* <a href=https://docs.docker.com/compose/install/>Docker-compose</a>  
2. Создать и заполнить ".env"
<br><pre>cp .env.dist .env</pre><br>
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=solution_factory
POSTGRES_USER=solution_factory
POSTGRES_PASSWORD=solution_factory
DB_HOST=db # имя контейнера базы данных
DB_PORT=5432
SECRET_KEY= # секретный ключ Django
JWT_TOKEN= # jwt токен от сервиса отправки сообщений
MESSAGE_SERVICE_URL=https://probe.fbrq.cloud/v1/send/
```
3. Собрать контейнеры. Запуск из корневой папки проекта.  
<br><pre>docker-compose up --build</pre><br> 

#solution_factory
## Stack
- Django
- Celery
-Flower
- Redis
- PostgreSQL
## Description
Service for sending messages to customers. The creation of a new mailing list is implemented using the API.
Full API documentation is available after starting the project at http://localhost:8000/docs/.
When creating a new "mailing_list" object, a "message" will be sent to all clients matching the filter, if
the date and time of the launch of the "mailing_list" has come according to the local time of the "client". When the time has not yet come,
"mail" will be sent automatically upon occurrence. If for some reason the messages were not delivered before
date and time of the end of the "mailing_list", "messages" will not be delivered to customers.
To track the status of tasks for sending messages after the project is launched, the flower interface is available at
http://localhost:5555/.
The project is configured with docker-compose, making it easy to get started

The "mailing_list" entity has the following attributes:
- unique mailing id
- date and time of the mailing start
- text of the message to be delivered to the client
- filter properties of clients to which the mailing should be made (mobile operator code, tag)
- date and time of the end of the mailing

The "client" entity has the following attributes:
- unique client id
- customer's phone number in the format 7XXXXXXXXXX (X is a number from 0 to 9)
- mobile operator code
- tag (arbitrary label)
- Timezone

The "mail" entity has the following attributes:
- unique message id
- date and time of creation (sending)
- sending status
- id of the distribution within which the message was sent
- id of the client to whom it was sent


## Run
1. Install:
* <a href=https://www.docker.com/get-started>Docker</a>
* <a href=https://docs.docker.com/compose/install/>Docker-compose</a>
2. Create and fill ".env"
<br><pre>cp .env.dist .env</pre><br>
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=solution_factory
POSTGRES_USER=solution_factory
POSTGRES_PASSWORD=solution_factory
DB_HOST=db # datebase container name
DB_PORT=5432
SECRET_KEY= # Django secret key
JWT_TOKEN= # jwt token from the messaging service
MESSAGE_SERVICE_URL=https://probe.fbrq.cloud/v1/send/
```
3. Collect containers. Run from the root folder of the project.
<br><pre>docker-compose up --build</pre><br>
