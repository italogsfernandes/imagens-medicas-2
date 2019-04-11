#!/bin/bash

set -e

LOCALE_DIRS="find im2webapp -name locale -type d"
LANGUAGES=(fr pt_BR)


RETURN=0

for LOCALE_DIR in $($LOCALE_DIRS) ; do

pushd $LOCALE_DIR/.. > /dev/null

for LANGUAGE in ${LANGUAGES[@]} ; do
    echo "Checking locales for: "$LANGUAGE
    django-admin makemessages -l $LANGUAGE 2>&1 > /dev/null
    LOCALE_FILE=locale/$LANGUAGE/LC_MESSAGES/django.po
    NB_DIFFS=$(git diff $LOCALE_FILE | grep "^[+-]" | grep -v "^[+-]\{3\}" | grep -v "POT-Creation-Date" | grep -v "[+-]#" | wc -l)
    if [ ! $NB_DIFFS -eq 0 ] ; then
        if [ $RETURN -eq 0 ] ; then
            echo "Translation files not up to date :"
            RETURN=1
        fi
        echo "- $LOCALE_DIR/$LANGUAGE/LC_MESSAGES/django.po"
    fi
    git checkout $LOCALE_FILE
    echo "Everything ok with locales/"$LANGUAGE
done
popd > /dev/null
done

exit $RETURN
