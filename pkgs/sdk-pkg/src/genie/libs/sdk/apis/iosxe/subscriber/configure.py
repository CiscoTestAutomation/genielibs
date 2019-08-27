"""Common configure functions for subscriber"""
# Python
import os
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def remove_subscriber(
    device, bgp_as, bridge_id, bridge_interface, vpn_id, vpn_interface
):
    """ Remove subscriber

        Args:
            device ('obj'): Device object
            bgp_as ('str'): BGP AS
            bridge_id ('str'): Bridge Id
            bridge_interface ('str'): Bridge interface
            vpn_id ('str'): VPN id
            vpn_interface ('str'): VPN interface
        Returns:
            None
        Raise:
            SubCommandFailure
    """

    config_cmd = (
        "interface {bridge_interface}\n"
        "no service instance {bridge_id} ethernet\n"
        "bridge-domain {bridge_id}\n"
        "no member vfi VPLS-{bridge_id}\n"
        "no bridge-domain {bridge_id}\n"
        "no l2vpn vfi context VPLS-{bridge_id}\n"
        "no vrf definition L3VPN-{vpn_id}\n"
        "no interface {vpn_interface}.{vpn_id}\n"
        "router bgp {as_n}\n"
        "no address-family ipv4 vrf L3VPN-{vpn_id}".format(
            bridge_interface=bridge_interface,
            bridge_id=bridge_id,
            vpn_id=vpn_id,
            vpn_interface=vpn_interface,
            as_n=bgp_as,
        )
    )

    try:
        out = device.configure(config_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in unconfiguring subscriber "
            "on interface {bridge_interface} "
            "with bridge id {bridge_id} "
            "on device {device}, "
            "Error: {e}".format(
                bridge_interface=bridge_interface,
                bridge_id=bridge_id,
                device=device.name,
                e=str(e),
            )
        ) from e
