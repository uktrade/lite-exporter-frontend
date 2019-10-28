web: ./manage.py migrate && ./manage.py compilescss && ./manage.py collectstatic && gunicorn -c gconfig.py -b 0.0.0.0:$PORT conf.wsgi
