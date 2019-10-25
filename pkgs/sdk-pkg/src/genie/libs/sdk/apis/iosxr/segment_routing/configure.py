"""Common configure functions for Segment Routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_segment_routing_gb_range(device, label_min, label_max):
    """ Add segment routing

        Args:
            device ('obj'): Device object
            label_min (`int`): Segment routing global block start
            label_max (`int`): Segment routing global block end

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "segment-routing\n"
            " global-block {label_min} {label_max}\n"
            "!\n".format(
                label_min=label_min,
                label_max=label_max,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not add segment routing")

def configure_segment_routing_sr_prefer(device, process_id, address_family):
    """ Configure segment routing sr prefer

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            address_family ('str'): Address family to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " address-family {address_family}\n"
            "  segment-routing mpls sr-prefer\n"
            " !\n".format(
                process_id=process_id,
                address_family=address_family,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure segment routing")

def configure_segment_routing_prefix_sid_index(device, process_id, interface,
    prefix_sid_index, address_family):
    """ Configure segment routing prefix-sid index

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface (`str`): Interface to configure
            prefix_sid_index (`int`): Prefix-sid index
            address_family ('str'): Address family to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  address-family {address_family}\n"
            "   prefix-sid index {prefix_sid_index}\n"
            "  !\n"
            " !\n".format(
                process_id=process_id,
                interface=interface,
                prefix_sid_index=prefix_sid_index,
                address_family=address_family,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure segment routing")
