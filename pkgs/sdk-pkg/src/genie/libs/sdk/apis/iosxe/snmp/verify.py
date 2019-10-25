"""Common verify functions for SNMP"""

# Python
import logging

# Genie
from pyats.async_ import pcall

# SNMP
from genie.libs.sdk.apis.iosxe.snmp.get import get_snmp_cli_dict, get_snmp_dict

log = logging.getLogger(__name__)


def verify_cli_and_snmp_cpu_memory(
    device,
    snmp_device,
    community,
    ip_address,
    oid,
    id_slot_map,
    snmp_map,
    version,
    load_tolerance=0,
    memory_tolerance=500,
):
    """ Verify CPU and Memory usage information from 
        CLI and SNMP are equivalent

        Args:
            device (`obj`): Device object
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
            load_tolerance (`int`): Tolerance for load information
            memory_tolerance (`int`): Tolerance for memory information
        Returns:
            result (`bool`): Verified result
        Raises:
            None
    """
    result = True
    try:
        cli_dict, snmp_dict = pcall(
            [get_snmp_cli_dict, get_snmp_dict],
            iargs=[
                [device],
                [
                    snmp_device,
                    community,
                    ip_address,
                    oid,
                    id_slot_map,
                    snmp_map,
                    version,
                ],
            ],
        )
    except Exception as e:
        log.error(
            "Failed to get CPU and Memory information "
            "from CLI and SNMP:\n{}".format(e)
        )
        return False

    if not snmp_dict or not cli_dict:
        log.error(
            "Failed to get CPU and Memory information "
            "from CLI and SNMP"
        )
        return False

    for slot, data in snmp_dict.items():
        if slot in cli_dict:
            for key, value in data.items():
                if "min" in key:
                    cli_value = (
                        cli_dict.get(slot, {})
                        .get("load_average", {})
                        .get(key, 0)
                        * 100
                    )
                    if abs(value - cli_value) > load_tolerance:
                        log.error(
                            "Load average {} of {} didn't match:\n"
                            "SNMP value: {}  CLI value: {}\n ".format(
                                key, slot, value, cli_value
                            )
                        )
                        result = False
                    else:
                        log.info(
                            "Load average {} of {} matched:\n"
                            "SNMP value: {}  CLI value: {}\n ".format(
                                key, slot, value, cli_value
                            )
                        )
                else:
                    cli_value = (
                        cli_dict.get(slot, {}).get("memory", {}).get(key, 0)
                    )
                    if abs(value - cli_value) > memory_tolerance:
                        log.error(
                            "Memory {} of {} did't match:\n"
                            "SNMP value: {}  CLI value: {}\n ".format(
                                key, slot, value, cli_value
                            )
                        )
                        result = False
                    else:
                        log.info(
                            "Memory {} of {} matched:\n"
                            "SNMP value: {}  CLI value: {}\n ".format(
                                key, slot, value, cli_value
                            )
                        )
        else:
            log.error("Slot {} is not in parsed CLI output".format(slot))
            result = False

    return result


def is_snmp_message_received(message, server, output):
    """ Verify if a message was received in snmp server
        Args:
            output ('obj'): Tcpdump output
            server ('str'): Syslog server address
            message ('str'): Message to be verified in Syslog server
        Returns:
            True
            False
        Raises:
            None
    """

    for packet in output:
        if packet.dst == server:
            try:
                varbindlist = (
                    packet.getlayer("IP")
                    .getlayer("UDP")
                    .getlayer("SNMP")
                    .getlayer("SNMPtrapv1")
                    .varbindlist
                )

            except AttributeError:
                continue

            for item in varbindlist:
                try:
                    output = item.value.val.decode()
                except (AttributeError, UnicodeDecodeError):
                    continue

                if message in output:
                    log.info(
                        "Message '{message}' has been found in SNMP "
                        "server {ip}".format(message=message, ip=server)
                    )
                    log.info("Packet details")
                    log.info(packet.show(dump=True))
                    return True

    log.error(
        "Message '{message}' has not been found in SNMP "
        "server {ip}".format(message=message, ip=server)
    )

    return False
