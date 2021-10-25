# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_snmp_snmpwalk(
    device, community, ip_address, oid, version="2c", option=None
):
    """ Get snmpwalk output from SNMP device
        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`, optional): SNMP version. Default is "2c"
            option (`str`): Optional command. Default is None
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            None
    """
    if option:
        cmd = "snmpwalk -v {version} -c {community} {ip_address} {oid} {option}".format(
            version=version,
            community=community,
            ip_address=ip_address,
            oid=oid,
            option=option,
        )
    else:
        cmd = "snmpwalk -v {version} -c {community} {ip_address} {oid}".format(
            version=version,
            community=community,
            ip_address=ip_address,
            oid=oid,
        )

    return device.execute(cmd)
