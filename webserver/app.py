from flask import Flask, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Simple Blog</h1>
    <ul>
      <li><a href="/users">Users</a></li>
      <li><a href="/entries">Blog Entries</a></li>
    </ul>
    """

@app.route('/users')
def users():
    sql = "SELECT * FROM users;"
    r = requests.get(f'http://dataservice:5000/query', params={'sql': sql})
    users = r.json()
    return render_template_string("""
        <h2>Users</h2>
        <ul>
        {% for user in users %}
            <li>{{ user[0] }} - {{ user[1] }}</li>
        {% endfor %}
        </ul>
        <a href="/">Back</a>
    """, users=users)

@app.route('/entries')
def entries():
    sql = """
        SELECT entries.title, entries.content, users.name 
        FROM entries JOIN users ON entries.user_id = users.id;
    """
    r = requests.get(f'http://dataservice:5000/query', params={'sql': sql})
    entries = r.json()
    return render_template_string("""
        <h2>Blog Entries</h2>
        {% for title, content, author in entries %}
          <div style="margin-bottom:20px;">
            <h3>{{ title }} <small>by {{ author }}</small></h3>
            <p>{{ content }}</p>
          </div>
        {% endfor %}
        <a href="/">Back</a>
    """, entries=entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
