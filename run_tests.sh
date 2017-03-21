#!/usr/bin/env bash

echo "Test for Author"
python manage.py downgrade 0 >/dev/null
python manage.py upgrade >/dev/null
python tests.py AuthorTestCase
