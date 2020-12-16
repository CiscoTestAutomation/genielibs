import logging
import os

from pyats import configuration as cfg
from pyats.datastructures import AttrDict
from pyats.easypy.plugins.bases import BasePlugin
from pyats.utils.dicts import recursive_update
from pyats.utils.secret_strings import SecretString

from .server import FileServer

logger = logging.getLogger(__name__)

FILETRANSFER_PROTOCOL_CFG = 'filetransfer.protocol'
FILETRANSFER_PROTOCOL_DEFAULT = 'ftp'


def start_servers(testbed, log_dir, synchro=None):
    '''find and start all dynamic file transfer servers in the testbed
    '''
    file_servers = []
    # servers may not exist
    for name, server in getattr(testbed, 'servers', {}).items():
        if server.get('dynamic'):
            # Make log dir if it doesn't already exist
            os.makedirs(log_dir, exist_ok=True)

            # Ensure dynamic server has a file copy protocol
            if not 'protocol' in server:
                protocol = cfg.get(FILETRANSFER_PROTOCOL_CFG)
                if not protocol:
                    raise TypeError('Dynamic server %s missing "protocol"'
                                    % name)
                server['protocol'] = protocol

            # Set up log file for file transfer server
            if 'logfile' in server.get('custom', {}):
                server['logfile'] = server['custom']['logfile']
            else:
                server['logfile'] = os.path.join(
                    log_dir, '%s.%s.log' % (name, server['protocol']))

            # Add multiprocessing manager to server kwargs if passed
            if synchro:
                server['synchro'] = synchro

            # Create file server
            file_servers.append(FileServer(testbed=testbed,
                                           name=name,
                                           **server))

            # Start server
            file_servers[-1].__enter__()

    # Return list of started servers
    return file_servers


class FileServerPlugin(BasePlugin):

    def pre_job(self, job):
        self.file_servers = []
        if self.runtime.testbed:
            log_dir = os.path.join(self.runtime.directory, 'filetransferlogs')
            self.file_servers = start_servers(self.runtime.testbed, log_dir,
                                              synchro=self.runtime.synchro)

    def post_job(self, job):
        for file_server in self.file_servers:
            # Stop running servers
            file_server.__exit__()


fileserver_plugin = {
    'plugins': {
        'FileServerPlugin':
            {'class': FileServerPlugin,
             'enabled': True,
             'kwargs': {},
             'module': 'genie.libs.filetransferutils.fileserver.plugin',
             'name': 'FileServerPlugin',
             'order': 61 # after testbed is loaded
            },
        },
    }
