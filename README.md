# BuggerNews django

### Setup

```bash
cp .env.example .env
vim .env
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```
