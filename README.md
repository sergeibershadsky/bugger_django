# BuggerNews django

### Setup

```bash
cp .env.example .env
vim .env
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

###

To get fresh articles:

```bash
curl -X http://localhost/posts/
```

or using httpie
```bash
http http://localhost/posts/
```

Force refresh articles
```bash
curl -X http://localhost/force-refresh/
or
http http://localhost/force-refresh/
```
