#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

echo -e "\n>>> Restoring database from dump file"
cat ./docker_files/db_dumps/db_dump.sql | docker exec -i db psql -U postgres

echo -e "\n>>> Running migrations"
./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
./manage.py createsuperuser \
   --username admin \
   --email admin@example.com \
   --noinput

echo -e "\n>>> Setting superuser 'admin' password to 12345"
./manage.py shell_plus --quiet-load -c "
u=User.objects.get(username='admin')
u.set_password('testpass123')
u.save()
"

echo -e "\n>>> Database restore finished."