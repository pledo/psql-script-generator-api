# psql-script-generator-api
It generates a SQL script based on a Jinja2 template, allowing you to automate the creation of a database, roles, and permissions. It is particularly useful for setting up a PostgreSQL database with predefined roles and permissions.


#### Install the API inside your Kubernetes cluster with k8 manifests

1- Create the namespace
```bash
kubectl create ns test-apps
```

2- Create the k8 objects
```bash
kubectl create -f https://raw.githubusercontent.com/pledo/psql-script-generator-api/main/docs/k8-manifests/psql-script-generator-k8.yaml


# Testing, running port-forward

  export POD_NAME=$(kubectl get pods --namespace test-apps -l "app.kubernetes.io/name=psql-script-generator-api,app.kubernetes.io/instance=test" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace test-apps $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace test-apps port-forward $POD_NAME 8080:$CONTAINER_PORT

# health get
curl -XGET localhost:8080/health
````

2- Cleaning the environment
```bash
kubectl delete -f https://raw.githubusercontent.com/pledo/psql-script-generator-api/main/docs/k8-manifests/psql-script-generator-k8.yaml

# Deleting the namespace

kubectl delete -f https://raw.githubusercontent.com/pledo/psql-script-generator-api/main/docs/k8-manifests/psql-script-generator-k8.yaml

```

#### Install the API inside your Kubernetes cluster with Helm

1- Add the helm repo
```bash
 helm repo add test https://pledo.github.io/psql-script-generator-api
 helm repo update
```

2- Install helm package

```bash
helm install test test/psql-script-generator-api


#Custom values, you can find 3 values.yaml files that you can use, modify or 
#create new ones, and execute them, after cloning the repo, enter inside the root folder:

# Listing value files
ls -1 charts/psql-script-generator-api/|egrep -i Values
prodValues.yaml
testValues.yaml
values.yaml

# Install the chart using one of them, for example.
helm install -f charts/psql-script-generator-api/values.yaml test test/psql-script-generator-api

```

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
4- Clean up the environment
```bash
# Uninstall the test relase
helm uninstall test

# Remove the repo
helm repo remove test
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
