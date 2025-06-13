import sqlite3


# modified
def get_user_info(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{username}'"
    )  # Insecure: unparameterized SQL
