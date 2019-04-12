#!/bin/bash

# Check migrations
MIGRATIONS=$(./manage.py makemigrations --dry-run im2webapp)
if [ "$MIGRATIONS" != "No changes detected in app 'im2webapp'" ] ; then
    echo "Migrations should be made : "
    echo "$MIGRATIONS"
    exit 1
else
    echo "No migration to be done"
fi
