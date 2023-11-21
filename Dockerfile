FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y libpcre3-dev
RUN pip install -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
