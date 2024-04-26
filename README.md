# psql-script-generator-api

### Usage

1- Clone repo and enter inside It

```bash
$ git clone -b main git@github.com:pledo/psql-script-generator-api.git 

$ cd psql-script-generator-api
```

2- Build and run the docker compose
```bash
$ docker-compose up -d --build
```

3- Call the api using curl with paremeters to get the .sql script and check the file

```bash
$ curl -o test_sql_script.sql -XPOST 'localhost:8000/generate-sql-script' \
-H 'Content-Type: application/json' \
-d '{"database":"test","role":"test_readwrite","user":"test_user","user_pass":"qweasdzxc","template":"readwrite-user-template.sql.j2"}'

$ cat test_sql_script.sql
```

4- You can run an full automated test that validate the readwrite and readonly templates. Just enter inside the tests folder and run the script
```bash
$ cd tests

$ bash full_test.sh
```