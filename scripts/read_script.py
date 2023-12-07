from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Replace these with your RDS PostgreSQL connection details
DB_HOST = "database-1.cjz9pbxtvmuk.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "rasitha123"
DB_NAME = ""

def query_database():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

    cursor = connection.cursor()

    # Example query: Retrieve all rows from the table
    query = "SELECT * FROM developer_metrics;"
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

@app.route('/')
def index():
    # Get data from the database
    data = query_database()

    # Render the data in an HTML template
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

