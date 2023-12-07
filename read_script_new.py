from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# RDS PostgreSQL credentials
rds_host = 'database-1.cjz9pbxtvmuk.us-east-1.rds.amazonaws.com'
rds_port = '5432'
rds_dbname = ''
rds_username = 'postgres'
rds_password = 'rasitha123'

# Connect to RDS PostgreSQL
conn = psycopg2.connect(
    host=rds_host,
    port=rds_port,
    dbname=rds_dbname,
    user=rds_username,
    password=rds_password
)
cursor = conn.cursor()

# Route to display data in a web page
@app.route('/')
def display_data():
    # Fetch data from the RDS table
    select_query = "SELECT * FROM developer_metrics"
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Close database connection
    cursor.close()
    conn.close()

    # Render HTML template with data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
