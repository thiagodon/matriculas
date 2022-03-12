#!/bin/sh

# docker-compose exec db sh -c 'export PGPASSWORD=local_db_pass && pg_dump --verbose -h 127.0.0.1 -p 5432 -U local_db_user -d local_db_name -Fc > /var/lib/postgresql/entregas.dump'
# docker-compose exec db sh -c 'export PGPASSWORD=ykGHX1onuZHG && pg_dump --verbose -h psql-mateusmais-dev.postgres.database.azure.com -p 5432 -U mateusmais@psql-mateusmais-dev -d mateusmais_entregas -Fc > /var/lib/postgresql/entregas.dump'

docker-compose exec db sh -c 'export PGPASSWORD=local_db_pass && dropdb  -h 127.0.0.1 -p 5432 -U local_db_user local_db_name'
docker-compose exec db sh -c 'export PGPASSWORD=local_db_pass && psql -h 127.0.0.1 -p 5432 -U local_db_user postgres -c "create database local_db_name"'
docker-compose exec db sh -c 'export PGPASSWORD=local_db_pass && pg_restore --verbose --clean --no-acl --no-owner -h 127.0.0.1 -p 5432 -U local_db_user -d local_db_name /var/lib/postgresql/entregas.dump'


docker-compose exec db sh -c 'export PGPASSWORD=local_db_pass && psql -h 127.0.0.1 -U local_db_user -d postgres'
SELECT * from pg_database where datname = 'local_db_name';
UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'local_db_name';
ALTER DATABASE local_db_name CONNECTION LIMIT 1;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'local_db_name';
DROP DATABASE local_db_name;




docker-compose exec postgres sh -c 'pg_dump -U mateusmais@psql-mateusmais-dev -h psql-mateusmais-dev.postgres.database.azure.com -p 5432 --verbose mateusmais > /var/lib/postgresql/mateusmais_hml.bak --exclude-table-data=sync_productbulk'
docker-compose exec postgres sh -c 'export PGPASSWORD=BrsYf8rG9JWS && pg_dump --verbose -h psql-mateusmais-dev.postgres.database.azure.com -p 5432 -U mateusmais@psql-mateusmais-dev -d mateusmais_dev -Fc > /var/lib/postgresql/mateusmais_dev.dump'
docker-compose exec postgres sh -c 'export PGPASSWORD=ykGHX1onuZHG && pg_dump --verbose -h psql-mateusmais-hml.postgres.database.azure.com -p 5432 -U mateusmais@psql-mateusmais-hml -d mateusmais -Fc > /var/lib/postgresql/mateusmais_hml.dump'


postgis://mateusmais@psql-mateusmais-dev:BrsYf8rG9JWS@10.0.0.4:5432/mateusmais
postgis://mateusmais@vm-pgbouncer-hml:zjPSio0OuSphZj@10.1.3.100:5432/mateusmais
docker-compose exec postgres sh -c 'export PGPASSWORD=mateusmais_local && psql -h 127.0.0.1 -U mateusmais -d postgres'

SELECT * from pg_database where datname = 'mateusmais';
UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'mateusmais';
ALTER DATABASE mateusmais CONNECTION LIMIT 1;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'mateusmais';
DROP DATABASE mateusmais;


docker-compose exec postgres sh -c 'export PGPASSWORD=mateusmais_local && dropdb  -h 127.0.0.1 -p 5432 -U mateusmais mateusmais'
docker-compose exec postgres sh -c 'export PGPASSWORD=mateusmais_local && psql -h 127.0.0.1 -p 5432 -U mateusmais postgres -c "create database mateusmais"'
docker-compose exec postgres sh -c 'export PGPASSWORD=mateusmais_local && pg_restore --verbose --clean --no-acl --no-owner -h 127.0.0.1 -p 5432 -U mateusmais -d mateusmais /var/lib/postgresql/mateusmais_hml.dump'
docker-compose exec postgres sh -c 'export PGPASSWORD=mateusmais_local && pg_restore --verbose --clean --no-acl --no-owner -h 127.0.0.1 -p 5432 -U mateusmais -d mateusmais /var/lib/postgresql/mateusmais_dev.dump'



