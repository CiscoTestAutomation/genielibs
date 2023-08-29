"""Common get info functions for lisp"""

# Python
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)

def get_lisp_instance_id_running_config(device, instance_id):
    """ Get parsed running BGP config
        Args:
            device ('obj'): Device object
            instance_id ('int'): instance id
        Returns:
            Dictionary
                Example {
                            'instance-id': int,
                            'multicast_address': str
                        }
    """
    try:
        output = device.execute("show running-config | section instance-id {instance_id}"
                                 .format(instance_id=instance_id))
    except SubCommandFailure:
        log.info("Command has not returned any results")
        return {}

    # instance-id 699
    r1 = re.compile(r"^instance\-id\s+(?P<instance>\d+)$")
    # broadcast-underlay 239.0.0.7
    r2 = re.compile(r"broadcast\-underlay\s+(?P<multicast_address>\S+)$")

    lisp_dict = {}

    for line in output.splitlines():
        line = line.strip()

        m = r1.match(line)
        if m:
            groups = m.groupdict()
            instance_id = int(groups['instance'])
            instance_id_dict = lisp_dict.setdefault("instance_id", instance_id)
            continue

        m = r2.match(line)
        if m:
            groups = m.groupdict()
            multicast_address = str(groups['multicast_address'])
            lisp_dict["multicast_address"] = multicast_address
            continue

    return lisp_dict

