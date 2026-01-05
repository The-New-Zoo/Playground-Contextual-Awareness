import requests
from flask import render_template_string, request


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

