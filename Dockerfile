FROM python:3.9

WORKDIR /app

COPY scripts/update_script.py . /app

# Install psycopg2-binary and other dependencies directly
RUN pip install psycopg2-binary==2.9.1 \
    && pip install Werkzeug==2.0.1 \
    && pip install requests==2.26.0
CMD ["python", "update_script.py"]
