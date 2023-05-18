# Microservice «Quiz»

Микросервис «Опросы»

Конфигурационный файл с переменными окружения должен находиться по пути "Quiz/quiz/backend/.env".

В нём находятся следующие переменные:

- ```HOST``` — хост этого микросервиса для invite-ссылок на опрос
- ```PORT``` — порт этого микросервиса для invite-ссылок на опрос

- ```WORKERS_PER_CORE```
- ```WEB_CONCURRENCY```
- ```SQLALCHEMY_DATABASE_URL```="sqlite+aiosqlite:///app/storage/quizzes_databases.db" — путь к базе данных
- ```BEARER_TOKEN``` — токен доступа к микросервису Пользователь
- ```TOKEN_SERVICE_URL```="185.46.11.65:80" — ссылка на микросервис Пользователь
- ```COUNT_TESTS_SERVICES```=5 — количество тестов (+ микросервис Анкета)
- ```REQUESTS_EXPIRATION_TIME_IN_MINUTES```


- ```TEST_SERVICES_BEARER_TOKEN``` — токен доступа к микросервисам Тестов
- ```TEST_SERVICE_URL``` — ссылка на api compose микросервисов Тестов


- ```BURNOUT_SERVICE_NAME``` — название теста
- ```BURNOUT_SERVICE_URL``` — ссылка на тест выгорания


- ```FATIGUE_SERVICE_NAME```
- ```FATIGUE_SERVICE_URL```


- ```COPING_SERVICE_NAME```
- ```COPING_SERVICE_URL```


- ```SPB_SERVICE_NAME```
- ```SPB_SERVICE_URL```

- ```QUESTIONNAIRE_SERVICE_NAME```
- ```QUESTIONNAIRE_SERVICE_URL```


# Запуск

Чтобы запустить проект, воспользуйтесь командой ```docker-compose build``` и затем ```docker-compose up``` из папки Quiz/
