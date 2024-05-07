# psql-script-generator-api


#### Install Install the API inside your Kubernetes cluster

1- Add the helm repo
```bash
 helm repo add test https://pledo.github.io/psql-script-generator-api
 helm repo update
```

2- Install helm package

```bash
helm install test test/psql-script-generator-api

```

3- Testing
```bash

# run the port-forward
  export POD_NAME=$(kubectl get pods --namespace test-apps -l "app.kubernetes.io/name=psql-script-generator-api,app.kubernetes.io/instance=test" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace test-apps $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace test-apps port-forward $POD_NAME 8080:$CONTAINER_PORT


# health get
curl -XGET localhost:8080/health

```

#### Local Usage

0- Make sure you have the postgres-client installed
```bash
sudo apt install postgresql-client
```
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
