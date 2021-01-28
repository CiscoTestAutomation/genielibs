""" Execute type APIs for APIC Fabric"""

import json
import logging

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
