import pg8000
import os

db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

def lambda_handler(event, context):
    try:
        connection = pg8000.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        print(connection)
        cursor = connection.cursor()
        print(cursor)
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"Database version: {result[0]}")
        
        cursor.close()
        connection.close()
        
        return {
            'statusCode': 200,
            'body': f"Database version: {result[0]}"
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
