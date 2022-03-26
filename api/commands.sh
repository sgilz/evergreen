export FLASK_APP="/mnt/c/Users/sgilz/universidad/9no_semestre/evergreen/api/__init__.py"
export DB_USER='admin' DB_PASS='LTg8B7BAxIemx7l2LNm1' DB_URI='localhost' DB_PORT='3306' DB_NAME='evergreen-db'

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask seed