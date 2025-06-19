from flask import render_template_string, request


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
