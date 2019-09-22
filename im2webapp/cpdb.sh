#!/bin/sh

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi

DB='im2webapp'
DB_USER=$1
SSH_HOST='italogsfernandes.com'
REMOTE_MEDIA='/home/italo/imagens-medicas-2/im2webapp/media/'

dropdb $DB
createdb $DB

ssh $SSH_HOST "pg_dump -U $DB_USER $DB | gzip" > $DB.sql.gz
gunzip --stdout $DB.sql.gz | psql $DB
rsync -avz -e ssh --delete $SSH_HOST:$REMOTE_MEDIA ./media/
