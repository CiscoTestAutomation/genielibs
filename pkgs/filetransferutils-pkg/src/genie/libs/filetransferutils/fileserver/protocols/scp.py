"""
SCP File Server Implementation using AsyncSSH
"""
import asyncio
import asyncssh
import os
import tempfile
import pathlib
import logging

log = logging.getLogger(__name__)

from pyats.topology.credentials import Credentials
from genie.libs.filetransferutils.fileserver.server import FileServer as BaseFileServer

DEFAULT_PORT = 0
DEFAULT_HOST = '0.0.0.0'

class SCPServer(asyncssh.SSHServer):
    """SSH server implementation for SCP file transfers.

    This class extends asyncssh.SSHServer to provide a specialized SSH server
    that handles SCP (Secure Copy Protocol) connections with user authentication
    and directory access control.

    Attributes:
        server_directory (str): The root directory path that the server will serve files from.
        allowed_users (dict): Dictionary mapping usernames to passwords for authentication.
                             If None or empty, password authentication is disabled.

    Methods:
        connection_made(conn): Called when a new SSH connection is established.
        connection_lost(exc): Called when an SSH connection is closed or lost.
        begin_auth(username): Initiates authentication process for a user.
        password_auth_supported(): Returns whether password authentication is enabled.
        validate_password(username, password): Validates user credentials against allowed_users.
    """
    def __init__(self, server_directory, allowed_users=None):
        self.server_directory = server_directory
        self.allowed_users = allowed_users or {}

    def connection_made(self, conn):
        peername = conn.get_extra_info("peername")
        if peername:
            log.debug(f'SSH connection from {peername[0]}')

    def connection_lost(self, exc):
        if exc:
            log.warning(f'SSH connection error: {exc}')
        else:
            log.debug('SSH connection closed')

    def begin_auth(self, username):
        log.debug(f"Authentication attempt for user: {username}")
        return True

    def password_auth_supported(self):
        return bool(self.allowed_users)

    def validate_password(self, username, password):
        ok = (username in self.allowed_users and self.allowed_users[username] == password) if self.allowed_users else False
        if ok:
            log.debug(f"Password auth successful for {username}")
        else:
            log.warning(f"Password auth failed for {username}")
        return ok


class FileServer(BaseFileServer):
    """SCP File Server Implementation.

    This class provides an SCP (Secure Copy Protocol) file server that runs in a separate
    process using AsyncSSH. It supports user authentication and serves files from a
    specified directory.

    The server automatically generates credentials and starts an SSH server that handles
    SCP connections for file transfers.
    """
    protocol = 'scp'

    def run_server(self):
        """Run AsyncSSH server for SCP."""
        try:
            asyncio.run(self._start_server())
        except Exception as e:
            log.error(f'Failed to start AsyncSSH server: {e}')
            self.queue.put({'error': str(e)})

    async def _start_server(self):
        """Start the SCP server asynchronously."""
        try:
            # Create directory if it doesn't exist
            local_dir = self.server_info.get('path', '/')
            pathlib.Path(local_dir).mkdir(parents=True, exist_ok=True)

            # Generate credentials
            username = self._generate_credential()
            password = self._generate_credential()
            allowed_users = {username: password} if (username and password) else {}

            address = self.server_info.get('address', DEFAULT_HOST)
            port = self.server_info.get('port', DEFAULT_PORT)

            # Generate host key if not provided - using context manager for cleanup
            host_key_path = self.server_info.get('host_key_path')
            if host_key_path:
                # Use existing host key - no cleanup needed
                await self._run_with_host_key(host_key_path,
                                                local_dir,
                                                allowed_users,
                                                address,
                                                port,
                                                username,
                                                password)
            else:
                # Generate temporary host key with automatic cleanup
                with tempfile.TemporaryDirectory() as temp_dir:
                    host_key_path = os.path.join(temp_dir, 'ssh_host_key_ed25519')
                    key = asyncssh.generate_private_key('ssh-ed25519')
                    with open(host_key_path, 'wb') as f:
                        f.write(key.export_private_key())

                    await self._run_with_host_key(host_key_path,
                                                    local_dir,
                                                    allowed_users,
                                                    address,
                                                    port,
                                                    username,
                                                    password)

        except Exception as e:
            log.error(f'AsyncSSH server error: {e}')
            self.queue.put({'error': str(e)})

    async def _run_with_host_key(self, host_key_path, local_dir, allowed_users, address, port, username, password):
        """Run SSH server with given host key."""
        ssh_server = SCPServer(local_dir, allowed_users)

        def sftp_factory(chan):
            return asyncssh.SFTPServer(chan, chroot=local_dir)

        server = await asyncssh.listen(
            host=address,
            port=port,
            server_host_keys=[host_key_path],
            server_factory=lambda: ssh_server,
            allow_scp=True,
            sftp_factory=sftp_factory,
        )

        actual_port = server.get_port()

        # Send new info back to parent process
        self.queue.put({
            'port': actual_port,
            'address': address,
            'path': local_dir,
            'host_key_path': host_key_path,
            'credentials': Credentials({
                'scp': {
                    'username': username,
                    'password': password
                }
            })
        })

        log.info(f"SCP server listening on {address}:{actual_port}")
        await server.wait_closed()

    def verify_server(self):
        # Host authorization may not match device authorization.
        pass

