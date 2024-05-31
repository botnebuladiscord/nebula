FROM python:latest

LABEL Maintainer="botnebula"

WORKDIR /

COPY main.py ./

RUN pip install -r requirements.txt

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./main.py"]
