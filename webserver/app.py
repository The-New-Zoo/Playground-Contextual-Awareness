import os
import pickle
import subprocess

import requests
from flask import (
    Flask,
    make_response,
    redirect,
    render_template_string,
    request,
    session,
)

app = Flask(__name__)
app.secret_key = "supersecret"  # Weak secret for session


@app.route("/")
def index():
    return """
    <h1>Community Space</h1>
    <ul>
      <li><a href="/members">Member List</a></li>
      <li><a href="/articles">Articles</a></li>
    </ul>
    """


@app.route("/members")
def members():
    sql = "SELECT * FROM users;"
    r = requests.get(f"http://dataservice:5000/query", params={"sql": sql})
    members = r.json()
    return render_template_string(
        """
        <h2>Our Members</h2>
        <ul>
        {% for m in members %}
            <li>{{ m[0] }} - {{ m[1] }}</li>
        {% endfor %}
        </ul>
        <a href="/">Main Menu</a>
    """,
        members=members,
    )


@app.route("/articles")
def articles():
    sql = """
        SELECT entries.title, entries.content, users.name 
        FROM entries JOIN users ON entries.user_id = users.id;
    """
    r = requests.get(f"http://dataservice:5000/query", params={"sql": sql})
    articles = r.json()
    return render_template_string(
        """
        <h2>Latest Articles</h2>
        {% for title, content, author in articles %}
          <div style="margin-bottom:20px;">
            <h3>{{ title }} <small>written by {{ author }}</small></h3>
            <div>{{ content|safe }}</div>
          </div>
        {% endfor %}
        <a href="/">Main Menu</a>
    """,
        articles=articles,
    )


@app.route("/run-cmd", methods=["GET", "POST"])
def run_cmd():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("cmd", "")
        output = subprocess.getoutput(cmd)
    return render_template_string(
        """
        <h2>Run a Shell Command</h2>
        <form method="post">
            <input name="cmd" placeholder="ls; whoami" />
            <button type="submit">Run</button>
        </form>
        <pre>{{ output }}</pre>
        <a href="/">Main Menu</a>
    """,
        output=output,
    )


@app.route("/pickle", methods=["GET", "POST"])
def pickle_endpoint():
    result = ""
    if request.method == "POST":
        data = request.form.get("data", "")
        try:
            obj = pickle.loads(bytes.fromhex(data))
            result = f"Deserialized: {obj}"
        except Exception as e:
            result = f"Error: {e}"
    return render_template_string(
        """
        <h2>Insecure Deserialization (Pickle)</h2>
        <form method="post">
            <input name="data" placeholder="hex-encoded pickle" />
            <button type="submit">Deserialize</button>
        </form>
        <pre>{{ result }}</pre>
        <a href="/">Main Menu</a>
    """,
        result=result,
    )


@app.route("/secrets")
def secrets():
    return f"<pre>{os.environ}</pre><a href='/'>Main Menu</a>"


@app.route("/profile/<int:user_id>")
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


# Weak authentication (plain text, no hashing, no validation)
users = {}


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            msg = "User exists!"
        else:
            users[username] = password  # Store plain text
            msg = "Registered!"
    return render_template_string(
        """
        <h2>Register</h2>
        <form method="post">
            <input name="username" placeholder="Username" />
            <input name="password" type="password" placeholder="Password" />
            <button type="submit">Register</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/login">Login</a> | <a href="/">Main Menu</a>
    """,
        msg=msg,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.get(username) == password:
            session["user"] = username
            return redirect("/")
        else:
            msg = "Invalid!"
    return render_template_string(
        """
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username" />
            <input name="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/register">Register</a> | <a href="/">Main Menu</a>
    """,
        msg=msg,
    )


@app.route("/read-file", methods=["GET", "POST"])
def read_file():
    content = ""
    if request.method == "POST":
        path = request.form.get("path", "")
        try:
            with open(path, "r") as f:
                content = f.read()
        except Exception as e:
            content = str(e)
    return render_template_string(
        """
        <h2>Path Traversal File Read</h2>
        <form method="post">
            <input name="path" placeholder="/etc/passwd or ../../Dockerfile" />
            <button type="submit">Read</button>
        </form>
        <pre>{{ content }}</pre>
        <a href="/">Main Menu</a>
    """,
        content=content,
    )


@app.route("/redirect")
def open_redirect():
    url = request.args.get("url", "/")
    return redirect(url)


@app.route("/debug")
def debug():
    resp = make_response(f"Debug info: {dict(request.headers)}")
    return resp


@app.route("/reflected-xss")
def reflected_xss():
    q = request.args.get("q", "")
    return f"<h2>Echo: {q}</h2><a href='/'>Main Menu</a>"


@app.route("/csrf-demo", methods=["GET", "POST"])
def csrf_demo():
    msg = ""
    if request.method == "POST":
        msg = f"Changed value to: {request.form.get('value')}"
    return render_template_string(
        """
        <h2>CSRF Demo</h2>
        <form method="post">
            <input name="value" placeholder="Change something" />
            <button type="submit">Submit</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/">Main Menu</a>
    """,
        msg=msg,
    )


@app.route("/ssrf", methods=["GET", "POST"])
def ssrf():
    result = ""
    if request.method == "POST":
        url = request.form.get("url", "")
        try:
            r = requests.get(url)
            result = r.text[:500]
        except Exception as e:
            result = str(e)
    return render_template_string(
        """
        <h2>SSRF Demo</h2>
        <form method="post">
            <input name="url" placeholder="http://localhost:5000/query?sql=..." />
            <button type="submit">Fetch</button>
        </form>
        <pre>{{ result }}</pre>
        <a href="/">Main Menu</a>
    """,
        result=result,
    )


@app.route("/host-header")
def host_header():
    host = request.headers.get("Host", "")
    return f"<h2>Host: {host}</h2><a href='/'>Main Menu</a>"


@app.route("/upload", methods=["GET", "POST"])
def upload():
    msg = ""
    if request.method == "POST":
        f = request.files["file"]
        f.save(f.filename)
        msg = f"Uploaded {f.filename}"
    return render_template_string(
        """
        <h2>Unrestricted File Upload</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/">Main Menu</a>
    """,
        msg=msg,
    )


@app.route("/eval", methods=["GET", "POST"])
def eval_endpoint():
    result = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            result = str(eval(code))
        except Exception as e:
            result = str(e)
    return render_template_string(
        """
        <h2>Eval Demo</h2>
        <form method="post">
            <input name="code" placeholder="1+1 or __import__('os').system('ls')" />
            <button type="submit">Eval</button>
        </form>
        <pre>{{ result }}</pre>
        <a href="/">Main Menu</a>
    """,
        result=result,
    )


@app.route("/hardcoded-creds")
def hardcoded_creds():
    return '<pre>admin:password123</pre><a href="/">Main Menu</a>'


if __name__ == "__main__":
    app.run(host="0.0.0.0")
