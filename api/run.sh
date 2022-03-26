#export DB_USER='admin' DB_PASS='LTg8B7BAxIemx7l2LNm1' DB_URI='localhost' DB_PORT='3306' DB_NAME='evergreen-db'
export FLASK_APP="__init__.py"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask seed
flask run --host=0.0.0.0