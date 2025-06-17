from flask import Flask, render_template_string, request, jsonify
import requests
import subprocess
import pickle
import os

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Community Space</h1>
    <ul>
      <li><a href="/members">Member List</a></li>
      <li><a href="/articles">Articles</a></li>
      <li><a href="/search">Search</a></li>
      <li><a href="/profile">Profile</a></li>
      <li><a href="/admin">Admin Panel</a></li>
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

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # VULNERABILITY: SQL Injection through dataservice
    sql = f"SELECT * FROM entries WHERE title LIKE '%{query}%' OR content LIKE '%{query}%';"
    r = requests.get(f'http://dataservice:5000/query', params={'sql': sql})
    results = r.json()
    
    # VULNERABILITY: XSS - direct template injection of user input
    return render_template_string(f"""
        <h2>Search Results for: {query}</h2>
        <form method="GET">
            <input type="text" name="q" value="{query}" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
        <ul>
        {% for result in results %}
            <li>{{ result[1] }} - {{ result[2] }}</li>
        {% endfor %}
        </ul>
        <a href="/">Main Menu</a>
    """, results=results)

@app.route('/profile')
def profile():
    username = request.args.get('user', '')
    # VULNERABILITY: XSS - unsafe template rendering
    return render_template_string(f"""
        <h2>Profile: {username}</h2>
        <p>Welcome to your profile page!</p>
        <a href="/">Main Menu</a>
    """)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            # VULNERABILITY: Command Injection - executes arbitrary commands
            result = subprocess.check_output(command, shell=True, text=True)
            return render_template_string("""
                <h2>Admin Panel</h2>
                <form method="POST">
                    <input type="text" name="command" placeholder="Enter command...">
                    <button type="submit">Execute</button>
                </form>
                <h3>Output:</h3>
                <pre>{{ output }}</pre>
                <a href="/">Main Menu</a>
            """, output=result)
        except Exception as e:
            return render_template_string("""
                <h2>Admin Panel</h2>
                <form method="POST">
                    <input type="text" name="command" placeholder="Enter command...">
                    <button type="submit">Execute</button>
                </form>
                <p>Error: {{ error }}</p>
                <a href="/">Main Menu</a>
            """, error=str(e))
    
    return render_template_string("""
        <h2>Admin Panel</h2>
        <form method="POST">
            <input type="text" name="command" placeholder="Enter command...">
            <button type="submit">Execute</button>
        </form>
        <a href="/">Main Menu</a>
    """)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = file.filename
    
    # VULNERABILITY: Path Traversal - allows writing to any location
    file.save(f'/tmp/{filename}')
    
    # VULNERABILITY: Insecure Deserialization
    try:
        data = request.get_data()
        obj = pickle.loads(data)
        return jsonify({'status': 'uploaded', 'deserialized': str(obj)})
    except Exception:
        return jsonify({'status': 'uploaded'})

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        config_data = request.get_data()
        try:
            # VULNERABILITY: Insecure Deserialization
            config = pickle.loads(config_data)
            return jsonify({'config': str(config)})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template_string("""
        <h2>Configuration</h2>
        <p>Send POST request with pickled configuration data</p>
        <a href="/">Main Menu</a>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
