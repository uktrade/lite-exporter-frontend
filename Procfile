web: ./manage.py migrate && ./manage.py compilescss && ./manage.py compress && ./manage.py collectstatic --ignore=*.scss && gunicorn -c gconfig.py -b 0.0.0.0:$PORT conf.wsgi
