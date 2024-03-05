FROM python:3.12.2-slim

RUN mkdir -p /app/src

WORKDIR /app/src

RUN pip install Django==4.2.10

RUN pip install --upgrade django

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x ./script/deploy.sh

EXPOSE 8000

CMD ["sh", "./script/deploy.sh"]