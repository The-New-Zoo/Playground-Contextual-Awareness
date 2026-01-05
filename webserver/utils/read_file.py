from flask import render_template_string, request


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

