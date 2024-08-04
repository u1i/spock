# USE_HTTPS=true gunicorn --bind 0.0.0.0:8080 wsgi:spock
gunicorn --bind 0.0.0.0:8080 wsgi:spock
