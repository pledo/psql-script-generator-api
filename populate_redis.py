import os
import requests
import redis

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
#redis_password = os.getenv('REDIS_PASSWORD', None)
#creds_provider = redis.UsernamePasswordCredentialProvider("username", "password")
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# GitHub repository information
github_repo_owner = 'pledo'
github_repo_name = 'psql-script-generator'
branch_name = 'main'
folder_path = 'src/cli/templates'

# GitHub API URL to get the contents of a directory
github_api_url = f'https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path}?ref={branch_name}'
response = requests.get(github_api_url)

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