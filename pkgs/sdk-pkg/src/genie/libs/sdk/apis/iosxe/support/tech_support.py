import re
import psutil
import logging
from datetime import datetime

from pyats.easypy import runtime
from unicon.eal.dialogs import Dialog
from genie.libs.filetransferutils import FileServer, FileUtils
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir

from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_show_tech(device,
                  prefix='',
                  show_tech_command='show tech-support',
                  device_dir=None,
                  remote_server=None,
                  remote_path=None,
                  protocol='scp',
                  timeout=600):
    """ Collect show tech-support from the device.

    Args:
        device (obj): Device object (optional)
        prefix (str): filename prefix (optional)
        show_tech_command (str): command to execute (default: show tech-support)
        device_dir (str): Device directory to save show tech to (default: flash:)
        remote_server (str): server name in testbed file
        remote_path (str): path to save the file to on the server
        protocol (str): protocol to use to copy (default: scp)
        timeout (int): timeout to copy file (default: 600s)

    Returns
        True on success, False on failure

    The filename is based the prefix + show_tech + timestamp.

    The default prefix is the device name.

    The show tech data will be redirected to a file on the flash filesystem,
    and uploaded to the remote_server via scp. The created show tech
    files will be deleted from the flash filesystem.

    The remote server is assumed to be defined in the testbed file
    including credentials if needed.

    Example server config:

    testbed:
        servers:
            scp1:
                server: 1.2.3.4
                type: scp
                address: 1.2.3.4
                credentials:
                    default:
                        username: test
                        password: 1234

    If no remote server is specified and the connection is done via
    SSH or telnet a temporary http server will be created and the
    show tech file will be sent to the host where the script is running.

    If the device is connected via proxy (unix jump host) and the proxy has
    'socat' installed, the upload will be done via the proxy automatically.
    """
    log.info('Getting show tech-support')

    device_dir = device_dir or 'flash:'

    if prefix and prefix[-1] != '_':
        prefix += '_'
    else:
        prefix = device.name + '_'

    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    filename = '{}{}show_tech_{}.txt'.format(device_dir, prefix, timestamp)
    # Capture show tech to flash
    try:
        device.execute('{} | redirect {}'.format(show_tech_command, filename), timeout=timeout)
    except Exception:
        log.exception('Failed to collect show tech')
        return False

    delete_dialog = Dialog([
        [r'Delete filename .*\?\s*$', 'sendline()', None, True, False],
        [r'Delete .*\[confirm\]\s*$', 'sendline()', None, True, False]
    ])

    if remote_server is not None:
        assert remote_path is not None, 'remote_path should be specified'

        try:
            fu_device = FileUtils.from_device(device)

            fu_device.copyfile(source=filename,
                               destination='{proto}://{host}{path}/{fname}'.format(
                                   proto=protocol,
                                   host=remote_server,
                                   path=remote_path,
                                   fname='{}show_tech_{}.txt'.format(prefix, timestamp)
                               ),
                               timeout_seconds=timeout, device=device)
            device.execute('delete flash:{}show_tech_{}.txt'.format(prefix, timestamp), service_dialog=delete_dialog)
        except Exception:
            log.error('Failed to copy show tech, keeping file on bootflash')
            return False

    else:
        if device.api.copy_from_device(local_path=filename, remote_path=remote_path):
            device.execute('delete flash:{}show_tech_{}.txt'.format(prefix, timestamp), service_dialog=delete_dialog)
        else:
            log.error('Failed to copy show tech, keeping file on {}'.format(device_dir))
            return False

    return True

def show_tech_support_firewall(device, timeout=300):
    """Execute show tech-support firewall command

        Args:
            device  (`obj`): Device object
            timeout (`int`): timeout for the command execution
        Returns:
            True on success, False on failure
    """
    log.info(f"Getting show tech-support firewall")
    cmd = "show tech-support firewall"
    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        log.error(f"Failed to execute command: {cmd}\nError: {e}")
        return False
    return True


def collect_install_log(device):
    """ Collect install failure logs from the device.
    Args:
        device (obj): Device object (required)
    Returns
        None
    """

    archive_filename = None

    log.info("Logging the below to get the install failure logs from device")

    # Add timestamp to the show tech support filename
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    file_name = f"show_tech_support_{timestamp}.txt"

    commands = [
        "show platform software install-manager r0 operation current detail",
        "show platform software install-manager r0 operation history detail",
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

            device.api.copy_from_device(local_path=f"{default_dir}{file_name}", remote_path=runtime.directory)
            if archive_filename:
                device.api.copy_from_device(local_path=f"{archive_filename}", remote_path=runtime.directory)
        except Exception as e:
            log.error(f"Failed to copy the install failure logs to runinfo directory: {e}")
        finally:
            # Reassign the default connection alias to the original alias
            device.default_connection_alias = conn_alias
