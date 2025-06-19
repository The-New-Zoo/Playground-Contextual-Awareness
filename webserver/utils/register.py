from flask import render_template_string, request

users = {}

def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            msg = 'User exists!'
        else:
            users[username] = password  # Store plain text
            msg = 'Registered!'
    return render_template_string('''
        <h2>Register</h2>
        <form method="post">
            <input name="username" placeholder="Username" />
            <input name="password" type="password" placeholder="Password" />
            <button type="submit">Register</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/login">Login</a> | <a href="/">Main Menu</a>
    ''', msg=msg) 