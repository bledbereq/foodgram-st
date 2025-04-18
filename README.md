1. Находясь в дериктории ```/infra```, создайте файл под названием ```.env```

2. Ставьте в файл ```.env```

    a. Настройки СУБД PostgreSQL:

    file name: ```.env```
    ```
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password
    POSTGRES_DB=foodgram
    SECRET_KEY=you_key
    DB_HOST=db
    DB_PORT=5432
    ```

**Вы можете ставить свои значения, но не забудте поменять ```docker-compose``` файл для СУБД*

---

3. После этого перейдите в директорию ```/infra``` и запустите ```docker-compose``` файл bash-командой 
```
docker compose up
```
