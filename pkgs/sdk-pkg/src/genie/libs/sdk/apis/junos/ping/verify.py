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
                wait=None,
                mpls_rsvp=None,
                loss_rate=0,
                count=None,
                source=None,
                max_time=30,
                check_interval=10):
    """ Verify ping loss rate on ip address provided

        Args:
            device ('obj'): Device object
            address ('str'): Address value
            ttl ('int'): ttl value passed in command
            wait ('int'): wait value passed in command
            mpls_rsvp ('str'): MPLS RSVP value
            loss_rate ('int'): Expected loss rate value
            count ('int'): Count value for ping command
            source ('str'): Source IP address, default: None
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            Boolean
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        if address and count and source:
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

        if loss_rate_found == loss_rate:
            return True
        timeout.sleep()
    return False
