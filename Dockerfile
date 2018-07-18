FROM ubuntu:16.04
ADD . /urs/src/app
WORKDIR /urs/src/app

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn main:app --bind localhost:6969 --worker-class aiohttp.worker.GunicornWebWorker"]