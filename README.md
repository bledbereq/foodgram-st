1. Находясь в главной дериктории ```/```, создайте файл под названием ```.env```

2. Ставьте в файл ```.env```

    a. Настройки СУБД PostgreSQL:

    file name: ```.env```
    ```
    NAME=foodgram_db
    USER=admin
    PASSWORD=root
    HOST=postgres
    PORT=5432
    ```
    b. А также настройки бэкенда:

    file name: ```.env```
    ```
    SECRET_KEY="secretKey"
    ALLOWED_HOSTS="127.0.0.1 localhost"
    CSRF_TRUSTED_ORIGINS="http://127.0.0.1 http://localhost"
    DEBUG=True
    ```

**Вы можете ставить свои значения, но не забудте поменять ```docker-compose``` файл для СУБД*

---

3. После этого перейдите в директорию ```/infra``` и запустите ```docker-compose``` файл bash-командой 
```
docker compose up
```
