import logging
import re
from datetime import datetime

from pyats.easypy import runtime
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

log = logging.getLogger(__name__)


def collect_install_log(device):
    """ Collect install failure logs from the device.
    Args:
        device (obj): Device object (required)
    Returns
        None on success, False on failure
    """

    archive_filename = None

    log.info("Logging the below to get the install failure logs from device")

    # Add timestamp to the show tech support filename
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    file_name = f"show_tech_support_{timestamp}.txt"

    commands = [
        "show platform software install-manager switch active R0 operation current detail",
        "show platform software install-manager switch active R0 operation history detail",
        f"show tech-support install | append {file_name}"
    ]

    for command in commands:
        device.execute(command)

    output = device.execute("request platform software trace archive")
    match = re.search(r'Done with creation of the archive file:\s*\[(.*?)\]', output)
    if match:
        archive_filename = match.group(1)

    # check if device has a telent connection to copy the files over to runinfo directory
    if 'telnet' not in device.connections.keys():
        log.info("Could not copy the install failure logs to runinfo directory")

    else:
        # Capture the connection alias
        conn_alias = device.default_connection_alias
        try:
            # Make sure the connection alias is telnet
            device.default_connection_alias = 'telnet'

            # Get default directory to copy the files
            default_dir = get_default_dir(device)

            device.api.copy_from_device(local_path=f"{default_dir}show_tech_support.txt", remote_path=runtime.directory)
            device.api.copy_from_device(local_path=f"{archive_filename}", remote_path=runtime.directory)
        except Exception as e:
            log.error(f"Failed to copy the install failure logs to runinfo directory: {e}")
        finally:
            # Reassign the default connection alias to the original alias
            device.default_connection_alias = conn_alias
