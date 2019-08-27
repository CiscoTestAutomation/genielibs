"""Common configure functions for community-list"""

# Python
import logging

# Common
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_summary

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_community_list_community_list_permit(device, community_list):

    """ Configure community list permit

        Args:
            device ('obj'): Device object
            community_list('list'): community list which contains dictionary
                dictionary contains following 3 keys:
                    seq ('int'): sequence number
                    permit ('str'): permit value
                    community ('str'): community value - Optional
                ex.)
                    [ 
                        {
                            'seq': 1,
                            'permit': 'deny',
                            'community': 62000:1
                        },
                        {   
                            'seq': 1,
                            'permit': 'permit'
                        },
                        {
                            'seq': 2,
                            'permit': 'deny',
                            'community': '62000:2'
                        },
                        {
                            'seq': 2,
                            'permit': 'permit'
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    # ip community-list 1 deny 62000:1
    # ip community-list 1 permit
    # ip community-list 2 deny 62000:2
    # ip community-list 2 permit

    config = []
    for comm in community_list:
        x = comm["seq"]
        community_permit = comm["permit"]
        community = "" if "community" not in comm else comm["community"]
        config.append(
            "ip community-list {x} {community_permit} {community}\n".format(
                x=x, community_permit=community_permit, community=community
            )
        )
    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring community-list "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e
