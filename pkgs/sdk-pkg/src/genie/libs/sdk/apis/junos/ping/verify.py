"""Common verification functions for ping"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_ping(device,
                address=None,
                ttl=None,
                tos=None,
                size=None,
                wait=None,
                mpls_rsvp=None,
                loss_rate=0,
                ping_size=None,
                count=None,
                interface=None,
                source=None,
                rapid=False,
                do_not_fragment=False,
                max_time=30,
                check_interval=10):
    """ Verify ping loss rate on ip address provided

        Args:
            device ('obj'): Device object
            address ('str'): Address value
            size {'str'}: Size value for ping command
            tos {'str'}: tos value for ping command
            ping_size {'str'}: data bytes expected
            ttl ('int'): ttl value passed in command
            wait ('int'): wait value passed in command
            mpls_rsvp ('str'): MPLS RSVP value
            loss_rate ('int'): Expected loss rate value
            count ('int'): Count value for ping command
            interface ('str'): source interface
            source ('str'): Source IP address, default: None
            rapid ('bool'): Appears in command or not, default: False
            do_not_fragment ('bool'): Appears in command or not, default: False
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            Boolean
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    if address or mpls_rsvp:
        cmd = ['ping {address}'.format(address=address)]
        if source:
            cmd.append('source {source}'.format(source=source))
        if size:
            cmd.append('size {size}'.format(size=size))
        if count:
            cmd.append('count {count}'.format(count=count))
        if interface:
            cmd.append('interface {interface}'.format(interface=interface))
        if tos:
            cmd.append('tos {tos}'.format(tos=tos))
        if ttl:
            cmd.append('ttl {ttl}'.format(ttl=ttl))
        if wait:
            cmd.append('wait {wait}'.format(wait=wait))
        if rapid:
            cmd.append('rapid')
        if do_not_fragment:
            cmd.append('do-not-fragment')
        if not address:
            cmd = ['ping mpls rsvp {rsvp}'.format(rsvp=mpls_rsvp)]
    else:
        log.info('Need to pass address or mpls_rsvp as argument')
        return False

    cmd = ' '.join(cmd)

    while timeout.iterate():
        try:
            # junos ping command can accept various paramegers order like below
            # ping 192.168.1.1 count 1 size 1514
            # ping 192.168.1.1 size 1514 count 1
            # so, store ping output as string and call parser with just `ping {addrss}`
            # with passing the ping output
            output = device.execute(cmd)
            out = device.parse('ping {address}'.format(address=address), output=output)
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        # Example dictionary structure:
        #     {
        #         "ping": {
        #             "address": "10.189.5.94",
        #             "data-bytes": 56,
        #             "result": [
        #                 {
        #                     "bytes": 64,
        #                     "from": "10.189.5.94",
        #                     "icmp-seq": 0,
        #                     "time": "2.261",
        #                     "ttl": 62
        #                 },
        #             ],
        #             "source": "10.189.5.94",
        #             "statistics": {
        #                 "loss-rate": 0,
        #                 "received": 1,
        #                 "round-trip": {
        #                     "avg": "2.175",
        #                     "max": "2.399",
        #                     "min": "1.823",
        #                     "stddev": "0.191"
        #                 },
        #                 "send": 1
        #             }
        #         }
        #     }
        loss_rate_found = Dq(out).get_values("loss-rate", 0)


        if (
            size
            and loss_rate_found == loss_rate
            and Dq(out).get_values("data-bytes", 0) == int(size)
        ):
            return True
        if loss_rate_found == loss_rate:
            return True
        timeout.sleep()
    return False

def verify_ping_packet_transmission(device,
                address,
                count,
                expected_transmitted_rate,
                max_time=30,
                check_interval=10):
    """ Verify ping loss rate on ip address provided

        Args:
            device ('obj'): Device object
            address ('str'): Address
            count ('int'): Count value for ping command
            expected_transmitted_rate ('int'): Expected transmitted rate
            max_time (`int`, Optional): Max time, default: 30 seconds
            check_interval (`int`, Optional): Check interval, default: 10 seconds
        Returns:
            Boolean
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'ping {address} count {count}'.format(address=address,
                                                        count=int(count))

            out = device.parse(cmd)
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        # Example dictionary structure:
        #     {
        #         "ping": {
        #             "address": "10.189.5.94",
        #             "statistics": {
        #                 "received": 1,
        #                 "send": 1

        number_of_transmitted_packets = Dq(out).get_values("send", 0)
        try:
            transmitted_rate = int((number_of_transmitted_packets * 100)/count)
        except:
            transmitted_rate = 0

        if transmitted_rate == int(expected_transmitted_rate):
            return True

        timeout.sleep()
    return False


def verify_ping_one_iterations(device,
                               address=None,
                               ttl=None,
                               tos=None,
                               size=None,
                               wait=None,
                               mpls_rsvp=None,
                               loss_rate=0,
                               ping_size=None,
                               count=None,
                               source=None):
    """ Verify ping loss rate on ip address provided

        Args:
            device ('obj'): Device object
            address ('str'): Address value
            size {'str'}: Size value for ping command
            tos {'str'}: tos value for ping command
            ping_size {'str'}: data bytes expected
            ttl ('int'): ttl value passed in command
            wait ('int'): wait value passed in command
            mpls_rsvp ('str'): MPLS RSVP value
            loss_rate ('int'): Expected loss rate value
            count ('int'): Count value for ping command
            source ('str'): Source IP address, default: None
        Returns:
            Boolean
        Raises:
            None
    """
    if tos:
        cmd = 'ping {address} source {source} size {size} count {count} tos {tos} rapid'.format(
                address=address,
                source=source,
                size=size,
                count=count,
                tos=tos
            )
    elif address and count and source:
        cmd = 'ping {address} source {source} count {count}'.format(
                address=address,
                source=source,
                count=count)
    elif address and count and not ttl and not wait:
        cmd = 'ping {address} count {count}'.format(address=address,
                                                    count=count)
    elif address and count and ttl and wait:
        cmd = 'ping {address} ttl {ttl} count {count} wait {wait}'.format(
                address=address,
                ttl=ttl,
                count=count,
                wait=wait)
    elif not address and mpls_rsvp:
        cmd = 'ping mpls rsvp {rsvp}'.format(rsvp=mpls_rsvp)
    elif address:
        cmd = 'ping {address}'.format(address=address)
    else:
        log.info('Need to pass address as argument')
        return False
    try:
        out = device.parse(cmd)
    except SchemaEmptyParserError as e:
        return False
    # Example dictionary structure:
    #     {
    #         "ping": {
    #             "address": "10.189.5.94",
    #             "data-bytes": 56,
    #             "result": [
    #                 {
    #                     "bytes": 64,
    #                     "from": "10.189.5.94",
    #                     "icmp-seq": 0,
    #                     "time": "2.261",
    #                     "ttl": 62
    #                 },
    #             ],
    #             "source": "10.189.5.94",
    #             "statistics": {
    #                 "loss-rate": 0,
    #                 "received": 1,
    #                 "round-trip": {
    #                     "avg": "2.175",
    #                     "max": "2.399",
    #                     "min": "1.823",
    #                     "stddev": "0.191"
    #                 },
    #                 "send": 1
    #             }
    #         }
    #     }
    loss_rate_found = Dq(out).get_values("loss-rate", 0)
    

    if size:
        if loss_rate_found == loss_rate and Dq(out).get_values("data-bytes", 0) == int(size):
            return True
    if loss_rate_found == loss_rate:
        return True
    return False