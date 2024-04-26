from fastapi import FastAPI, HTTPException, Response
from jinja2 import Template
import logging
import os
import redis

app = FastAPI()

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
#redis_client = redis.Redis(host=redis_host, decode_responses=True)

# ------- Health Check ------- #
# Define the filter
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"

# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# Define the API endpoints
@app.get('/health')
def health():
    print('health endpoint')
    return {"Message": "OK"}

@app.get('/test')
def test():
    print('test endpoint')
    return {"Message": "OK"}

@app.get('/redis-ping')
def redisping():
    #return "Redis Ping"
    return "Redis ping:{}".format(redis_client.ping())


@app.get('/redis-set')
def redisset():
    redis_client.set('foo','bar')

@app.get('/redis-get')
def redisget():
    redis_client.get('foo')
    return 'Getting Redis data: {}'.format(redis_client.get('foo'))



# ------------------------------

@app.post('/generate-sql-script')
async def generate_sql_script(data: dict):
    database = data['database']
    role = data['role']
    user = data['user']
    user_pass = data['user_pass']
    template_name = data['template']

    # Fetch template from Redis
    template_content = redis_client.get(template_name)
    if not template_content:
        raise HTTPException(status_code=404, detail='Template not found in Redis')

    #template = Template(template_content.decode())
    template = Template(template_content)
    rendered_sql_script = template.render(
        app_database=database,
        app_role=role,
        app_user=user,
        app_user_pass=user_pass,
    )

    # Return the rendered script as a download
    response = Response(content=rendered_sql_script)
    response.headers['Content-Disposition'] = f'attachment; filename="{template_name}.sql"'
    response.headers['Content-Type'] = 'application/octet-stream'
    return response

if __name__ == '__main__':
    app.run(debug=True)