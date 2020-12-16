import logging
import os
import random
import signal
import tempfile
import threading

from pyats.utils.sig_handlers import enable_double_ctrl_c
from tftpy import TftpClient, TftpServer

from ..server import FileServer as BaseFileServer
from ..server import ALPHA

DEFAULT_PORT = 0

class FileServer(BaseFileServer):
    '''FileServer for tftp protocol

    Starts a TFTP server in another process and returns address information
    '''
    protocol = 'tftp'

    def run_server(self):
        # Run server in separate process
        signal.signal(signal.SIGINT, lambda x, y: None)

        address = self.server_info['address']
        port = self.server_info.get('port', DEFAULT_PORT)
        self.path = self.server_info.setdefault('path', '/')

        server = TftpServer(self.path)

        logfile = self.server_info.get('logfile', None)
        if logfile:
            ftp_logger = logging.getLogger('tftpy')
            ftp_logger.setLevel(logging.DEBUG)
            ftp_logger.propagate = False
            ftp_handler = logging.FileHandler(logfile)
            ftp_logger.addHandler(ftp_handler)

        # Port is only allocated after server is running, so start a thread
        # to retrieve
        threading.Thread(target=self.get_port, args=(server,)).start()
        server.listen(address, port)

    def verify_server(self):
        ip = self.server_info['address']
        port = self.server_info['port']
        path = self.server_info['path']

        # Set up client logging
        logfile = self.server_info.get('logfile', None)
        if logfile:
            logfile = '%s.client%s' % os.path.splitext(logfile)
            ftp_logger = logging.getLogger('tftpy')
            ftp_logger.setLevel(logging.DEBUG)
            ftp_logger.propagate = False
            ftp_handler = logging.FileHandler(logfile)
            ftp_logger.addHandler(ftp_handler)

        # Create a temporary file to copy to the TFTP server
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file that will not conflict with any existing files
            filename = self._generate_filename()
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, 'w') as f:
                f.write('ab'*100)

            # can't write to root. Use tmpdir instead
            if path == '/':
                filename = os.path.join(tmpdir, '%s2' % filename)

            client = TftpClient(ip, port)
            client.upload(filename, filepath)

            # Confirm file was copied
            upfilepath = os.path.join(path, filename)
            if not os.path.isfile(upfilepath):
                raise OSError('TFTP Upload unsuccessful')

            os.remove(upfilepath)

    def get_port(self, server):
        # Threaded function to get the allocated port for the TFTP server
        server.is_running.wait(5)
        self.queue.put({'port': server.listenport, 'path': self.path})

    def _generate_filename(self):
        path = self.server_info['path']
        for i in range(5):
            filename = ''.join([random.choice(ALPHA) for x in range(10)])
            filepath = '%s/%s' % (path, filename)
            if not os.path.exists(filepath):
                return filename
        raise OSError('Could not find filename not already in %s' % path)
