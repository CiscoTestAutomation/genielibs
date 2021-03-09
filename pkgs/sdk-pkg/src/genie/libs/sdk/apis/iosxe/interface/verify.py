"""Common verify functions for interface"""

# Python
import re
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from pyats.utils.objects import find, R
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Utils
from genie.libs.sdk.apis.utils import get_config_dict
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)
from genie.utils import Dq

# Interface
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_running_config,
)

log = logging.getLogger(__name__)


def verify_interface_config_carrier_delay(
    device, interface, max_time=60, check_interval=10, flag=True
):
    """Verify interface carrier_delay config in - show run interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
            flag (`bool`): True if verify has carrier delay
                           False if verify no carrier delay
        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.execute("show run interface {}".format(interface))

        cfg_dict = get_config_dict(out)
        key = "interface {}".format(interface)

        if key in cfg_dict:
            for line in cfg_dict[key].keys():
                if "carrier-delay" in line:
                    result = True
                    break
            else:
                result = False
        else:
            result = False

        if flag == result:
            return True
        timeout.sleep()

    return False


def verify_interface_config_ospf_bfd(
    device, interface, max_time=60, check_interval=10, flag=True
):
    """Verify interface ospf bfd config in - show run interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
            flag (`bool`): True if verify shutdown 
                           False if verify no shutdown
        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.execute("show run interface {}".format(interface))

        cfg_dict = get_config_dict(out)
        key = "interface {}".format(interface)

        if key in cfg_dict and "ip ospf bfd" in cfg_dict[key]:
            result = True
        else:
            result = False

        if flag == result:
            return True
        timeout.sleep()

    return False


def verify_interface_mtu_packets(pkts, peer_ip):
    """ Verify one mtu packet split into two packets

        Args:
            pkts (`obj`): Pcap object
            peer_ip (`str`): Ping ip address
        Returns:
            result (`bool`): Verified result
    """
    pkt_dict = {}
    for pkt in pkts:
        if (
            pkt.haslayer("IP")
            and pkt["IP"].dst == peer_ip
            and pkt["IP"].proto == 1
        ):
            pid = pkt["IP"].id
            if pid in pkt_dict:
                pkt_dict[pid].append(pkt)
            else:
                pkt_dict.setdefault(pid, [pkt])

    for pid, pkt_list in pkt_dict.items():
        if len(pkt_list) != 2:
            log.info(
                "Found packet with id '{id}' didn't split into two packets:\n{pkt}\n ".format(
                    id=pid, pkt="\n".join(pkt.summary() for pkt in pkt_list)
                )
            )
            return False
        else:
            log.info(
                "Found packet with id '{id}' split into two packets:\n{pkt}\n ".format(
                    id=pid, pkt="\n".join(pkt.summary() for pkt in pkt_list)
                )
            )
    else:
        return True


def is_interface_changed_state_log(device, interface):
    """ Verify interface didn't flap in the log

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            result(`str`): verify result
    """
    result = []
    out = device.parse("show logging")
    p = re.compile(r".*Interface {}, changed state to.*".format(interface))
    for line in out["logs"]:
        if p.match(line):
            result.append(line)
    return "\n".join(result)


def verify_interface_no_error_counters(device, interface, counters=None):
    """ Verify no error counters

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            counters (`list`): Extra counters to be checked
        Returns:
            None
    """
    log.info(
        "Checking counters errors on interface {} on device {}".format(
            interface, device.name
        )
    )

    counter_list = [
        "in_errors",
        "in_crc_errors",
        "in_frame",
        "in_overrun",
        "in_ignored",
        "out_errors",
        "out_collision",
    ]
    if counters:
        counter_list.extend(counters)

    try:
        out = device.parse("show interfaces {}".format(interface))
        counters_dict = out[interface]["counters"]
    except Exception as e:
        log.error(e)
        raise Exception("Failed to get counters on {}".format(interface))

    for key in counter_list:
        if counters_dict[key] != 0:
            raise Exception(
                "Found counter {} has errors on {}".format(key, interface)
            )


def verify_interface_config_shutdown(
    device, interface, max_time=60, check_interval=10, flag=True
):
    """Verify interface have shutdown in - show run interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
            flag (`bool`): True if verify shutdown 
                           False if verify no shutdown
        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.execute("show run interface {}".format(interface))

        cfg_dict = get_config_dict(out)
        key = "interface {}".format(interface)

        if key in cfg_dict and "shutdown" in cfg_dict[key]:
            result = True
        else:
            result = False

        if flag == result:
            return True
        timeout.sleep()

    return False


def verify_interface_config_no_shutdown(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface doesn't have shutdown in - show run interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
    """
    return verify_interface_config_shutdown(
        device, interface, max_time, check_interval, False
    )


def verify_interface_state_up(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is up and and line protocol is up

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.parse("show interfaces {}".format(interface))
        oper_status = out[interface]["oper_status"]
        line_protocol = out[interface]["line_protocol"]
        if oper_status == line_protocol == "up":
            return True
        timeout.sleep()

    return False


def verify_interface_state_down(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is down and and line protocol is down

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.parse("show interfaces {}".format(interface))
        oper_status = out[interface]["oper_status"]
        line_protocol = out[interface]["line_protocol"]
        enabled = out[interface]["enabled"]
        if oper_status == line_protocol == "down" and enabled == True:
            return True
        timeout.sleep()

    return False


def verify_interface_state_admin_down(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is administratively down and line protocol is down

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.parse("show interfaces {}".format(interface))
        oper_status = out[interface]["oper_status"]
        line_protocol = out[interface]["line_protocol"]
        enabled = out[interface]["enabled"]
        if oper_status == line_protocol == "down" and enabled == False:
            return True
        timeout.sleep()

    return False


def verify_interface_ip_route_connected(
    device,
    interface,
    ip_address,
    prefix,
    vrf,
    max_time=60,
    check_interval=10,
    flag=True,
):
    """Verify interface IP address route is present in
        - show ip route connected

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ip_address (`str`): Interface ip address
            prefix (`int`): prefix length
            vrf (`str`): vrf name
            flag (`bool`): True if verify present 
                           False if verify not present
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)
    if prefix:
        ip_address = "{ip}/{prefix}".format(ip=ip_address, prefix=prefix)

    reqs = R(
        [
            "vrf",
            "(?P<vrf>.*)",
            "address_family",
            "ipv4",
            "routes",
            ip_address,
            "next_hop",
            "outgoing_interface",
            interface,
            "outgoing_interface",
            interface,
        ]
    )

    while timeout.iterate():
        try:
            out = device.parse("show ip route connected")
        except Exception as e:
            log.info(e)
            timeout.sleep()
            continue

        found = find([out], reqs, filter_=False, all_keys=True)

        if flag == bool(found):
            return True
        timeout.sleep()

    return False


def verify_no_interface_ip_route_connected(
    device, interface, ip_address, prefix, vrf, max_time=60, check_interval=10
):
    """Verify interface IP address route is not present in
        - show ip route connected

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            ip_address (`str`): Interface ip address
            prefix (`int`): prefix length
            vrf (`str`): vrf name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
    """
    return verify_interface_ip_route_connected(
        device,
        interface,
        ip_address,
        prefix,
        vrf,
        max_time,
        check_interval,
        False,
    )


def verify_interface_secondary_addresses(
    device, connected_sec_addr, local_sec_addr, vrf, address_family, start, end
):
    """ Verify secondary addresses are present in RIB

        Args:
            device (`obj`): Device object
            connected_sec_addr (`str`): Secondary ip address for connected
            local_sec_addr (`str`): Secondary ip address for local
            vrf (`str`): Vrf name
            address_family (`str`): Address family
            start (`int`): start number on ip
            end (`int`): end number on ip
        Returns:
            list of address not in RIB
    """
    ip_list = []
    cmd = "show ip route connected"
    try:
        out = device.parse(cmd)
        route_dict = out["vrf"][vrf]["address_family"][address_family][
            "routes"
        ]
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to parse {}".format(cmd))

    for x in range(end - start):
        c = connected_sec_addr.format(x=x + 1)
        l = local_sec_addr.format(x=x + 1)
        if c not in route_dict:
            ip_list.append(c)
        if l not in route_dict:
            ip_list.append(l)

    return ip_list


def verify_interface_port_channel_status_down(device, port_channel):
    """ Verify Port Channel state is down

        Args:
            device('obj'): device to change hostname on
            port_channel('str'): Port channel interface

        Returns:
            N/A
    """

    out = device.parse("show etherchannel summary")

    if out and "interfaces" in out:
        for intf in out["interfaces"]:
            if intf == port_channel.capitalize():
                if out["interfaces"][intf]["oper_status"] != "down":
                    raise Exception("Interface {} is enabled".format(intf))

                if (
                    "members" in out["interfaces"][intf]
                    or "protocol" in out["interfaces"][intf]
                ):
                    raise Exception(
                        "Interface {} has members or protocol defined".format(
                            intf
                        )
                    )


def verify_interface_port_channel_status_changed(device, port_channel, status):
    """ Verify Port channel status

        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel interface
            status (`str`): Interface status
        Returns:
            result(`bool`): verify result
    """
    out = device.parse("show etherchannel summary")

    if (
        out
        and "interfaces" in out
        and port_channel.capitalize() in out["interfaces"]
        and "members" in out["interfaces"][port_channel.capitalize()]
    ):
        for intf in out["interfaces"][port_channel.capitalize()]["members"]:
            if (
                out["interfaces"][port_channel.capitalize()]["members"][intf][
                    "flags"
                ]
                == status
            ):
                log.info(
                    "Interface {intf} status has changed to {status}".format(
                        intf=intf, status=status
                    )
                )
                return True

    log.info(
        "None of the interfaces status have changed to {status}".format(
            intf=intf, status=status
        )
    )
    return False


def verify_interface_port_channel_status_up_and_interfaces_bundled(
    device, port_channel, interface, max_time, check_interval
):
    """ Verify Port channel state and the bundled interfaces

        Args:
            device('obj'): device to change hostname on
            port_channel('str'): Port channel interface
            interface('str'): Interface name
            max_time ('int'): maximum time to check
            check_interval ('int'): how often to check

        Returns:
            result(`bool`): verify result
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.parse("show etherchannel summary")
        if (
            "members" in out["interfaces"][port_channel.capitalize()]
            and out["interfaces"][port_channel.capitalize()]["members"][
                Common.convert_intf_name(interface)
            ]["bundled"]
        ):
            return True
        timeout.sleep()

    return


def verify_interface_bundled_interfaces_mode(device, interfaces, port_channel, lacp_id):
    """ Verify bundled interfaces mode

        Args:
            device (`obj`): Device object
            interfaces (`list`): Interfaces list
            port_channel (`str`): Port channel interface
            lacp_id (`int`): lacp ID
        Returns:
            None
    """
    out = device.parse("show lacp {id} internal".format(id=lacp_id))

    intfs_list = interfaces[0:3]
    mode_list = ["S", "S", "S", "F"]

    for intf, mode in zip(intfs_list, mode_list):
        intf = Common.convert_intf_name(intf)
        if intf not in out["interfaces"][port_channel.capitalize()]["members"]:
            raise Exception(
                "Interface {intf} is not in found under"
                " the port channel as expected".format(intf=intf)
            )
        if (
            mode
            not in out["interfaces"][port_channel.capitalize()]["members"][
                intf
            ]["flags"]
        ):
            raise Exception(
                "Interface {intf} is not in the expected"
                " mode {mode}".format(intf=intf, mode=mode)
            )
        else:
            log.info(
                "Interface {intf} is in the expected mode {mode}".format(
                    intf=intf, mode=mode
                )
            )
            continue

    return


def verify_interface_port_channel_status_bundled(
    device, port_channel, max_time, check_interval, bundled_count, down_count
):
    """ Verify bundled interfaces mode

        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel interface
            max_time ('int'): maximum time to check
            check_interval ('int'): how often to check
        Returns:
            result(`bool`): verify result
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.parse("show etherchannel summary")

        if (
            out
            and "interfaces" in out
            and port_channel.capitalize() in out["interfaces"]
            and "members" in out["interfaces"][port_channel.capitalize()]
        ):
            bundled_count = 0
            down_count = 0
            for intf in out["interfaces"][port_channel.capitalize()][
                "members"
            ]:
                if out["interfaces"][port_channel.capitalize()]["members"][
                    intf
                ]["bundled"]:
                    bundled_count += 1
                elif (
                    "D"
                    in out["interfaces"][port_channel.capitalize()]["members"][
                        intf
                    ]["flags"]
                ):
                    down_count += 1

                if bundled_count == 3 and down_count == 1:
                    return True
        timeout.sleep()

    return False


def verify_interface_port_channel_in_no_use(
    device, port_channel, max_time, check_interval
):
    """ Verify bundled interfaces mode

        Args:
            device (`obj`): Device object
            port_channel (`str`): Port channel interface
            max_time ('int'): maximum time to check
            check_interval ('int'): how often to check
        Returns:
            result(`bool`): verify result
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = device.parse("show etherchannel summary")

        if (
            out
            and "interfaces" in out
            and port_channel.capitalize() in out["interfaces"]
        ):
            if "M" in out["interfaces"][port_channel.capitalize()]["flags"]:
                return True
        timeout.sleep()

    return False


def is_interface_present_running_config(device, interface):
    """ Verify if interface is present in running-config
        Args:
            device ('obj')      : Device object
            interface ('str')   : Interface

        Raises:
            SubCommandFailure
            Exception
        Returns
            True
            False
    """

    try:
        output = get_interface_running_config(
            device=device, interface=interface
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(str(e))
    except Exception as e:
        raise Exception(str(e))

    return bool(output)


def verify_interface_config_rejected(device, interface):
    """ Verify if it fails when trying to configure an interface
        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
        Returns:
            True: Rejected configuration 
            False: Accepted configuration
        Raises:
            None
    """
    try:
        device.configure("int {interface}".format(interface=interface))
    except SubCommandFailure as e:
        return True

    return False


def is_interface_traffic_flowing_at_rate(
    interface_rate, tgn_tx_rate, tolerance
):
    """ Verify if interface traffic is flowing at generated rate
        Args:
            interface_rate ('float'): Interface rate
            tgn_tx_rate ('float'): Generated rate
            tolerance ('float'): Margin of error in percentage 

        Returns:
            True
            False
    """
    tgn_tx_rate = float(tgn_tx_rate)

    tolerance_less = tgn_tx_rate - ((tolerance / 100) * tgn_tx_rate)
    tolerance_more = tgn_tx_rate + ((tolerance / 100) * tgn_tx_rate)
    if tolerance_less <= interface_rate and interface_rate <= tolerance_more:
        return True


def verify_interface_description_in_running_config(
    device, interface, description
):
    """Verify interface description in show running-config

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            description (`str`): Interface description

        Returns:
            result(`bool`): verify result
    """
    try:
        output = get_running_config_section_dict(
            device, interface + "$"
        )
    except Exception as e:
        log.error(str(e))
        raise Exception(
            "Failed to find interface {} through show running-config".format(
                interface
            )
        )

    intf = "interface {}".format(interface)
    desc = "description {}".format(description)
    try:
        result = isinstance(output[intf][desc], dict)
    except KeyError:
        return False

    return result


def verify_interface_description_in_show_interfaces(
    device, interface, description
):
    """Verify interface description in show interfaces <interface>

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            description (`str`): Interface description

        Returns:
            result(`bool`): verify result
    """
    cmd = "show interfaces {interface}".format(interface=interface)

    try:
        output = device.parse(cmd)
    except SchemaEmptyParserError as e:
        log.error(str(e))
        raise SchemaEmptyParserError("Failed to execute {}".format(cmd))

    if output[interface].get("description", "") == description:
        return True

    return False


def verify_interface_errors(device,
                            interface,
                            expected_value,
                            input=False,
                            output=False,
                            max_time=30,
                            check_interval=10):
    """ Verify interface input and output errors

        Args:
            device (`obj`): Device object
            interface (`str`): Pass interface in show command
            expected_value (`int`, Optional): Expected errors values
            input (`bool`, Optional): True if input errors to verify. Default to False.
            output (`bool`, Optional): True if output errors to verify. Default to False.
            max_time (`int`, Optional): Max time, default: 60 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds

        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            cmd = 'show interface {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Any(): {
        #     Optional('counters'): {
        #         Optional('in_errors'): int,

        interface, data = next(iter(out.items()))
        data = Dq(data)
        if input and output:
            input_errors = data.get_values("in_errors", 0)
            output_errors = data.get_values("out_errors", 0)
            if input_errors == output_errors == expected_value:
                return True
        elif input:
            input_errors = data.get_values("in_errors", 0)
            if input_errors == expected_value:
                return True
        elif output:
            output_errors = data.get_values("out_errors", 0)
            if output_errors == expected_value:
                return True

        timeout.sleep()
        continue

    return False


def verify_interface_state_admin_up(
    device, interface, max_time=60, check_interval=10
):
    """Verify interface state is administratively up and line protocol is up

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): True if is up else False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'show interfaces {interface}'.format(
                interface=interface)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Any(): {
        #     'oper_status': str,
        #     Optional('line_protocol'): str,
        
        oper_status = out[interface]["oper_status"]
        line_protocol = out[interface]["line_protocol"]
        enabled = out[interface]["enabled"]
        if oper_status == line_protocol == "up" and enabled == True:
            return True
        timeout.sleep()

    return False

