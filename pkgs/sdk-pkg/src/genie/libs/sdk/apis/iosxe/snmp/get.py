"""Common get info functions for SNMP"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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
            version (`str`): SNMP version
            option (`str`): Optional command
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


def get_snmp_id_slot_map(device, community, ip_address, oids, version="2c"):
    """ Get id-slot mapping from SNMP server

        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oids (`list`): Oid codes
            version (`str`): SNMP version
        Returns:
            id_slot_map (`dict`): Id slot mapping
                ex: {"1": "sip1", "7": "rp0", "9": "esp0"}
        Raises:
            None
    """
    sub_map1 = {}
    pids = []
    out1 = get_snmp_snmpwalk(device, community, ip_address, oids[0], version)

    # SNMPv2-SMI::enterprises.10.69.109.1.10.4.1.2.9 = INTEGER: 9036
    p = re.compile(r"\.(?P<sid>[\d]+) += +.*: +(?P<pid>[\d]+)")
    found1 = p.findall(out1)

    for item in found1:
        sub_map1.update({item[0]: item[1]})
        pids.append(item[1])

    sub_map2 = {}
    option = "| grep -E '{}'".format("|".join(pids))
    out2 = get_snmp_snmpwalk(
        device, community, ip_address, oids[1], version, option
    )

    # SNMPv2-SMI::mib-10.106.1.1.1.1.7.7031 = STRING: "cpu R0/0"
    p2 = re.compile(
        r'(?P<pid>{}).* += +.*: +"cpu +(?P<slot>[\w]+)\/'.format(
            "|".join(pids)
        )
    )
    found2 = p2.findall(out2)

    for item in found2:
        if re.match(r"^\d", item[1]):
            slot = "sip" + item[1]
        else:
            slot = item[1].replace("F", "esp").replace("R", "rp")
        sub_map2.update({item[0]: slot.lower()})

    id_slot_map = {}
    for sid, pid in sub_map1.items():
        slot = sub_map2.get(pid)
        id_slot_map.update({sid: slot})

    return id_slot_map


def get_snmp_dict(
    snmp_device,
    community,
    ip_address,
    oid,
    id_slot_map,
    snmp_map,
    version="2c",
):
    """ Get CPU and memory usage information from SNMP device

        Args:
            snmp_device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            id_slot_map (`dict`): Id-slot mapping
                ex: {"1": "sip1", "7": "rp0", "9": "esp0"}
            snmp_map (`dict`): SNMP-CLI mapping
                ex: {'12': 'used', '13': 'free', '24': '1_min',
                     '25': '5_min', '26': '15_min', '27': 'committed'}
            version (`str`): SNMP version
        Returns:
            snmp_dict (`dict`): Information dictionary
                ex: {"sip0": {
                     "used": 575640,
                     "free": 389036,
                     "1_min": 3,
                     "5_min": 4,
                     "15_min": 0,
                     "committed": 869368}}
    """
    out = get_snmp_snmpwalk(snmp_device, community, ip_address, oid, version)

    snmp_dict = {}

    for key, slot in id_slot_map.items():
        slot_dict = snmp_dict.setdefault(slot, {})

        # SNMPv2-SMI::enterprises.10.69.109.1.10.4.1.12.1 = Gauge32: 465360
        p = re.compile(
            r"(?P<lid>[\d]+)\.{} += +.*: +(?P<value>[\d]+)".format(key)
        )
        found = p.finditer(out)

        for item in found:
            lid = item.groups()[0]
            value = item.groups()[1]
            if lid in snmp_map:
                slot_dict.update({snmp_map[lid]: int(value)})

    return snmp_dict


def get_snmp_cli_dict(device):
    """ Get CPU and memory usage information from CLI

        Args:
            device (`obj`): Device object
        Returns:
            None
            out (`dict`): Information dictionary
                ex: {"sip0": {
                        "load_average": {
                            "status": "healthy",
                            "1_min": 0.07,
                            "5_min": 0.02,
                            "15_min": 0.0
                        },
                        "memory": {
                            "status": "healthy",
                            "total": 964676,
                            "used": 575896,
                            "used_percentage": 60,
                            "free": 388780,
                            "free_percentage": 40,
                            "committed": 869972,
                            "committed_percentage": 90
                        },
                        "cpu": {
                            "0": {
                                "user": 3.4,
                                "system": 0.8,
                                "nice_process": 0.0,
                                "idle": 95.69,
                                "irq": 0.0,
                                "sirq": 0.1,
                                "waiting": 0.0
                            }
                        }}}
        Raises:
            None
    """
    try:
        out = device.parse(
            "show platform software status control-processor brief"
        )
    except SchemaEmptyParserError:
        return {}

    return out["slot"]
