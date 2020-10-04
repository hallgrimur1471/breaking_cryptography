"""
Implement and break HMAC-SHA1 with an artificial timing leak

Useful command while developing:
#pylint:disable=line-too-long
svarmi_watch . .py " ( bash -c 'sleep 2; curl http://localhost:1471/test?file=foo\&signature=46b4ec586117154dacd49d664e5d63fdc88efb51' & ) && drvn_cryptography_run_cryptopals_challenge 31 -v"
"""

import time
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

import drvn.cryptography.utils as utils
import drvn.cryptography.hmac as hmac


def run_challenge():
    http_server = HTTPServer(("", 1471), RequestHandler)
    server_thread = threading.Thread(target=http_server.serve_forever)
    logging.info("Starting HTTP server ...")
    server_thread.start()
    time.sleep(1)

    file_ = b"foo"
    signature = utils.generate_random_bytes(20).hex()  # guess
    response = urlopen(
        f"http://localhost:1471/test?file={file_}&signature={signature}"
    )
    print(response.read())

    logging.info("Shutting down HTTP server ...")
    http_server.shutdown()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        results = urlparse(self.path)
        query = parse_qs(results.query)

        file_, signature = query["file"][0], query["signature"][0]
        file_ = file_.encode()
        signature = bytes.fromhex(signature)

        if is_authenticated(file_, signature):
            self.wfile.write(b"File authenticated\n")
        else:
            self.wfile.write(b"File is not authenticated\n")


def is_authenticated(file_, signature):
    key = b"very secret key"
    hmac_ = hmac.sha1(key, file_)
    return is_equal(signature, hmac_)


def is_equal(a, b):
    """
    Insecure method for checking if a equals b

    Args:
        a (bytes)
        b (bytes)
    """
    for i in range(max(len(a), len(b))):
        if i >= len(a) or i >= len(b) or a[i] != b[i]:
            return False
        time.sleep(0.05)
    return True
