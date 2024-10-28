FROM python:3.12-alpine3.20

WORKDIR /goodreads

COPY src requirements.txt /goodreads/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--chdir", "src/goodreads", "--bind", "0.0.0.0:8000", "core.wsgi:application"]

ENTRYPOINT ["./entrypoint.sh"]
