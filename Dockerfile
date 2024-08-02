FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip vim curl net-tools iputils-ping

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "cps.py"]