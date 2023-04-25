"""Common configure functions for nve"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def unconfig_nve_src_intf(device, nve_intf):
    """Unconfig the source interface on the nve interface
        Args:
            device ('obj'): Device object
            nve_intf ('str'): NVE Interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring the source interface on interface {nve_if}".format(
            nve_if=nve_intf
        )
    )

    try:
        device.configure(
            [
                "interface {interface}".format(interface=nve_intf),
                "no source-interface",
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig the source interface on interface {interface}. "
            "Error:\n{error}".format(
                interface=nve_intf, error=e
            )
        )


def unconfig_nve_vni_members(device, nve_intf, vni_cfg):
    """Unconfig VNI member(s) on the nve interface
        Args:
            device ('obj'): Device object
            nve_intf ('str'): NVE Interface
            vni_cfg ('dict'): VNI(s) to unconfigure
                vni_id ('str'): VNI id
                    is_ingress_rep (Optional, 'bool'): Is this an IR VNI
                    mcast_group (Optional, 'str'): multicast group address
                    vrf_name (Optional, 'str'): name of the L3VNI vrf
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring a VNI member on the interface {nve_if}".format(
            nve_if=nve_intf
        )
    )

    cfg = ["interface {interface}".format(interface=nve_intf)]

    for vni, vni_attr in vni_cfg.items():
        if 'vrf_name' in vni_attr:
            cfg += [f"no member vni {vni} vrf {vni_attr['vrf_name']}"]
        elif 'mcast_group' in vni_attr:
            cfg += [f"no member vni {vni} mcast-group {vni_attr['mcast_group']}"]
        elif 'is_ingress_rep' in vni_attr and vni_attr['is_ingress_rep']:
            cfg += [f"no member vni {vni} ingress-replication"]
        else:
            cfg += [f"no member vni {vni}"]

    try:
        device.configure(cfg)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfig the VNI member on interface {interface}. "
            "Error:\n{error}".format(
                interface=nve_intf, error=e
            )
        )
