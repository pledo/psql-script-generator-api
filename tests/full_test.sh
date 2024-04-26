#!/bin/bash

# Inside the repo's root
temp=$( realpath "$0"  ) && dirname "$temp"|cd
pwd
cd ../
pwd

echo -e "\n ### Testing"

# Create the .sql scripts
docker-compose up -d --build
sleep 5

curl -o test_sql_script.sql -XPOST 'localhost:8000/generate-sql-script' -H 'Content-Type: application/json' -d '{"database":"test","role":"test_readwrite","user":"test_user","user_pass":"qweasdzxc","template":"readwrite-user-template.sql.j2"}'
curl -o test_ro_sql_script.sql -XPOST 'localhost:8000/generate-sql-script' -H 'Content-Type: application/json' -d '{"database":"test_ro","role":"test_readonly","user":"test_ro_user","user_pass":"qweasdzxc","template":"readonly-user-template.sql.j2"}'

# Starting postgres docker container
 docker run --name psql-validating -e POSTGRES_PASSWORD=mysecretpassword -p 5555:5432 -d postgres:13 ;sleep 5

# Running the SQL script inside the postgres database
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_sql_script.sql
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_ro_sql_script.sql

#Testing the user_test grants

echo -e "\n ### Validating rw user grants ### \n"
export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d postgres -p 5555 -w -f tests/validating.sql

echo -e "\n ### Validating ro user grants ### \n"
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d test_ro -p 5555 -w -f tests/validating_setup_for_ro_user.sql
export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_ro_user -d test_ro -p 5555 -w -f tests/validating_ro.sql

echo -e "\n ### Cleaning the env"
# Stopping and deleting the postgres container
docker stop psql-validating; docker rm psql-validating
docker-compose down --remove-orphans

# Deleting sql script
 rm test_sql_script.sql test_ro_sql_script.sql

# Deactivating venv
deactivate

# Deleting venv folder
rm -rf tutorial_env
