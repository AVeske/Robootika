"""Client for the compressor HTTP API (MG400 vacuum gripper).

From a script:      from compressor_client import set_compressor
                    set_compressor("suck")
From the terminal:  python compressor_client.py off
"""
import json
import sys
import urllib.request

API_URL = "http://127.0.0.1:8000/api/pump"


def set_compressor(mode):
    """Send a mode ('suck', 'off', ...) to the API and return its reply as a dict.
    Never raises: on a network error returns {'ok': False, 'error': ...}."""
    body = json.dumps({"mode": mode}).encode()
    request = urllib.request.Request(API_URL, body, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return json.loads(response.read())
    except Exception as error:
        return {"ok": False, "error": str(error)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python compressor_client.py suck|off")
        sys.exit(1)
    print(set_compressor(sys.argv[1]))
