FROM python:3.6-alpine3.6
ADD . /urs/src/app
WORKDIR /urs/src/app
EXPOSE 6969
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn main:app --bind localhost:6969 --worker-class aiohttp.worker.GunicornWebWorker"]