import oracledb


def get_connection():
    username = "your_username"
    password = "your_password"
    dsn = "localhost:1521/XE"  # Adjust host/port/service name as needed

    try:
        # In thin mode, no Oracle Client library is required.
        connection = oracledb.connect(
            user=username,
            password=password,
            dsn=dsn
        )
        print("Connected using oracledb in thin mode!")
        return connection
    except oracledb.Error as e:
        print("Error connecting to Oracle:", e)
        return None
