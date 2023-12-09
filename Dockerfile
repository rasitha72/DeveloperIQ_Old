FROM python:alpine
WORKDIR /app

COPY update_script.py . /app/

# Install psycopg2-binary and other dependencies directly
RUN pip install psycopg2-binary \
    && pip install Werkzeug==2.0.1 \
    && pip install requests==2.26.0
CMD ["python3", "update_script.py"]
