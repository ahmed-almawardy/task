FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /web/

COPY . .

COPY requirements .

RUN pip install -r requirements/base.txt

CMD python /web/app/__main__.py