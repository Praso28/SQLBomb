import sqlite3
import os
import sys

def init_database():
    """Initialize the SQLite database with schema and sample data"""
    print("Initializing the SQL Bomb Defusal Game database...")

    # Database file path
    db_dir = os.path.join(os.path.dirname(__file__), 'database')
    db_path = os.path.join(db_dir, 'tictictomb.db')

    # Make sure the database directory exists
    os.makedirs(db_dir, exist_ok=True)

    # Check if database already exists
    db_exists = os.path.exists(db_path)

    # In cloud environments, we might not want to remove the existing database
    # Only remove if explicitly running this script directly
    if db_exists and __name__ == "__main__":
        try:
            os.remove(db_path)
            print(f"Removed existing database file: {db_path}")
            db_exists = False
        except Exception as e:
            print(f"Error removing existing database: {e}")
            sys.exit(1)

    # If database exists and we're not running this script directly, exit early
    if db_exists and __name__ != "__main__":
        print(f"Database already exists at {db_path}. Skipping initialization.")
        return

    # Create a new SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"Created new database file: {db_path}")
    except Exception as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

    # Read and execute schema.sql
    try:
        with open(os.path.join(db_dir, "schema.sql"), "r") as schema_file:
            schema_sql = schema_file.read()
            cursor.executescript(schema_sql)
            conn.commit()
            print("Schema created successfully.")
    except Exception as e:
        print(f"Error creating schema: {e}")
        sys.exit(1)

    # Read and execute sample_data.sql
    try:
        with open(os.path.join(db_dir, "sample_data.sql"), "r") as data_file:
            data_sql = data_file.read()
            cursor.executescript(data_sql)
            conn.commit()
            print("Sample data inserted successfully.")
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        sys.exit(1)

    # Close the connection
    cursor.close()
    conn.close()

    print("Database initialization completed successfully!")
    print("You can now run the game with: streamlit run app.py")

if __name__ == "__main__":
    init_database()
