# PYthon
import logging

# pyATS
from pyats.utils.objects import find, R

# Unicon
from unicon.core.errors import SubCommandFailure

# iosxe traceroute
from genie.utils.timeout import Timeout
from genie.libs.parser.iosxe.traceroute import Traceroute

log = logging.getLogger(__name__)


def verify_traceroute_first_hop_address(
    device, prefix, expected_first_hop_address
):
    """ Verify if first hop ip address is expected one
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            expected_hop_address ('str'): Expected next hop ip address
        Returns:
            True/False
        Raises:
            None
    """

    parsed_output = device.api.get_traceroute_parsed_output(
        device=device, addr=prefix
    )
    if not parsed_output:
        return False

    # Since we are checking first hop, '1' is hard coded
    first_hop = (
        parsed_output["traceroute"]
        .get(prefix, {})
        .get("hops", {})
        .get("1", {})
        .get("paths", {})
        .get(1, {})
        .get("address", None)
    )

    if not first_hop:
        return False
    elif expected_first_hop_address == first_hop:
        log.info('First hop address is {address} as expected'.format(address=expected_first_hop_address))
        return True
    else:
        log.info(
            "First hop address {address} is not as expected".format(
                address=first_hop
            )
        )
        return False


def verify_traceroute(device, addr, vrf=None, proto=None, ingress=None, source=None,
                      dscp=None, numeric=None, timeout=None, probe=None,
                      minimum_ttl=None, maximum_ttl=None, port=None, style=None,
                      expected_output_label_list=None, expected_hop_list=None,
                      ignore_last_label=False, ignore_first_label=False,
                      check_first_hop=True, max_time=60, check_interval=30):
    """ Verify traceroute if it matches expected_output_label_list or expected_hop_list
        Args:
            device ('obj'): Device object
            vrf ('str'): vrf name
            addr ('str'): Destination address
            proto ('str'): Protocol(ip/ipv6)
            ingress ('str'): Ingress traceroute
            source ('str'): Source address or interface
            dscp ('int'): DSCP Value
            numeric ('str'): Numeric display
            timeout ('int'): Timeout in seconds
            probe ('int'): Probe count
            minimum_ttl ('int'): Minimum Time to Live
            maximum_ttl ('int'): Maximum Time to Live
            port ('int'): Port Number
            ignore_last_label ('bool'): Ignore last label in expected_output_label_list,
            ignore_first_label ('bool'): Ignore first label in expected_output_label_list
            expected_output_label_list ('list'): Expected output label list of first hop
                ex.) 
                    expected_output_label_list = ['16052','16062','16063','39']
            expected_hop_list ('list'): Expected hop list
                ex.) 
                    expected_hop_list = ['10.19.198.29', '10.169.14.129', '10.169.14.34', '192.168.1.1']
            check_first_hop ('bool'): flag to check all labels only from first hop's labels. 
                                      if False, all top label from each hop will be checked.
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How long to wait between checks
        Returns:
            True/False
        Raises:
            None
    """

    def verify_func(device, addr=None, vrf=None, proto=None, ingress=None, source=None,
                    dscp=None, numeric=None, timeout=None, probe=None,
                    minimum_ttl=None, maximum_ttl=None, port=None, style=None,
                    expected_output_label_list=None, expected_hop_list=None,
                    ignore_last_label=False, ignore_first_label=False,
                    check_first_hop=True):
        if not (expected_output_label_list or expected_hop_list):
            log.error('expected_output_label_list or expected_hop_list is not provided.')
            return False
        parsed_output = device.api.get_traceroute_parsed_output(
            device=device, 
            addr=addr,
            vrf=vrf,
            proto=proto,
            ingress=ingress,
            source=source,
            dscp=dscp,
            numeric=numeric,
            timeout=timeout,
            probe=probe,
            minimum_ttl=minimum_ttl,
            maximum_ttl=maximum_ttl,
            port=port,
            style=style
        )

        if not parsed_output:
            return False

        if expected_output_label_list:
            hops = parsed_output["traceroute"].get(addr, {}).get("hops", {})
            if ignore_first_label:
                expected_output_label_list.pop(0)

            for i in range(1, len(hops.keys())+1):
                hop_labels = (hops
                    .get(str(i), {})
                    .get("paths", {})
                    .get(1, {})
                    .get("label_info", {})
                    .get("MPLS", {})
                    .get("label", None)
                )

                if not hop_labels:
                    if check_first_hop:
                        return False
                    else:
                        expected_output_label_list.pop(0)
                        continue

                hop_label_list = hop_labels.split('/')
                if ignore_last_label:
                    hop_label_list.pop()

                if hop_label_list != expected_output_label_list:
                    return False
                else:
                    break
        
        if expected_hop_list:
            for address in expected_hop_list:
                reqs = R(
                    [
                        'traceroute',
                        addr,
                        'hops',
                        '(.*)',
                        'paths',
                        '(.*)',
                        'address',
                        address
                    ]
                )
                found = find([parsed_output], reqs, filter_=False, all_keys=True)
            
                if not found:
                    return False

        return True

    iteration = Timeout(max_time, check_interval)
    while iteration.iterate():
        result = verify_func(device=device, addr=addr, vrf=vrf, proto=proto, ingress=ingress, source=source,
                    dscp=dscp, numeric=numeric, timeout=timeout, probe=probe,
                    minimum_ttl=minimum_ttl, maximum_ttl=maximum_ttl, port=port, style=style,
                    expected_output_label_list=expected_output_label_list, expected_hop_list=expected_hop_list,
                    ignore_last_label=ignore_last_label, ignore_first_label=ignore_first_label,
                    check_first_hop=check_first_hop)
        if result:
            return True

        iteration.sleep()

    return False
