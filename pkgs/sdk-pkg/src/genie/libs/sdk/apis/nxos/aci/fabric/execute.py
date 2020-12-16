""" ACI Fabric Execute type APIs """

import json
import logging
import os

from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)

def execute_register_nodes(device, nodes, rest_alias='rest'):
    """ Registers the provided nodes to the fabric

    Args:
        device (obj): The device to execute on

        nodes (list): Names of the nodes to register. These nodes must
            have 'serialnum' and 'node_id' defined under the
            testbed.device.custom key.

        rest_alias (str, optional): Alias for the REST connection. Defaults
            to rest.

    Returns:
        True if registering is successful
        False if registering fails

    Raises:
        N/A
    """

    try:
        device.connect(via=rest_alias, alias=rest_alias)
    except Exception as e:
        log.error("Failed to connect to '{dev}' using alias '{alias}'. Error: {e}"
                  .format(dev=device.name, alias=rest_alias, e=str(e)))
        return False

    failed_to_register = []

    for node in nodes:
        if node not in device.testbed.devices:
            failed_to_register.append(
                "The node '{}' does not exist in the testbed.".format(node))
            continue

        node = device.testbed.devices[node]

        serialnum = node.custom.get('serialnum')
        node_id = node.custom.get('node_id')
        if not serialnum or not node_id:
            failed_to_register.append(
                "'{dev}' is missing one of the following "
                "attributes({dev}.custom.<attribute>) from the testbed file: "
                "['serialnum', 'node_id']".format(dev=node))
            continue

        payload = {
            "fabricNodeIdentP": {
                "attributes": {
                    "dn": "uni/controller/nodeidentpol/nodep-{serialnum}".format(serialnum=serialnum),
                    "serial": serialnum,
                    "nodeId": str(node_id),
                    "name": node.name
                }
            }
        }

        try:
            device_rest = getattr(device, rest_alias)
        except AttributeError:
            failed_to_register.append(
                "'{dev}' does not has a connection with the alias '{alias}' "
                "defined.".format(dev=device.name,
                                  alias=rest_alias))
            continue

        try:
            device_rest.post(
                dn='api/node/mo/uni/controller/nodeidentpol.json',
                payload=json.dumps(payload))
        except Exception as e:
            failed_to_register.append("Node registration commands failed! "
                                      "Error: {}".format(str(e)))
            continue

    if failed_to_register:
        log.warning("Failed to register all nodes. See the following list of "
                    "issues: {}".format(failed_to_register))
        return False
    else:
        return True

def execute_clean_controller_fabric(device, max_time=90):
    """ Cleans the controller part of the ACI fabric

    Args:
        device (obj): Device to execute on

        max_time (int, optional): Max time in seconds allowed for 'acidiag
            touch clean'. Defaults to 90.

    Returns:
        True if successful
        False if failed

    Raises:
        N/A
    """

    clean_dialog = Dialog([
        Statement(
            pattern=r".*This command will wipe out this device\, Proceed\? \[y\/N\].*",
            action='sendline(y)'
        )
    ])

    try:
        device.execute(
            'acidiag touch clean',
            timeout=max_time,
            reply=clean_dialog,
            error_pattern=[r".*Cant find image.*"])
    except Exception as e:
        log.error("Failed to execute the command. Error: {}".format(str(e)))
        return False
    else:
        return True

def execute_clean_node_fabric(
        device,
        hostname=None,
        copy_protocol=None,
        image=None,
        destination_dir=None,
        copy_max_time=300,
        max_time=90):
    """ Cleans the node part of the ACI fabric

    Args:
        device (obj): Device to execute on

        hostname (str, optional): Hostname to copy boot image from if its not
            found. Defaults to None.

        copy_protocol (str, optional): Protocol to use for copying boot image
            if its not found. Defaults to None

        image (str, optional): Boot image to copy if its not found. Defaults
            to None.

        destination_dir (str, optional): Directory to copy the boot image to.
            Defaults to None.

        copy_max_time (int, optional): Max time in seconds allowed for copying
            the image. Defaults to 300.

        max_time (int, optional): Max time in seconds allowed for executing
            clean commands. Defaults to 90.

    Returns:
        True if successful
        False if failed

    Raises:
        N/A
    """

    clean_dialog = Dialog([
        Statement(
            pattern=r".*This command will wipe out this device\, Proceed\? \[y\/N\].*",
            action='sendline(y)'
        )
    ])

    # Check if a boot image is configured and exists
    boot_cfg = device.execute(
        'cat /mnt/cfg/0/boot/grub/menu.lst.local | grep boot')
    if boot_cfg:
        boot_cfg = boot_cfg.split()[1]

        if ':' in boot_cfg:
            boot_cfg = boot_cfg.split(':')[1]

        bootflash = device.execute('ls bootflash/')

        if boot_cfg in bootflash:
            image_found = True
        else:
            image_found = False

    else:
        image_found = False

    # There is no boot image and copy to device is not specified.
    # Can no longer proceed.
    if (not image_found and
            not hostname and
            not copy_protocol and
            not image and
            not destination_dir):
        log.error("No boot image exists and arguments to copy an image were "
                  "not specified.")
        return False

    # If the image does not exist on the device and copy image args are
    # specified, then copy the image.
    elif not image_found:
        server = hostname
        protocol = copy_protocol
        remote_path = image
        local_path = destination_dir

        testbed = device.testbed
        if (protocol in testbed.servers and
                'default' in testbed.servers[protocol].credentials and
                'username' in testbed.servers[protocol].credentials.default and
                'password' in testbed.servers[protocol].credentials.default):
            username = testbed.servers[protocol].credentials.default.username
            password = testbed.servers[protocol].credentials.default.password
        else:
            username = None
            password = None

        try:
            device.api.copy_to_device(
                protocol=protocol,
                server=server,
                remote_path=remote_path,
                local_path=local_path,
                timeout=copy_max_time,
                username=username,
                password=password
            )
        except Exception as e:
            log.error("Failed to copy image to the device. Error: {}"
                      .format(str(e)))
            return False
        else:
            boot_cfg = os.path.basename(remote_path)

    cmds = ['/bin/setup-clean-config.sh',
            '/bin/setup-bootvars.sh {}'.format(boot_cfg)]

    try:
        device.execute(
            cmds,
            timeout=max_time,
            reply=clean_dialog,
            error_pattern=[r".*Cant find image.*"])
    except Exception as e:
        log.error("Failed during cleaning the device. Error: {}".format(str(e)))
        return False
    else:
        return True
