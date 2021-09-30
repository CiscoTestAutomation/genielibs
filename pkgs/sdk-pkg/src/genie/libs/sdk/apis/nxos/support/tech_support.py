import re
import psutil
import logging
from datetime import datetime

from unicon.eal.dialogs import Dialog
from genie.libs.filetransferutils import FileUtils
from genie.libs.filetransferutils import FileServer

log = logging.getLogger(__name__)


def get_show_tech(device,
                  prefix='',
                  show_tech_command='show tech-support',
                  device_dir=None,
                  remote_server=None,
                  remote_path=None,
                  protocol='scp',
                  vrf='management',
                  timeout=600):
    """ Collect show tech-support from the device.

    Args:
        device (obj): Device object (optional)
        prefix (str): filename prefix (optional)
        show_tech_command (str): command to execute (default: show tech-support)
        device_dir (str): Device directory to save show tech to (default: bootflash:)
        remote_server (str): server name in testbed file
        remote_path (str): path to save the file to on the server
        protocol (str): protocol to use to copy (default: scp)
        vrf (str): VRF to use (default: management)
        timeout (int): timeout to copy file (default: 600s)

    Returns
        True on success, False on failure

    The filename is based the prefix + show_tech + timestamp.

    The default prefix is the device name.

    The show tech data will be redirected to a file on the bootflash,
    compressed with tar and uploaded to the target_host via scp.
    The created show tech files will be deleted from the bootflash.

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

    device_dir = device_dir or 'bootflash:'

    if prefix and prefix[-1] != '_':
        prefix += '_'
    else:
        prefix = device.name + '_'

    # Capture show tech to flash
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    filename_without_extention = '{}{}show_tech_{}'.format(device_dir, prefix, timestamp)
    filename = filename_without_extention + '.txt'

    try:
        device.execute('{} > {}'.format(show_tech_command, filename), timeout=timeout)
        device.execute('tar create {} gz-compress {}'.format(filename_without_extention, filename))

        delete_dialog = Dialog([
            [r'Do you want to delete .* \[y\]\s*$', 'sendline()', None, True, False]
        ])
        device.execute('delete {}'.format(filename), reply=delete_dialog)
    except Exception:
        log.exception('Failed to collect show tech')
        return False

    filename = '{}.tar.gz'.format(filename_without_extention)

    if remote_server is not None:
        assert remote_path is not None, 'remote_path should be specified'

        try:
            fu_device = FileUtils.from_device(device)

            fu_device.copyfile(source=filename,
                               destination='{proto}://{host}{path}/{fname}'.format(
                                   proto=protocol,
                                   host=remote_server,
                                   path=remote_path,
                                   fname='{}show_tech_{}.tar.gz'.format(prefix, timestamp)
                               ),
                               vrf=vrf,
                               timeout_seconds=timeout, device=device)
            device.execute('delete {}'.format(filename), reply=delete_dialog)
        except Exception:
            log.error('Failed to copy show tech, keeping file on {}'.format(device_dir))
            return False

    else:

        if device.api.copy_from_device(local_path=filename, remote_path=remote_path):
            device.execute('delete {}'.format(filename), reply=delete_dialog)
        else:
            log.error('Failed to copy show tech, keeping file on {}'.format(device_dir))
            return False

    return True
