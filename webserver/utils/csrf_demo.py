from flask import render_template_string, request


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

