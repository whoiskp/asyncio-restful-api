FROM python:3.6-alpine3.6
ADD . /urs/src/app
WORKDIR /urs/src/app
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "api/main.py"]