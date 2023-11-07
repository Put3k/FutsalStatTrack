<h1>Dump and restore database</h1>

<br>
<h3>Dump fly.io PostgreSQL database:</h3>
<a href="https://community.fly.io/t/backup-and-restore-postgresql-in-fly-io-step-by-step/11455">Backup and Restore
PostgreSQL in fly.io</a>
<p>
Proxy DB port on local machine:

```
fly proxy 15432:5432 --app <your_app_name-db>
```

in new terminal window:
```
pg_dump -p 15432 -h localhost -U postgres -c -d <your_app_database_name> -f db_backup
```

Enter database password (Operator Passowrd from fly PostgreSQL db application). You can access it by:
```
fly ssh console --app <your_app_name-db>
echo $OPERATOR_PASSWORD
```


<br>
<h3>Restore database in docker container</h3>
<a href="https://stackoverflow.com/questions/24718706/backup-restore-a-dockerized-postgresql-database">Restore database
inside container</a>
<p>
Run:

```
cat <db_file_name> | docker exec -i <db_container_name> psql -U postgres
```
Run migrations:
```
docker-compose exec web python manage.py migrate
```


<h3>IMPORTANT</h3>
When making a dump always use it with -c or --clean flag to output commands to DROP all the dumped database
objects prior to outputting the commands for creating them.