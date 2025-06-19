import requests
from flask import render_template_string

def members():
    sql = "SELECT * FROM users;"
    r = requests.get(f'http://dataservice:5000/query', params={'sql': sql})
    members = r.json()
    return render_template_string("""
        <h2>Our Members</h2>
        <ul>
        {% for m in members %}
            <li>{{ m[0] }} - {{ m[1] }}</li>
        {% endfor %}
        </ul>
        <a href="/">Main Menu</a>
    """, members=members) 