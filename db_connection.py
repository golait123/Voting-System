import psycopg2
from psycopg2 import OperationalError


def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port=5432,  # Default PostgreSQL port
            user="postgres",  # Replace with your PostgreSQL username
            password="24mci0007",  # Replace with your PostgreSQL password
            dbname="postgres"  # Your database name (here "postgres")
        )
        # Uncomment the next line for debugging:
        # print("Connected to PostgreSQL database")
        return connection
    except OperationalError as e:
        print("Error connecting to PostgreSQL:", e)
        return None


if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connected successfully!")
        conn.close()
