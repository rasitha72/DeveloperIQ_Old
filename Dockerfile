FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY update_script.py .

RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "update_script.py"]

