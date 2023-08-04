1. Start Postgres and Redis instances:

```sh
sudo docker run -d \
  --name=postgres \
  --restart=unless-stopped \
  -e POSTGRES_PASSWORD= \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15


export FLASK_APP=app.py  
flask db init  
flask db migrate -m "create mj table"
flask db upgrade    


tail -f output.log
