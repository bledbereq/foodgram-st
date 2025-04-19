1. Находясь в дериктории ```/infra```, создайте файл под названием ```.env```

2. Ставьте в файл ```.env```

    ```
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password
    POSTGRES_DB=foodgram
    SECRET_KEY=you_key
    DB_HOST=db
    DB_PORT=5432
    ```

3. После этого перейдите в директорию ```/infra``` и запустите ```docker-compose``` файл bash-командой 
    ```
    docker compose up
    ```
4. Перейдите ```http://localhost/```
___


Для работы напанели админа, нам необходимо также перейти в дерикторию ```/infra```, где уже запущен ```docker-compose``` файл.
Выполните bash-команду:
```
docker-compose exec backend python manage.py createsuperuser
```
После того как заполните все поля, можете перейти в ```http://localhost/admin``` и зайти с помощью ранее зарегестрированного суперпользователя

---
О работе:
- Все postman-тесты успешно пройдены
