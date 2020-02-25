"""Common verify functions for NTP"""

# Python
import re
import logging
import time
from datetime import datetime
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Genie
from pyats.async_ import pcall
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_smallest_stratum_ntp_system_peer(device, max_time=90, check_interval=15):
    """ Verify NTP server with the smallest stratum is elected as system peer

        Args:
            device (`obj`): Device object
            max_time (int): Maximum wait time for the trigger,
                            in seconds. Default: 90
            check_interval (int): Wait time between iterations when looping is needed,
                            in seconds. Default: 15
        Returns:
            result (`bool`): Verified result
            sys_peer (`str`): System peer ip
            other_peers (`list`): Other peers ip
    """
    result = ""
    sys_peer = ""
    other_peers = []

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.parse("show ntp associations")
        stratum = (
            out.get("clock_state", {}).get("system_status", {}).get("clock_stratum")
        )
        sys_peer = (
            out.get("clock_state", {})
            .get("system_status", {})
            .get("associations_address")
        )

        for peer, data in out["peer"].items():
            if peer != sys_peer:
                other_peers.append(peer)

            peer_stratum = data["local_mode"]["client"]["stratum"]
            if stratum > peer_stratum:
                log.info(
                    "Found peer {peer} has a smaller stratum {stratum}".format(
                        peer=peer, stratum=peer_stratum
                    )
                )
                result = False
                break
        else:
            result = True

        if not result:
            timeout.sleep()
        else:
            break

    return result, sys_peer, other_peers


def is_ntp_clock_synchronized(
    device, ip_address_peer, max_time=60, check_interval=5, check_leap=False
):
    """ Verify that clock is synchronized to given peer

        Args:
            device (`obj`): Device object
            ip_address_peer (`str`): peer ip address
            max_time (int): Maximum wait time for the trigger,
                            in seconds. Default: 60
            check_interval (int): Wait time between iterations when looping is needed,
                            in seconds. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show ntp status")
            if out["clock_state"]["system_status"]["status"] == "synchronized":
                if check_leap:
                    if out["clock_state"]["system_status"]["leapsecond"] == True:
                        return True
                elif out["clock_state"]["system_status"]["refid"] == ip_address_peer:
                    return True
        except Exception:
            pass
        timeout.sleep()
    return False


def verify_ntp_time_changed(device, search_time):
    """ Verify that time has changed on clock

        Args:
            device (`obj`): Device object
            search_time (`str`): time to search
                ex ) search_time = '23:59:55'
        Returns:
            result (`bool`): Verified result
    """
    while True:
        try:
            out = device.parse("show clock")
            if search_time in out["time"]:
                return True
        except SchemaEmptyParserError as e:
            log.error("Parser did not return output for " "command 'show clock'")
            return False
        except KeyError as ke:
            log.error("Key {} not found in parser for " "'show clock'".format("time"))
            return False
    return False


def verify_ntp_leap_second(device, time_list):
    """ Verify that leap second happened
        Args:
            device (`obj`): Device object
            time_list (`obj`): timedelta object
        Returns:
            result (`bool`): Verified result
    """
    while True:
        now = datetime.now()
        if now >= time_list:
            try:
                output = device.parse("show clock")
                return output
            except SchemaEmptyParserError as e:
                log.error("Parser did not return output for " "command 'show clock'")
                return None
    return None


def verify_ntp_time(device, target, max_time=90, check_interval=15):
    """ Verify ntp clock is same on two devices

        Args:
            device (`obj`): Device object
            target (`obj`): Device object
            max_time (int): Maximum wait time for the trigger,
                            in seconds. Default: 90
            check_interval (int): Wait time between iterations when looping is needed,
                            in seconds. Default: 15
        Returns:
            result (`bool`): Verified result
    """

    def clock(dev):
        return dev.parse("show clock")

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        t1, t2 = pcall(clock, dev=[device, target])
        log.info(
            "Device: {device} Clock: {t1}\n"
            "Device: {target} Clock: {t2}".format(
                device=device.name, target=target.name, t1=t1, t2=t2
            )
        )

        p = re.compile(r"\d+:\d+:\d+")
        for key in t1:
            if "time" == key:
                result = p.findall(t1[key]) == p.findall(t2[key])
            else:
                result = t1[key] == t2[key]
            if not result:
                break
        else:
            return True

        timeout.sleep()

    return False


def verify_ntp_association_with_server(
    device, ip_address_server, peer_mode, max_stratum, max_time=15, check_interval=5
):
    """Verify association with server

        Args:
            server (`obj`): Server Device object
            ip_address_server (`str`): IP address to server
            peer_mode (`str`): peer mode type
            max_stratum (`int`): maximum stratum value
            max_time (int): Maximum wait time for the trigger,
                            in seconds. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in seconds. Default: 5
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        result = False
        try:
            out = device.parse("show ntp associations detail")
        except SchemaEmptyParserError as e:
            log.error("Parser not found for command " "'show ntp associations detail'")
            return False
        for vrf in out["vrf"].keys():
            try:
                allowed_ip_dict = out["vrf"][vrf]["associations"]["address"][
                    ip_address_server
                ]["local_mode"]["client"]["isconfigured"]["True"]
                stratum_found = allowed_ip_dict["stratum"]
                refid = allowed_ip_dict["refid"]
                peer_mode_found = allowed_ip_dict["peer"][refid]["local_mode"][
                    peer_mode
                ]["local_mode"]
            except KeyError as e:
                log.error(
                    "Could not find following key{}, exception {}".format(
                        peer_mode, str(e)
                    )
                )
                result = False

            if stratum_found < max_stratum and peer_mode_found == peer_mode:
                result = True
            else:
                result = False
        if result:
            return result
        timeout.sleep()

    return result


def verify_synced_ntp_server(device, ip_address, max_time=1200,
        check_interval=30):
    """ Verify synched NTP server

        Args:
            device (`obj`): Device object
            ip_address (`list`): list of Server peer IP address
            max_time (int): Maximum wait time for the trigger,
                            in seconds. Default: 1200
            check_interval (int): Wait time between iterations when looping is needed,
                            in seconds. Default: 30
        Returns:
            peer_dict (`dict`): Peer dictionary
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ntp associations")
        except SchemaEmptyParserError:
            log.error('No NTP server found')
            return False
        for ip in ip_address:
            try:
                if (
                    out.get("peer").get(ip).get("local_mode").get("client").get("mode")
                    == "synchronized"
                ):
                    log.info("IP {} is synchronized".format(ip))
                    # will sync with only one NTP server. so, check only one
                    return True
                else:
                    log.warning("IP {} is not yet synchronized".format(ip))
            except Exception as e:
                log.error("{}".format(e))
        timeout.sleep()

    return False


def verify_no_ntp_association_configuration(device):
    """ Verify no NTP association configuration on the device

        Args:
            device (`obj`): Device object
        Returns:
            peer_dict (`dict`): Peer dictionary
    """

    try:
        out = device.parse("show ntp associations")
        return out.get("peer", None)
    except SchemaEmptyParserError as e:
        log.info("Verified no NTP association configuration found on the device")
    return None
