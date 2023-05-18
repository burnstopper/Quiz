# Microservice «Quiz»

Микросервис «Опросы»

Конфигурационный файл с переменными окружения должен находиться по пути "Quiz/quiz/backend/.env".

В нём находятся следующие переменные:

- HOST — хост этого микросервиса для invite-ссылок на опрос
- PORT — порт этого микросервиса для invite-ссылок на опрос

- WORKERS_PER_CORE
- WEB_CONCURRENCY
- SQLALCHEMY_DATABASE_URL="sqlite+aiosqlite:///app/storage/quizzes_databases.db" — путь к базе данных
- BEARER_TOKEN="JhbGciOiJIUzI1NiIsInR5I6IkpXVCJ9JzdWIiOiJKdXN0IGFGF2VzcyB0b2tlbiB0byBjb21t5pY2F0ZSB3dGloIFVzIifQ" — токен доступа к микросервису Пользователь
- TOKEN_SERVICE_URL="185.46.11.65:80" — ссылка на микросервис Пользователь
- COUNT_TESTS_SERVICES=5 — количество тестов (+ микросервис Анкета)


- TEST_SERVICES_BEARER_TOKEN="ycK0pFhS6akv" — токен доступа к микросервисам Тестов
- TEST_SERVICE_URL="http://194.67.126.160:8080" — ссылка на api compose микросервисов Тестов


- BURNOUT_SERVICE_NAME="Burnout" — название теста
- BURNOUT_SERVICE_URL="http://194.67.126.160:8081" — ссылка на тест выгорания


- FATIGUE_SERVICE_NAME="Fatigue"
- FATIGUE_SERVICE_URL="http://194.67.126.160:8082"


- COPING_SERVICE_NAME="Coping"
- COPING_SERVICE_URL="http://194.67.126.160:8083"


- SPB_SERVICE_NAME="SPB"
- SPB_SERVICE_URL="http://194.67.126.160:8084"


# Запуск

Чтобы запустить проект, воспользуйтесь командой ```docker-compose build``` и затем ```docker-compose up``` из папки Quiz/
