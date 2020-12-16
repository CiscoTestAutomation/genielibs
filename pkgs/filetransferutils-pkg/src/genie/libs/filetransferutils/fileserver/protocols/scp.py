from ..server import FileServer as BaseFileServer

class FileServer(BaseFileServer):
    '''FileServer for scp protocol

    Does not actually start any server, just provides address information for
    scp copy commands
    '''
    protocol = 'scp'

    def start_server(self):
        # override start_server to not start a separate process
        # Address already found in __init__, not other updated info needed
        return {}

    def verify_server(self):
        # Host authorization may not match device authorization.
        pass
