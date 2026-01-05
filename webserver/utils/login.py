from flask import render_template_string, request, session, redirect

users = {}

def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users.get(username) == password:
            session['user'] = username
            return redirect('/')
        else:
            msg = 'Invalid!'
    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username" />
            <input name="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
        </form>
        <p>{{ msg }}</p>
        <a href="/register">Register</a> | <a href="/">Main Menu</a>
    ''', msg=msg) 