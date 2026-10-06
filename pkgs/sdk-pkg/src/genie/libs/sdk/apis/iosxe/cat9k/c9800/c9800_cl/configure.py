from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_ip as _configure_management_ip,
)


def configure_management_ip(device,
                            address=None,
                            interface=None,
                            vrf=None,
                            no_switchport=True,
                            dhcp_timeout=30,
                            fallback_to_management_vrf=True):
    """Configure the management IP on a C9800-CL submodel device.

    Args:
        device ('obj'): Device object.
        address ('dict'): IPv4 and/or IPv6 addresses to configure.
        interface ('str'): Management interface.
        vrf ('str'): Interface VRF.
        no_switchport ('bool'): Configure ``no switchport``; defaults to True.
        dhcp_timeout ('int'): DHCP timeout in seconds; defaults to 30.
        fallback_to_management_vrf ('bool'): Use the VRF from the device
            management configuration when ``vrf`` is not provided. Defaults
            to True.
    """
    _configure_management_ip(
        device=device,
        address=address,
        interface=interface,
        vrf=vrf,
        no_switchport=no_switchport,
        dhcp_timeout=dhcp_timeout,
        fallback_to_management_vrf=fallback_to_management_vrf,
    )
