"""Common configure functions for prefix-list"""

# Python
import logging

# Common
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_summary
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_netmask

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_prefix_list_prefix_list(device, prefix_list):
    """ Configures prefix-list on device

        Args:
            device('obj'): device to configure on
            prefix_list('list'): prefix list which contains dictionary
                dictionary contains following 3 keys:
                    prefix_list ('str'): prefix list value
                    seq ('int'): sequence number
                    route ('str'): IP address
                ex.)
                   [ {
                        'prefix_list': 1,
                        'seq': 5,
                        'route': '172.16.0.0/24'
                    },
                    {
                        'prefix_list': 2,
                        'seq': 5,
                        'route': '172.16.1.0/24'
                    },
                    {
                        'direction': 'in',
                        'permit': 'deny',
                        'route': '10.94.12.1',
                        'comparison_operator': '<',
                        'comparison_value': 36
                    } 
                    ]

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not isinstance(prefix_list, list):
        raise SubCommandFailure("prefix_list must be a list")

    config = []

    for pf in prefix_list:
        if "prefix_list" in pf:
            config.append(
                "\nip prefix-list {prefix_list}".format(
                    prefix_list=pf["prefix_list"]
                )
            )

            if "seq" in pf:
                config.append(" seq {seq}".format(seq=pf["seq"]))

        if "direction" in pf:
            config.append(
                "\nip prefix-list {direction}".format(
                    direction=pf["direction"]
                )
            )

        if not "/" in pf["route"]:
            pf["route"] += get_interface_netmask(pf["route"])

        config.append(
            " {permit} {route}".format(permit=pf["permit"], route=pf["route"])
        )

        if "comparison_operator" in pf and "comparison_value" in pf:
            config.append(
                " {comparison_operator} {comparison_value}".format(
                    comparison_operator=pf["comparison_operator"],
                    comparison_value=pf["comparison_value"],
                )
            )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring prefix-list "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e
