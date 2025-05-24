from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Community Space</h1>
    <ul>
      <li><a href="/members">Member List</a></li>
      <li><a href="/articles">Articles</a></li>
    </ul>
    """

@app.route('/members')
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

@app.route('/articles')
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
          <div style="margin-bottom:20px;">
            <h3>{{ title }} <small>written by {{ author }}</small></h3>
            <div>{{ content|safe }}</div>
          </div>
        {% endfor %}
        <a href="/">Main Menu</a>
    """, articles=articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
