import ftplib
import logging
import signal

from pyats.topology.credentials import Credentials
from pyats.utils.secret_strings import SecretString, to_plaintext
from pyats.utils.sig_handlers import enable_double_ctrl_c
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from ..server import FileServer as BaseFileServer
from ..server import ALPHA

DEFAULT_PORT = 0

class FileServer(BaseFileServer):
    '''FileServer for ftp protocol

    Starts a FTP server in another process and returns address information
    '''
    protocol = 'ftp'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_server(self):
        # Run server in separate process
        signal.signal(signal.SIGINT, lambda x, y: None)
        # dict to send back in queue once server is started
        new_info = {}

        creds = self.server_info.get('credentials', {}).get('ftp', {})
        username = creds.get('username', self._generate_credential())
        password = creds.get(
            'password',
            SecretString.from_plaintext(self._generate_credential()))

        # return credentials back to parent process
        new_info['credentials'] = Credentials({
            'ftp': {
                'username': username,
                'password': password
            }
        })

        address = self.server_info['address']
        port = self.server_info.get('port', DEFAULT_PORT)
        address = (address, port)
        path = self.server_info.setdefault('path', '/')
        new_info['path'] = path

        # Create FTP Server
        auth = DummyAuthorizer()
        auth.add_user(username, to_plaintext(password), path, perm='elradfmwMT')
        handler = FTPHandler
        handler.authorizer = auth
        server = FTPServer(address, handler)
        server.max_cons = 256
        server.max_cons_per_ip = 5

        # Set up logging for the FTP Server
        logfile = self.server_info.get('logfile', None)
        if logfile:
            ftp_logger = logging.getLogger('pyftpdlib')
            ftp_logger.setLevel(logging.DEBUG)
            ftp_logger.propagate = False
            ftp_handler = logging.FileHandler(logfile)
            ftp_logger.addHandler(ftp_handler)

        # Retrieve allocated port
        _, new_info['port'] = server.address

        # Send new info back to parent process
        self.queue.put(new_info)

        # Listen
        server.serve_forever()

    def verify_server(self):
        ip = self.server_info['address']
        port = self.server_info['port']
        username = self.server_info['credentials']['ftp']['username']
        password = to_plaintext(
            self.server_info['credentials']['ftp']['password'])

        # Connect to FTP server
        client = ftplib.FTP()
        client.connect(host=ip, port=port)
        client.login(user=username, passwd=password)
        # Get list of files from FTP server
        client.dir(lambda x: None)
        client.quit()
