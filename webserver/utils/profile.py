import requests
from flask import render_template_string


def profile(user_id):
    sql = f"SELECT * FROM users WHERE id={user_id};"
    r = requests.get(f"http://dataservice:5000/query", params={"sql": sql})
    user = r.json()
    return render_template_string(
        """
        <h2>User Profile</h2>
        <pre>{{ user }}</pre>
        <a href="/">Main Menu</a>
    """,
        user=user,
    )

