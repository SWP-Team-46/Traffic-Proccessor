from flask import Flask, request

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def error_page(path):
    return f"""
    <h1>Access denied</h1>
    <p>Your IP from error server view: {request.remote_addr}</p>
    <p>Path: /{path}</p>
    """, 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
