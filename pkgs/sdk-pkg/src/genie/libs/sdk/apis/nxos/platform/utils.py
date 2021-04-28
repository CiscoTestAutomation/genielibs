# Python
import re
import time
import logging

# Unicon
from unicon import Connection
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)

# Logger
log = logging.getLogger(__name__)


def write_erase_reload_device_without_reconfig(
    device,
    via_console,
    reload_timeout,
    username=None,
    password=None,
    reload_creds=None,
    reload_hostname='Router',
):
    """Execute 'write erase' on device and reload without reconfiguring.

        Args:
            device(`obj`): Device object
            via_console(`str`): Via to use to reach the device console.
            reload_timeout(`int`): Maximum time to wait for reload to complete
            reload_creds(`str or list`): Creds to apply if reloading device asks
    """


    # Set 'write erase' dialog
    wr_dialog = Dialog(
        [
          Statement(
            pattern=r'.*Do you wish to proceed anyway\? \(y/n\)\s*\[n\]',
            action="sendline(y)",
            loop_continue=True,
            continue_timer=False)
        ]
    )

    # Execute 'write erase' command
    log.info("\n\nExecuting 'write erase' on device '{}'".format(device.name))
    try:
        device.execute("write erase", reply=wr_dialog)
    except Exception as e:
        raise Exception(
            "Error while executing 'write erase' on device '{}' : {}".format(
                device.name, e
            )
        ) from e
    else:
        log.info(
            "Successfully executed 'write erase' command on device '{}'".format(
                device.name
            )
        )

    # Collect device base information before reload
    os = device.os
    hostname = device.name

    username, password =  device.api.get_username_password(
        device = device,
        username = username,
        password = password,
        creds = reload_creds)

    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])

    # Execute 'reload' command
    log.info("\n\nExecuting 'reload' on device '{}'".format(device.name))
    try:
        device.reload(
            prompt_recovery=True, reload_creds=reload_creds,
            timeout = reload_timeout)
        device.disconnect()
    except SubCommandFailure:
        # Disconnect and destroy the connection
        log.info(
            "Sucessfully executed 'reload' command on device {}".format(
                device.name
            )
        )
        log.info(
            "Disconnecting and destroying handle to device {}".format(
                device.name
            )
        )
        device.destroy()
    except Exception as e:
        raise Exception(
            "Error while reloading device '{}'".format(device.name)
        ) from e

    # Wait until reload has completed and device can be reachable
    log.info(
        "\n\nWaiting '{}' seconds for device to reboot after reload...".format(
            reload_timeout
        )
    )
    time.sleep(reload_timeout)

    # Reconnect to device
    log.info(
        "\n\nReconnecting to device '{}' after reload...".format(hostname)
    )
    new_device = Connection(
        credentials=dict(default=dict(username=username, password=password)),
        os=os,
        hostname=reload_hostname,
        start=["telnet {ip} {port}".format(ip=ip, port=port)],
        prompt_recovery=True,
    )
    try:
        new_device.connect()
    except (ConnectionError, TimeoutError) as e:
        # Connection or Timeout Error but 'no' has been sent
        # simply destroy handle at this point
        new_device.disconnect()
        log.info(
            "Reconnected to device '{}' after 'write erase' and reload'".format(
                hostname
            )
        )
    except Exception as e:
        raise Exception(
            "Error reconnecting to device '{}' after 'write erase'"
            " and reload".format(hostname)
        ) from e
    else:
        new_device.disconnect()
        log.info(
            "Successully reconnected to device '{}' after 'write erase' "
            "and reload'".format(hostname)
        )


def is_connected_via_vty(device, alias=None):
    ''' Check if we are connected via VTY
    '''
    if alias:
        conn = getattr(device, alias)
    else:
        conn = device
    show_users = conn.execute(r'show users | inc \*')
    if re.search(' pts', show_users):
        return True
    return False
