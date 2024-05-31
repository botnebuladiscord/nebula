FROM python:latest

LABEL Maintainer="botnebula"

WORKDIR /

COPY main.py ./


#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./main.py"]
