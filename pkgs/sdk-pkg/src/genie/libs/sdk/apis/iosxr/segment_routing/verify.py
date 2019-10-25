'''Common verify functions for Segment routing'''
# Python
import logging

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.utils.timeout import Timeout
from pyats.utils.objects import find, R
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def verify_segment_routing_operation(device, loopback_interface, label_min,
    prefix_sid_index, max_time=60, check_interval=20):
    ''' Verify Segment routing operation

        Args:
            device (`obj`): Device object
            loopback_interface (`str`): Loopback interface
            label_min (`int`): Segment routing global block start
            prefix_sid_index (`int`): Prefix-sid index
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        result = True

        try:
            out = device.parse('show isis segment-routing label table')
        except SchemaEmptyParserError:
            log.info("Device output is empty.")
            result = False
            timeout.sleep()
            continue

        reqs = R(['instance', '(?P<segment_routing>.*)',
                   'label', '(?P<label>.*)',
                   'prefix_interface', '(?P<prefix_interface>.*)'])

        found = find([out], reqs, filter_=False, all_keys=True)

        if found:
            for item in found:
                if item[0] == loopback_interface:
                    if item[1][3] == label_min+prefix_sid_index:
                        result = True
        else:
            log.error("Could not find any mpls route")
            result = False

        if result is True:
            return result

        timeout.sleep()

    return result

def verify_segment_routing_label_by_traceroute(device, traceroute_address,
    process_id):
    ''' Verify Segment routing label by traceroute

        Args:
            device (`obj`): Device object
            traceroute_address ('str): Traceroute address
            process_id ('str'): Router ISIS process ID
        Returns:
            result (`bool`): Verified result
    '''

    try:
        out = device.parse('show isis segment-routing label table')
    except SchemaEmptyParserError:
        log.info("Couldn't retrieve segment routing label details")
        return False

    traceroute_result = device.api.get_traceroute_parsed_output(
        device=device, addr=traceroute_address)
    if not traceroute_result:
        log.info("Couldn't retrieve traceroute result")
        return False

    for hop in traceroute_result['traceroute'][traceroute_address]['hops']:
        for next_hop in traceroute_result['traceroute'][traceroute_address]\
            ['hops'][hop]['paths']:
            if 'label_info' in traceroute_result['traceroute'][traceroute_address]\
                ['hops'][hop]['paths'][next_hop]:
                traceroute_label = traceroute_result['traceroute'][traceroute_address]\
                    ['hops'][hop]['paths'][next_hop]['label_info']['MPLS']['label']
        for label in out['instance'][process_id]['label']:
            if label == int(traceroute_label):
                log.info("Verified segment routing label")
                return True

    return False
