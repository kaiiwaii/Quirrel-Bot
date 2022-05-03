CNAME=""
DB_USERNAME=""
DB_PASSWORD=""
DB_NAME=""
SAVEPATH="/var/lib/postgresql/data/pgdata"

docker run --name $CNAME -p 5432:5432 -e POSTGRES_USER=$DB_USERNAME -e PGDATA=$SAVEPATH -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME -d --restart unless-stopped postgres
pip3 install -r requirements.txt