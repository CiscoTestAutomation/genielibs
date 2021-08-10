import os
import base64
import logging
import http.server

from pyats.topology.credentials import Credentials
from pyats.utils.secret_strings import SecretString, to_plaintext

from ..server import FileServer as BaseFileServer

DEFAULT_PORT = 0

log = logging.getLogger(__name__)


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        try:
            if self.server.auth:
                if self.headers.get(
                        "Authorization") != "Basic " + self.server.auth:
                    self.do_AUTHHEAD()
                    return
            # Translate a /-separated PATH to the local filename syntax.
            path = self.translate_path(self.path)
            # get filename from path
            fname = os.path.basename(path)
            filename = os.path.join(self.server.directory, fname)
            length = int(self.headers['Content-Length'])
            with open(filename, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")
            self.end_headers()
        except Exception:
            log.error('Unable to receive file', exc_info=True)

    def do_PUT(self):
        try:
            if self.server.auth:
                if self.headers.get(
                        "Authorization") != "Basic " + self.server.auth:
                    self.do_AUTHHEAD()
                    return
            # Translate a /-separated PATH to the local filename syntax.
            path = self.translate_path(self.path)
            # get filename from path
            fname = os.path.basename(path)
            filename = os.path.join(self.server.directory, fname)
            length = int(self.headers['Content-Length'])
            # Signal to device that we are ready to receive the file data
            if self.headers.get('Expect', '') == '100-continue':
                self.send_response_only(100)
                self.end_headers()
            # receive data and store in file
            with open(filename, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")
            self.end_headers()
        except Exception:
            log.error('Unable to receive file', exc_info=True)

    def do_GET(self):
        self.directory = self.server.directory
        if self.server.auth:
            if self.headers.get(
                    "Authorization") != "Basic " + self.server.auth:
                self.do_AUTHHEAD()
                return
        super().do_GET()


class FileServer(BaseFileServer):
    '''FileServer for http protocol

    Starts a HTTP server in another process and returns address information
    '''
    protocol = 'http'

    def run_server(self):
        # Run server in separate process
        address = self.server_info.get('address', '0.0.0.0')
        port = self.server_info.get('port', DEFAULT_PORT)
        local_dir = self.server_info.get('path', '/')
        http_auth = self.server_info.get('http_auth', False)

        # Setup local HTTP server
        server_address = (address, port)
        httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
        httpd.directory = local_dir
        local_port = httpd.server_port

        if http_auth:
            creds = self.server_info.get('credentials', {}).get('http', {})
            username = creds.get('username', self._generate_credential())
            password = creds.get(
                'password',
                SecretString.from_plaintext(self._generate_credential()))

            httpd.auth = base64.b64encode(
                "{}:{}".format(username, to_plaintext(password)).encode()).decode()
        else:
            httpd.auth = None

        # Send new info back to parent process
        self.queue.put({
            'port': local_port,
            'path': local_dir,
            'credentials': Credentials({
                'http': {
                    'username': username,
                    'password': password
                }
            }) if http_auth else {}
        })

        # Keep process alive
        httpd.serve_forever()

    def verify_server(self):
        """ No verification is done.

        This is on purpose, it does not always work
        e.g. if local VPN is preventing connectivity.
        """
        pass
