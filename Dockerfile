FROM alpine:3.16


WORKDIR /keju

COPY pipfile ./

RUN pipenv sync

COPY . .

EXPOSE  8000

CMD ["python", "manage.py," "runserver"]