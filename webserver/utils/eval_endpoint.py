from flask import render_template_string, request


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
