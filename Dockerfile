FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/usr/src/web
RUN mkdir $APP_HOME/
RUN mkdir $APP_HOME/staticfiles

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY ./be-healthy2/entrypoint.sh .

EXPOSE 8000

CMD ["python", "be-healthy2/manage.py", "runserver", "0.0.0.0:8000"]