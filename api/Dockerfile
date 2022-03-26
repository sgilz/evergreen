FROM python:3.9.12-alpine3.14
WORKDIR /api
EXPOSE 5000
ENV DB_USER='admin' DB_PASS='LTg8B7BAxIemx7l2LNm1' DB_URI='localhost' DB_PORT='3306' DB_NAME='evergreen-db'
COPY __init__.py auth.py requirements.txt run.sh farm_chain.py ./
RUN pip install -r requirements.txt && chmod 700 run.sh 
CMD ["sh", "run.sh"]
