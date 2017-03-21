#!/usr/bin/env bash

python tests.py --failfast
python manage.py downgrade 0 >/dev/null
python manage.py upgrade >/dev/null
