from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from jinja2 import Template
import os
import redis
import requests

app = FastAPI()

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
#redis_client = redis.Redis(host=redis_host, decode_responses=True)

# Github repository
github_repo_owner = os.getenv('GITHUB_REPO_OWNER', 'pledo')
github_repo_name = os.getenv('GITHUB_REPO_NAME', 'psql-script-generator')
branch_name = os.getenv('GITHUB_REPO_BRANCH', 'main')
folder_path = os.getenv('GITHUB_REPO_FOLDER_PATH', 'src/cli/templates')

class HealthCheck(BaseModel):
    status: str = "OK"


@app.get('/redis-refresh')
def redisrefresh():
    # GitHub API URL to get the contents of a directory
    github_api_url = f'https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path}?ref={branch_name}'
    response = requests.get(github_api_url)
    print(response)
    if response.status_code == 200:
        # Iterate over the files in the templates directory
        for file_info in response.json():
            file_name = file_info['name']
            file_download_url = file_info['download_url']
    
            # Download the file content
            file_content_response = requests.get(file_download_url)
            if file_content_response.status_code == 200:
                file_content = file_content_response.content.decode('utf-8')
    
                # Store the file content in Redis
                redis_client.set(file_name, file_content)
                print(f"Template '{file_name}' loaded into Redis.")
            else:
                print(f"Failed to download template '{file_name}' from GitHub.")
    else:
        print("Failed to fetch templates from GitHub.")
    print(f"Files loaded:{redis_client.keys()}")

@app.get('/list-templates')
def list_templates():
    templates = redis_client.keys()
    print(f"Current templates:{templates}")
    return templates



@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")


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

#if __name__ == '__main__':
#    app.run()
