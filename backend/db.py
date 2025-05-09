import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'tictictomb.db')

# Check if database exists, if not initialize it
if not os.path.exists(DB_PATH):
    from init_database import init_database
    init_database()

def execute_query(query):
    """Execute a query and return results with column names"""
    # Create a new connection for each query to avoid threading issues
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute(query)
            conn.commit()  # Commit any changes
            try:
                # Get column names from cursor description
                columns = [desc[0] for desc in cur.description] if cur.description else []

                # Fetch all rows
                rows = cur.fetchall()

                # If we have results and column names, convert to a list of dictionaries
                if rows and columns:
                    # Create a list of dictionaries with column names as keys
                    results = []
                    for row in rows:
                        result_dict = {}
                        for i, col in enumerate(columns):
                            if i < len(row):
                                result_dict[col] = row[i]
                        results.append(result_dict)
                    return results
                elif rows:
                    # If we have rows but no column names, return the raw rows
                    return rows
                else:
                    # No results
                    return []
            except sqlite3.Error as e:
                print(f"Fetch error: {e}")
                # If no results to fetch (e.g., for INSERT/UPDATE)
                return []
        except Exception as e:
            print(f"Query error: {e}")
            return []
