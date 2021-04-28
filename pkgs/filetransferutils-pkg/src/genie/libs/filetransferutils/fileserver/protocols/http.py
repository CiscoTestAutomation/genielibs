import os
import logging
import requests
import threading
import http.server

from ..server import FileServer as BaseFileServer

DEFAULT_PORT = 0

log = logging.getLogger(__name__)


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        try:
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
            # Translate a /-separated PATH to the local filename syntax.
            path = self.translate_path(self.path)
            # get filename from path
            fname = os.path.basename(path)
            filename = os.path.join(self.server.directory, fname)
            length = int(self.headers['Content-Length'])
            # Signal to device that we are ready to receive the file data
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

        # Setup local HTTP server
        server_address = (address, port)
        httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
        httpd.directory = local_dir
        local_port = httpd.server_port

        # Start http server in background thread
        t = threading.Thread(target=httpd.serve_forever)
        t.start()
        self.queue.put({'port': local_port, 'path': local_dir})

    def verify_server(self):
        """ No verification is done.

        This is on purpose, it does not always work
        e.g. if local VPN is preventing connectivity.
        """
        pass
