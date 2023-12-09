# update_script.py
import requests
import psycopg2
from datetime import datetime, timedelta
import time

# GitHub API credentials
github_username = 'rasitha72'
github_token = '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'

def update_postgresql_table():
    # Your PostgreSQL connection details
    connection = psycopg2.connect(
        host="database-1.cjz9pbxtvmuk.us-east-1.rds.amazonaws.com",
        port=5432,
        user="postgres",
        password="rasitha123",
        database="",
    )

    # Your update logic
    cursor = connection.cursor()

    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # List of contributors to GitHub REST API
    contributors = ['Kasuntharu', 'thushanwithanage', 'rasitha72']

    for contributor in contributors:
        # GitHub API endpoint for contributor events
        github_api_url = f'https://api.github.com/users/{contributor}/events'

        # GitHub API request headers
        headers = {
            'Authorization': f'Basic {github_username}:{github_token}'
        }

        # Make GitHub API request
        response = requests.get(github_api_url, headers=headers)

        # Process GitHub API response
        if response.status_code == 200:
            events = response.json()

            # Initialize counters
            commit_count = 0
            issue_count = 0
            pull_request_count = 0

            # Loop through events and count relevant actions
            for event in events:
                event_type = event['type']
                created_at = event['created_at'][:10]

                if created_at == yesterday_str:
                    if event_type == 'PushEvent':
                        commit_count += 1
                    elif event_type == 'IssuesEvent':
                        issue_count += 1
                    elif event_type == 'PullRequestEvent':
                        pull_request_count += 1

            # Insert data into RDS PostgreSQL table
            insert_query = """
                INSERT INTO developer_metrics (contributor, commit_count, issue_count, pull_req, created_on)
                VALUES (%s, %s, %s, %s, %s)
            """
            data = (contributor, commit_count, issue_count, pull_request_count, datetime.now())
            cursor.execute(insert_query, data)
            #connection.commit()

            print(f'Metrics for {contributor} on {yesterday_str} inserted successfully.')
        else:
            print(f'Error fetching GitHub events for {contributor}. Status code: {response.status_code}')

    # Close database connection
    cursor.close()

    connection.commit()
    connection.close()

if __name__ == "__main__":
    while True:
        update_postgresql_table()
        time.sleep(1800)  # Sleep for 30 minutes (30 mins * 60 seconds)
