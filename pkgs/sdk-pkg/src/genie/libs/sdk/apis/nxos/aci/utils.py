"""Base functions for NXOS ACI"""

# Python
import logging

from genie.libs.sdk.apis.utils import copy_to_device as generic_copy_to_device

from pyats.utils.fileutils import FileUtils

log = logging.getLogger(__name__)

def copy_to_device(device,
                   remote_path,
                   local_path,
                   server,
                   protocol,
                   vrf=None,
                   timeout=300,
                   compact=False,
                   use_kstack=False,
                   username=None,
                   password=None,
                   **kwargs):
    """
    Copy file from linux server to device
        Args:
            device ('Device'): Device object
            remote_path ('str'): remote file path on the server
            local_path ('str'): local file path to copy to on the device
            server ('str'): hostname or address of the server
            protocol('str'): file transfer protocol to be used
            vrf ('str'): vrf to use (optional)
            timeout('int'): timeout value in seconds, default 300
            compact('bool'): compress image option for n9k, defaults False
            username('str'): Username to be used during copy operation
            password('str'): Password to be used during copy operation
            use_kstack('bool'): Use faster version of copy, defaults False
                                Not supported with a file transfer protocol
                                prompting for a username and password
        Returns:
            None
    """
    # aci uses the linux implementation and fileutils doesnt support
    # os/platform abstraction
    setattr(device, 'os', 'linux')
    fu = FileUtils.from_device(device)
    setattr(device, 'os', 'nxos')

    generic_copy_to_device(device=device,
                           remote_path=remote_path,
                           local_path=local_path,
                           server=server,
                           protocol=protocol,
                           vrf=vrf,
                           timeout=timeout,
                           compact=compact,
                           use_kstack=use_kstack,
                           username=username,
                           password=password,
                           fu=fu,
                           **kwargs)