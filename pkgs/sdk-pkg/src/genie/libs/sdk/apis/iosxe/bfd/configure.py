"""Common configure functions for bfd"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_bfd_on_interface(
    device, interface, interval, min_rx, multiplier
):
    """ Configures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            interval ('str'): interval
            min_rx ('str'): min_rx
            multiplier ('str'): multiplier
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.info(
        "Configuring bfd with interval={}, min_rx={}, multiplier={}, on "
        "interface {}".format(interval, min_rx, multiplier, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "bfd interval {} min_rx {} multiplier {}".format(
                    interval, min_rx, multiplier
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd on interface {interface}".format(
                interface=interface
            )
        )


def enable_bfd_on_ospf(device, interface):
    """ Enabled bfd on ospf protocol on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on ospf protocol
    """
    log.info("Enabling bfd on ospf protocol")
    try:
        device.configure(["interface {}".format(interface), "ip ospf bfd"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable bfd on ospf protocol on interface {interface}".format(
                interface=interface
            )
        )


def disable_bfd_on_ospf(device, interface):
    """ Disables bfd on ospf protocol

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling bfd on ospf protocol
    """
    log.info("Disabling bfd on ospf protocol")
    try:
        device.configure(["interface {}".format(interface), "no ip ospf bfd"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable bfd on ospf protocol on interface {interface}".format(
                interface=interface
            )
        )


def enable_bfd_static_route(device, interface, ip_address):
    """ Enables bfd static route on device

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
            ip_address ('str'): ip address of destination
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling bfd static rout on device
    """
    log.info(
        "Enabling bfd static route on {} to {}".format(interface, ip_address)
    )
    try:
        device.configure(
            ["ip route static bfd {} {}".format(interface, ip_address)]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd static route on interface {interface}".format(
                interface=interface
            )
        )

def unconfigure_bfd_on_interface(
    device, interface
):
    """ Unconfigures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.info(
        "Unconfiguring bfd on "
        "interface {}".format(interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no bfd interval"
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure bfd on interface {interface}".format(
                interface=interface
            )
        )

def configure_bfd_neighbor_on_interface(
    device, interface, address_family, neighbor_address
):
    """ Configures bfd neighbor on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            address_family ('str'): ipv4|ipv6 address family
            neighbor_address ('str'): neighbor address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.debug(
        "Configuring bfd with address_family={}, neighbor_address={} on "
        "interface {}".format(address_family, neighbor_address, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "bfd neighbor {} {} ".format(
                    address_family, neighbor_address
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure bfd neighbor on interface {interface}".format(
                interface=interface
            )
        )

def unconfigure_bfd_neighbor_on_interface(
    device, interface, address_family, neighbor_address
):
    """ Unconfigures bfd on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            address_family ('str'): ipv4|ipv6 address family
            neighbor_address ('str'): neighbor address
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """
    log.debug(
        "UnConfiguring bfd with address_family={}, neighbor_address={} on "
        "interface {}".format(address_family, neighbor_address, interface)
    )

    try:
        device.configure(
            [
                "interface {}".format(interface),
                "no bfd neighbor {} {} ".format(
                    address_family, neighbor_address
                ),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure bfd neighbor on interface {interface}".format(
                interface=interface
            )
        )

def unconfigure_bfd_value_on_interface(device, interface, value):
    """ Unconfigures bfd on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            bfd ('str'): bfd value to unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Unconfiguring bfd on "
        "interface {}".format(interface)
    )
    config = [
                "interface {}".format(interface),
                "no bfd {}".format(value)
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure bfd value on interface {interface}. Error:\n{e}"
        )

def enable_bfd_on_isis_ipv6_address(device, interface):
    """ Enabled bfd on isis ipv6 address on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on isis ipv6 address
    """
    log.info("Enabling bfd on isis ipv6 address")
    cmd = ["interface {}".format(interface), "isis ipv6 bfd"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
             f"Could not enable bfd on isis ipv6 address on interface {interface}. Error:\n{e}"
        )

def disable_bfd_on_isis_ipv6_address(device, interface):
    """ Disables bfd on isis ipv6 address
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure under
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling bfd on isis ipv6 address
    """
    log.info("Disabling bfd on isis ipv6 address")
    cmd = ["interface {}".format(interface), "no isis ipv6 bfd"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not disable bfd on isis ipv6 address on interface {interface}. Error:\n{e}"
        )

def enable_ospf_bfd_all_interfaces(device, process_id):
    """ Enable BFD on all interfaces for OSPF
        Args:
            device ('obj'): device to use
            process_id ('str'): OSPF process id
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling BFD on all interfaces for OSPF
    """
    log.debug("Enable BFD on all interfaces for OSPF")
    try:
        device.configure([
            f"router ospf {process_id}",
            "bfd all-interfaces"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable BFD on all interfaces for OSPF. Error:\n{e}"
        )

def set_isis_timers(
    device,
    isis_lsp_refresh_interval=None,
    isis_spf_interval=None,
    isis_spf_initial_wait=None,
    isis_spf_min_wait=None,
    prc_interval=None,
    prc_initial_wait=None,
    prc_min_wait=None,
    lsp_gen_interval=None,
    lsp_gen_initial_wait=None,
    lsp_gen_min_wait=None
):
    """ Configures various BFD features on the device
        Args:
            device ('obj'): device to use
            isis_lsp_refresh_interval ('int', optional): <1-65535>  LSP refresh time in seconds
            isis_spf_interval ('int', optional): <1-120>  Interval between consecutive SPFs in seconds
            isis_spf_initial_wait ('int', optional): Initial wait before first SPF in milliseconds
            isis_spf_min_wait ('int', optional): <1-120000>  Minimum wait between first and second SPF in milliseconds
            prc_interval ('int', optional): <1-120>  PRC interval in seconds
            prc_initial_wait ('int', optional): <1-120000>  Initial wait for PRC in milliseconds
            prc_min_wait ('int', optional): <1-120000>  Minimum wait between first and second PRC in milliseconds
            lsp_gen_interval ('int', optional): <1-120>  LSP Interval in seconds
            lsp_gen_initial_wait ('int', optional): <1-120000>  Initial wait in milliseconds
            lsp_gen_min_wait ('int', optional): <1-120000>  Wait between first and second lsp generation in milliseconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring isis timers
    """

    log.debug("configuring isis timers on the device")
    config = []
    if isis_lsp_refresh_interval and isis_spf_interval and isis_spf_initial_wait and isis_spf_min_wait:
        config.extend([
            f"router isis",
            f"lsp-refresh-interval {isis_lsp_refresh_interval}",
            f"spf-interval {isis_spf_interval} {isis_spf_initial_wait} {isis_spf_min_wait}"
        ])
    if prc_interval and prc_initial_wait and prc_min_wait:
        config.extend([
            f"prc-interval {prc_interval} {prc_initial_wait} {prc_min_wait}"
        ])
    if lsp_gen_interval and lsp_gen_initial_wait and lsp_gen_min_wait:
        config.extend([
            f"lsp-gen-interval {lsp_gen_interval} {lsp_gen_initial_wait} {lsp_gen_min_wait}"
        ])
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure BFD features on the device. Error:\n{e}"
        )

def configure_bfd_ospf_timers (
    device, 
    ospf_process_id=None, 
    ospf_lsa_delay=None, 
    ospf_lsa_min_delay=None, 
    ospf_lsa_max_delay=None, 
    ospf_spf_delay=None,
    spf_start=None,
    spf_hold=None,
):
    """ Configures various BFD features on the device
        Args:
            device ('obj'): device to use
            ospf_process_id ('int', optional): OSPF process ID
            ospf_lsa_delay ('int', optional): <0-600000>  Delay to generate first occurrence of LSA in milliseconds
            ospf_lsa_min_delay ('int', optional): <1-600000>  Minimum delay between originating the same LSA in milliseconds
            ospf_lsa_max_delay ('int', optional): <1-600000>  Maximum delay between originating the same LSA in milliseconds
            ospf_spf_delay ('int', optional): <1-600000>  Delay between receiving a change to SPF calculation in milliseconds
            spf_start ('int', optional): <1-600000>  Delay between first and second SPF calculation in milliseconds
            spf_hold ('int', optional): <1-600000>  Maximum wait time in milliseconds for SPF calculations
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring BFD features
    """
    
    log.info("configuring various BFD features on the device")
    config = []
    if ospf_process_id:
        config.append(f"router ospf {ospf_process_id}")
        if (ospf_lsa_delay and ospf_lsa_min_delay and ospf_lsa_max_delay):
            config.append(f"timers throttle lsa {ospf_lsa_delay} {ospf_lsa_min_delay} {ospf_lsa_max_delay}")
        if (ospf_spf_delay and spf_start and spf_hold):
            config.append(f"timers throttle spf {ospf_spf_delay} {spf_start} {spf_hold}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure BFD features on the device. Error:\n{e}"
        )

def configure_ospf_interface_cost(device, interface, cost):
    """ Configures ospf cost on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure ospf cost
            cost ('str'): cost value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring ospf cost on interface
    """
    log.info("configuring ospf cost on interface")
    cmd = ['interface {interface}'.format(interface=interface), 'ip ospf cost {cost}'.format(cost=cost)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ospf cost on interface {interface}. Error:\n{e}"
        )

def enable_eigrp_bfd_all_interfaces(device, eigrp_instance):
    """ Enables bfd on all interfaces for eigrp
        Args:
            device ('obj'): device to use
            eigrp_instance ('str'): EIGRP instance to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling bfd on all interfaces for eigrp
    """
    log.info(f"Enabling bfd on all interfaces for eigrp instance {eigrp_instance}")
    try:
        device.configure([
            f"router eigrp {eigrp_instance}",
            "bfd all-interfaces"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable bfd on all interfaces for eigrp instance {eigrp_instance}. Error:\n{e}"
        )

def rp_bfd_all_interfaces(device, routing_protocol, process_id=None, system_number=None):
    '''Enable BFD on all interfaces for routing protocol
    Args:
        device ('obj'): device to use
        routing_protocol ('str'): routing protocol name
        process_id ('int', optional): routing protocol process id
        system_number ('int', optional): routing protocol Autonomous system number
    '''
    log.debug("Enable BFD on all interfaces for routing protocol")
    
    config = []
    if routing_protocol == 'isis':
        config.extend([
            f"router {routing_protocol}",
            f"bfd all-interfaces"
        ])
    if routing_protocol == 'ospf' or 'ospfv3' and process_id:
        config.extend([
            f"router {routing_protocol} {process_id}",
            f"bfd all-interfaces"
        ])
    if routing_protocol == 'eigrp' and system_number: 
        config.extend([
            f"router {routing_protocol} {system_number}",
            f"bfd all-interfaces"
        ])
    if routing_protocol == 'rip':
        config.extend([
            f"router {routing_protocol}",
            f"bfd all-interfaces"
        ])
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not enable BFD on all interfaces for routing protocol {routing_protocol}. Error:\n{e}"
        )
