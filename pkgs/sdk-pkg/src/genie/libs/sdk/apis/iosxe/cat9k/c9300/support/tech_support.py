import logging
import re
from datetime import datetime

from pyats.easypy import runtime
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

log = logging.getLogger(__name__)


def collect_install_log(device, timeout=600):
    """ Collect install failure logs from the device.
    Args:
        device (obj): Device object (required)
        timeout (int): Timeout value for show tech-support command (default: 600 seconds)
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
    ]

    for command in commands:
        device.execute(command)

    show_tech_commands = [
        f"show tech-support install | append {file_name}"
    ]

    for command in show_tech_commands:
        device.execute(command, timeout=timeout)

    output = device.execute("request platform software trace archive")
    match = re.search(r'Done with creation of the archive file:\s*\[(.*?)\]', output)
    if match:
        archive_filename = match.group(1)

    try:
        # Get default directory to copy the files
        log.info("Getting default directory to copy the files")
        default_dir = get_default_dir(device)

        log.info(f"Copying file {file_name} to runinfo directory: {runtime.directory}")
        device.api.copy_from_device(local_path=f"{default_dir}{file_name}", remote_path=runtime.directory)
        if archive_filename:
            log.info(f"Copying archive file {archive_filename} to runinfo directory: {runtime.directory}")
            device.api.copy_from_device(local_path=f"{archive_filename}", remote_path=runtime.directory)

    except Exception as e:
        log.error(f"Failed to copy the install failure logs to runinfo directory: {e}", exc_info=True)
