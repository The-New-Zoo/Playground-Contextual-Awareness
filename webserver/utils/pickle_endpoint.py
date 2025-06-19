import pickle

from flask import render_template_string, request


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

