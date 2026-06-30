from flask import Flask, request

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def error_page(path):
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Access denied</title>
        <style>
          body {{
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #111827;
            color: white;
            font-family: Arial, sans-serif;
          }}
          .box {{
            text-align: center;
            padding: 40px;
            border: 1px solid #374151;
            border-radius: 16px;
            background: #1f2937;
          }}
          h1 {{
            color: #ef4444;
          }}
        </style>
      </head>
      <body>
        <div class="box">
          <h1>Access denied</h1>
          <p>Your IP is blocked or suspicious.</p>
          <p>Blocked path: /{path}</p>
          <p>Your IP from error server view: {request.remote_addr}</p>
        </div>
      </body>
    </html>
    """, 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
