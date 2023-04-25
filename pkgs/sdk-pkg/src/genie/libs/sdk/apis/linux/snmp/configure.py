"""Common configure functions for snmp"""

import logging
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)


def set_snmp_snmpset(
    device, community, ip_address, oid, version="2c", string= None, option=None
):
    """ Snmpset command
        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`): SNMP version
            string (`str`): string command
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = f"snmpset -v {version} -c {community} {ip_address} {oid}"
    if string:
        cmd += f" s {string}"
    if option:
        cmd += f" {option}"
    try:

        return device.execute(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp set on the device. Error:\n{e}")
