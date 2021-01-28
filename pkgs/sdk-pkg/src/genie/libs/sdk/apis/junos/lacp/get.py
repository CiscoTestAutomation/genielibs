"""Common get info functions for LACP"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_lacp_stats(device, interface, link, stat_names):
    """Get LACP traffic stats of given interface via 'show lacp statistics {interface}'
        Args:
            device (`obj`): Device object
            interface (`str`): Lag interface name
            link (`str`): link name of Lag interface
            stat_names (`list`): list of link stat names

        Returns:
            list of stat values

        Raises:
            None
    """
    try:
        parsed_output = device.parse(
            'show lacp statistics interfaces {interface}'.format(
                interface=interface))
    except SchemaEmptyParserError as e:
        return None

    # example of parsed_output
    # {
    #   "lacp-interface-statistics-list": {
    #     "lacp-interface-statistics": {
    #       (snip)
    #       "lag-lacp-statistics": [
    #         {
    #           "name": "ge-0/0/0",
    #           "lacp-rx-packets": "582",
    #           "lacp-tx-packets": "567",
    #           "unknown-rx-packets": "0",
    #           "illegal-rx-packets": "0"
    #         },
    #         {
    #           "name": "ge-0/0/6",
    #           "lacp-rx-packets": "590",
    #           "lacp-tx-packets": "574",
    #           "unknown-rx-packets": "0",
    #           "illegal-rx-packets": "0"
    #         }
    #       ]
    #     }
    #   }
    # }

    lag_lacp_stats = parsed_output.q.get_values('lag-lacp-statistics')

    result = []
    for lacp_stat in lag_lacp_stats:
        if link == lacp_stat['name']:
            for stat in stat_names:
                if stat in lacp_stat:
                    result.append(int(lacp_stat[stat]))
                else:
                    log.warn(
                        "stat_name {stat} is not correct. lag-lacp-statistics: {lag_lacp_stats"
                        .format(stat=stat, lag_lacp_stats=lag_lacp_stats))
                    result.append(None)

            return result

    log.warn(
        "Interface {interface} couldn't be found. lag-lacp-statistics: {lag_lacp_stats}"
        .format(interface=interface, lag_lacp_stats=lag_lacp_stats))
    return result