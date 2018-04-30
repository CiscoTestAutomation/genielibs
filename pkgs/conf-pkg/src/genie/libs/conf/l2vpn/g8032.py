
__all__ = (
        'G8032Ring',
        )

from genie.conf.base import DeviceFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesInheriter


class G8032Ring(DeviceFeature):

    # iosxr: l2vpn / ethernet ring g8032 someword (config-l2vpn)
    # iosxr: l2vpn / ethernet ring g8032 someword / exclusion-list vlan-ids 100-200,300
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 (config-l2vpn)
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel (config-l2vpn)
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / level <0-7>
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / port0 interface Bundle-Ether1
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / port1 bridge-domain someword2
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / port1 interface Bundle-Ether1
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / port1 none
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / aps-channel / port1 xconnect someword2
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / description someword2
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / inclusion-list vlan-ids someword2
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / profile someword2
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port0 neighbor
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port0 next-neighbor
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port0 owner
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port1 neighbor
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port1 next-neighbor
    # iosxr: l2vpn / ethernet ring g8032 someword / instance 1 / rpl port1 owner
    # iosxr: l2vpn / ethernet ring g8032 someword / open-ring
    # iosxr: l2vpn / ethernet ring g8032 someword / port0 interface Bundle-Ether1 (config-l2vpn)
    # iosxr: l2vpn / ethernet ring g8032 someword / port0 interface Bundle-Ether1 / monitor interface Bundle-Ether1
    # iosxr: l2vpn / ethernet ring g8032 someword / port1 interface Bundle-Ether1 (config-l2vpn)
    # iosxr: l2vpn / ethernet ring g8032 someword / port1 interface Bundle-Ether1 / monitor interface Bundle-Ether1
    # iosxr: l2vpn / ethernet ring g8032 someword / port1 none
    # iosxr: l2vpn / ethernet ring g8032 someword / port1 virtual

    def __init__(self):
        raise NotImplementedError

