import subprocess

from flask import render_template_string, request


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

