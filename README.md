# FastAPI Template
Template based on [@fastapi_production_template](https://github.com/zhanymkanov/fastapi_production_template)
and [@djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)

## Local Development

### First Build Only
1. `cp .env.example .env`
2. `docker-compose up -d --build`


### Linters
Format the code
```shell
docker compose exec app format
```

### Migrations
- Create an automatic migration from changes in `src/database.py`
```shell
docker compose exec app makemigrations *migration_name*
```
- Run migrations
```shell
docker compose exec app migrate
```
- Downgrade migrations
```shell
docker compose exec app downgrade -1  # or -2 or base or hash of the migration
```

### Tests
All tests are integrational and require DB connection. 

One of the choices I've made is to use default database (`postgres`), separated from app's `app` database.
- Using default database makes it easier to run tests in CI/CD environments, since there is no need to setup additional databases
- Tests are run with `force_rollback=True`, i.e. every transaction made is then reverted

Run tests
```shell
docker compose exec app pytest
```

