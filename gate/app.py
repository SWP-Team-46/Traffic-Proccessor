from flask import Flask, request, Response
import requests

app = Flask(__name__)

MAIN_SERVER = "http://cnss:8080"
ERROR_SERVER = "http://error-server:5000"

# Blocked IP list.
# It is empty for now, so all IPs are allowed.
BLOCKED_IPS = {
    "172.19.0.1"
    "10.241.1.122"
}


def get_client_ips():
    """
    Get all possible client IPs.
    X-Forwarded-For may contain the original client IP if there is a proxy.
    We check both to avoid missing blocked clients.
    """
    ips = []

    if request.remote_addr:
        ips.append(request.remote_addr)

    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        forwarded_ips = [
            ip.strip()
            for ip in forwarded_for.split(",")
            if ip.strip()
        ]
        ips.extend(forwarded_ips)

    return ips


def proxy_request(target_server):
    """
    Forward request to the selected server:
    - cnss if the IP is allowed
    - error-server if the IP is blocked
    """

    url = target_server + request.full_path

    if url.endswith("?"):
        url = url[:-1]

    response = requests.request(
        method=request.method,
        url=url,
        headers={
            key: value
            for key, value in request.headers
            if key.lower() != "host"
        },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    ]

    headers = [
        (name, value)
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(response.content, response.status_code, headers)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def gate(path):
    client_ips = get_client_ips()

    print(f"[GATE] Request IPs: {client_ips}", flush=True)

    blocked_ip = None

    for ip in client_ips:
        if ip in BLOCKED_IPS:
            blocked_ip = ip
            break

    if blocked_ip:
        print(f"[GATE] DENY {blocked_ip} -> error-server", flush=True)
        return proxy_request(ERROR_SERVER)

    print(f"[GATE] ALLOW {client_ips} -> cnss", flush=True)
    return proxy_request(MAIN_SERVER)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
