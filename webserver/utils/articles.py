import requests
from flask import render_template_string

def articles():
    sql = """
        SELECT entries.title, entries.content, users.name 
        FROM entries JOIN users ON entries.user_id = users.id;
    """
    r = requests.get(f'http://dataservice:5000/query', params={'sql': sql})
    articles = r.json()
    return render_template_string("""
        <h2>Latest Articles</h2>
        {% for title, content, author in articles %}
          <div style=\"margin-bottom:20px;\">
            <h3>{{ title }} <small>written by {{ author }}</small></h3>
            <div>{{ content|safe }}</div>
          </div>
        {% endfor %}
        <a href="/">Main Menu</a>
    """, articles=articles) 