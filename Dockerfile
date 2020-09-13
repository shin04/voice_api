FROM python:3.8

# RUN apt-get update
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt

EXPOSE 5000

ENTRYPOINT [ "sh", "start.sh" ]
