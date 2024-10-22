"""Common configure functions for OSPF"""

# Python
import logging

# Genie
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement

# Unicon
from unicon.core.errors import SubCommandFailure

# Ospf
from genie.libs.sdk.apis.iosxe.ospf.get import (
    get_router_ospf_section_running_config,
)

from genie.libs.sdk.apis.utils import has_configuration

log = logging.getLogger(__name__)


def configure_ospf_max_metric_router_lsa_on_startup(
    device, ospf_process_id, metric_value):
    """Configure max-metric router-lsa on start-up

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            metric_value (`int`): Metric value to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cfg_cmd = [
        "router ospf {}".format(ospf_process_id),
        "max-metric router-lsa on-startup {}".format(metric_value),
    ]

    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring max-metric {metric_value}"
            " on device {device}, Error: {error}".format(
                metric_value=metric_value, device=device, error=e
            )
        ) from e

def unconfigure_ospf(device,ospf_process_id):

    """Remove ospf on device

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f"no router ospf {ospf_process_id}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring, Please verify"
        ) from e

def configure_shut_ospf(device, ospf_process_id):
    """ Configure shut on ospf process

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number

        Return:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring "shutdown" on "router ospf {}"'.format(ospf_process_id)
    )
    try:
        device.configure("router ospf {}\n" "shutdown".format(ospf_process_id))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed in configuring "shutdown" with '
            "ospf process {ospf_process} on device {device}, "
            "Error: {error}".format(
                ospf_process=ospf_process_id, device=device, error=e
            )
        ) from e

def redistribute_bgp_under_ospf(device,ospf_process_id,bgp_as,vrf=None):

    """Redistribute bgp prefixes under ospf

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            vrf (str): ospf with vrf

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if vrf:
        cfg_cmd = [
            "router ospf {} vrf {}".format(ospf_process_id,vrf),
            "redistribute bgp {}".format(bgp_as),
        ]
    else:
        cfg_cmd = [
            "router ospf {} ".format(ospf_process_id),
            "redistribute bgp {}".format(bgp_as),
        ]
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring, Please verify"
        ) from e

def configure_no_shut_ospf(device, ospf_process_id):
    """ Configure no shut on ospf process

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number

        Return:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring "no shutdown" on "router ospf {}"'.format(ospf_process_id)
    )
    try:
        device.configure(
            "router ospf {}\n" "no shutdown".format(ospf_process_id)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed in configuring "no shutdown" with '
            "ospf process {ospf_process} on device {device}, "
            "Error: {error}".format(
                ospf_process=ospf_process_id, device=device, error=e
            )
        ) from e

def remove_ospf_max_metric_configuration(device, ospf_process_id):
    """ Remove max-metric from running-config under ospf

        Args:
            device (`obj`): Device object
            ospf_process_id (`str`): Router OSPF id

        Return:
            None

        Raises:
            SubCommandFailure
    """

    section_dict = get_router_ospf_section_running_config(
        device=device, ospf_process_id=ospf_process_id
    )
    if section_dict:
        if has_configuration(
            configuration_dict=section_dict,
            configuration="max-metric router-lsa",
        ):
            try:
                device.configure(
                    [
                        "router ospf {ospf_process_id}".format(
                            ospf_process_id=ospf_process_id
                        ),
                        "no max-metric router-lsa",
                    ]
                )
            except SubCommandFailure as e:
                raise SubCommandFailure(
                    "Failed in removing max-metric from "
                    "running-config under ospf {ospf_process_id} on device "
                    "{device}, Error: {e}".format(
                        ospf_process_id=ospf_process_id,
                        device=device.name,
                        e=str(e),
                    )
                ) from e
    else:
        raise Exception(
            "Router OSPD id {ospf_process_id} is not "
            "configured in device {device}".format(
                ospf_process_id=ospf_process_id, device=device.name
            )
        )


def configure_ospf_passive_interface(device, interface, ospf_process_id):
    """Configure passive interface

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): ospf process id
            interface (`list`): interfaces to configure
            ex.)
                interface = ['tenGigabitEthernet0/4/0']

        Return:
            None

        Raises:
            SubCommandFailure
    """

    config = ["router ospf {}".format(ospf_process_id)]

    if not isinstance(interface, list):
        interface = [interface]

    for intf in interface:
        config.append(
            "passive-interface {}".format(Common.convert_intf_name(intf))
        )

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring passive interfaces {interface} "
            "with OSPF process id {ospf_process_id} on device {device}, "
            "Error: {e}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                device=device.name,
                e=str(e),
            )
        ) from e

def remove_ospf_passive_interface(device, interface, ospf_process_id):
    """Remove passive interface

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            interface (`list`): interfaces to configure
            ex.)
                interface = ['tenGigabitEthernet0/4/0']

        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = ["router ospf {}".format(ospf_process_id)]

    if not isinstance(interface, list):
        interface = [interface]

    for intf in interface:
        config.append(
            "no passive-interface {}".format(Common.convert_intf_name(intf))
        )

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing passive interfaces {interface}"
            "with OSPF process id {ospf_process_id}"
            " on device {device}, Error: {e}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                device=device.name,
                e=str(e),
            )
        ) from e


def configure_ospf_cost(device, interface, ospf_cost):
    """configure ospf cost

        Args:
            device (`obj`): Device object
            ospf_cost (`int`): Ospf cost value
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = []
    config.append("interface {}".format(interface))
    config.append("ip ospf cost {}".format(ospf_cost))
    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf cost {ospf_cost} is not configured on device"
            " {device} for interface {interface}".format(
                ospf_cost=ospf_cost, device=device, interface=interface
            )
        ) from e


def configure_ospf_networks(device, ospf_process_id, ip_address=None,\
                             netmask=None, area=None, router_id=None, bfd=None, vrf_name=None):
    """ Configures ospf on networks

        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            ip_address ('list'): List of ip_address' to configure
            netmask ('str'): Netmask to use
            area ('str'): Area to configure under
            router_id('str'): ospf router id
            bfd ('str', optional) : bfd name, default value is None
        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    cmd = [f'router ospf {ospf_process_id}{f" vrf {vrf_name}" if vrf_name else ""}']

    if ip_address:
        for ip in ip_address:
            cmd.append('network {ip_address} {netmask} area {area}'
                   .format(ip_address=ip, netmask=netmask, area=area))
    if router_id:
        cmd.append('router-id {router_id}'.format(router_id=router_id))
    if bfd:
        cmd.append("bfd {bfd}".format(bfd=bfd))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under ospf {ospf_process_id}".format(
                ospf_process_id=ospf_process_id, error=e
            )
        )

def configure_ospf_vrf(device, ospf_process_id, vrf, router_id):

    """ Configures router-id in ospf vrf
        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            vrf('str'): vrf id for ospf process
            router_id('str'): ospf router id
        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    cmd = ['router ospf {ospf_process_id} vrf {vrf}'.format(
                      ospf_process_id=ospf_process_id, vrf=vrf)]
    cmd.append('router-id {router_id}'.format(router_id=router_id))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring vrf {vrf} on ospf {ospf_process_id}."
            "Error:\n{error}".format(
            vrf=vrf, ospf_process_id=ospf_process_id, error=e)
        )

def unconfigure_ospf_router_id(device, ospf_process_id, router_id):
    """ unonfigures ospf router-id
        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            router_id ('str'): Router id to use

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure([
            'router ospf {ospf_process_id}'.format(
                ospf_process_id=ospf_process_id),
            'no router-id {router_id}'.format(router_id=router_id)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to remove the router-id {router_id} "
            "with OSPF process id {ospf_process_id}, Error: {error}".format(
                ospf_process_id=ospf_process_id,
                router_id=router_id, error=e
            )
        )

def redistribute_bgp_metric_type_under_ospf(device, ospf_process_id,
                                            vrf=None, bgp_as=None,
                                            metric_type=None, tag=None):
    """ redistributes bgp metric type under ospf
        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            vrf ('str'): vrf to be configured
            metric_type ('str'): metricy type used
            tag('str'): tag used in metric_type

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                'router ospf {ospf_process_id} vrf {vrf}'.format(
                  ospf_process_id=ospf_process_id, vrf=vrf),
                'redistribute bgp {bgp_as} metric-type {metric_type} tag {tag}'\
                    .format(bgp_as=bgp_as, metric_type=metric_type, tag=tag)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to redistributes bgp metric type under ospf  "
            "{ospf_process_id}, Error: {error}".format(
                ospf_process_id=ospf_process_id,
                error=e
            )
        )


def configure_ospf_routing_on_interface(device, interface, ospf_process_id,
                                        areaid):
    """ Configures ospf and ip routing on Interface

        Args:
            device ('obj'): Device to use
            interface ('str'): Interface to use
            ospf_process_id ('str'): Process id for ospf process
            areaid ('str'): Area id to use

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                'interface {interface}'.format(interface=interface),
                'ip ospf {ospf_process_id} area {areaid}'.format(
                    ospf_process_id=ospf_process_id, areaid=areaid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the interface {interface} "
            "with OSPF process id {ospf_process_id} and area {areaid}, "
            "Error: {error}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                areaid=areaid, error=e
            )
        )

def unconfigure_ospf_on_device(device, ospf_process_id):
    """ unconfigures ospf and ip routing on device
        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure('no router ospf {ospf_process_id}'.format(
            ospf_process_id=ospf_process_id))
    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Failed to unconfigure router ospf {ospf_process_id} "
                "on device, Error: {error}".format(
                    ospf_process_id=ospf_process_id, error=e))


def configure_ospf_message_digest_key(device, interface, message_digest_key,
                                      md5, key=None):
    '''
    configure ospf message digest key

        Args:
            device (`obj`): Device object
            key (`str`): key value
            message_digest_key (`str`): message digest key value
            md5 (`str`): md5 value
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None

        Raises:
            SubCommandFailure
    '''
    configs = ["interface {interface}".format(interface=interface)]
    if key:
        configs.append(
                    "ip ospf message-digest-key {message_digest_key} md5 "
                    "{md5} {key}".format(
                    message_digest_key=message_digest_key,md5=md5,key=key)
                )
    else:
        configs.append(
                    "ip ospf message-digest-key {message_digest_key} md5 "
                    "{md5}".format(
                    message_digest_key=message_digest_key,md5=md5)
                )

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf message-digest-key {key} is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
                key=message_digest_key, device=device,
                interface=interface, error=e
            )
        )


def configure_ospf_network_point(device, interface):
    """configure ospf point to point network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "ip ospf network point-to-point"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf network point-to-point is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )


def configure_ospf_network_broadcast(device, interface):
    """configure ospf broadcast network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None

        Raises:
            SubCommandFailure
    """
    configs = [
         f"interface {interface}",
         f"ip ospf network broadcast"
         ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Ospf network broadcast is not configured on device {device} for interface {interface}. Error:\n{e}"
           )

def configure_ospf_bfd(device, interface):
    """configure ospf ip bfd

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "ip ospf bfd"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf bfd is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ospf_priority(device, interface,priority):
    """configure ip ospf priority

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            priority('int'): Priority value to configure for ospf

        Return:
            None

        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"ip ospf priority {priority}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
          f"Ospf priority is not configured on device {device} for interface {interface}.Error:\n{e}"
        )
def unconfigure_ospfv3(device, pid):
    """unconfigure ospfv3

        Args:
            device (`obj`): Device object
            pid (`str`): Ospfv3 process id

        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no router ospfv3 {pid}".format(pid=pid))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospfv3 is not unconfigured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e
            )
        )

def configure_ospfv3(device, pid, router_id=None, vrf=None, nsr=None,
    graceful_restart=None, address_family=None, bfd=None,
    traffic_type=None, adjacency=None, redistribute=None, route_method=None,
    metric=0, metric_type=1):
    """configure ospf ip bfd

        Args:
            device (`obj`): Device object
            pid (`str`): Ospfv3 process id
            router_id (`str`, optional): Router id, default value is None
            vrf('str', optional): vrf id for ospf process
            nsr (`Bool`, optional): Nsr to be configured, default value is None
            graceful_restart (`Bool`, optional): Graceful restart to be
                                                 configured,default value is None
            address_family (`str`, optional): Address family to be configured,
                                              default value is None
            bfd ('str', optional) : bfd name, default value is None
            traffic_type('str' optional) : type of traffic
            adjacency('bool' optional): option to log adjacency changes
            redistribute('bool' optional): option to redistribute routes
            route_method('str' optional): route type to be redistributed
            metric('int' optional): route metric
            metric-type('int' optional): route metric type

        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = ["router ospfv3 {pid}".format(pid=pid)]
    if graceful_restart:
        config.append("graceful-restart")
    if nsr:
        config.append("nsr")
    if address_family and traffic_type:
        config.append(
            f"address-family {address_family} {traffic_type}")
        if router_id:
            config.append(f"router-id {router_id}")
    elif address_family:
        config.append(
            f"address-family {address_family}")
        if router_id:
            config.append(f"router-id {router_id}")
        if bfd:
            config.append("bfd {bfd}".format(bfd=bfd))
    if redistribute and metric and route_method and metric_type:
        config.append("redistribute {route_method} metric {metric} metric-type {metric_type}"
                .format(route_method=route_method,metric=metric, metric_type=metric_type))
    elif redistribute and route_method:
            config.append("redistribute {route_method}".format(route_method=route_method))
    if adjacency:
        config.append("log-adjacency-changes")
    config.append("exit-address-family")
    if vrf:
        config.append('address-family ipv6 unicast vrf {vrf}'.format(vrf=vrf))
        config.append('redistribute connected')
        if route_method:
            config.append('redistribute {route_method}'.format(route_method=route_method))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Ospfv3 is not configured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e
            )
        )

def configure_ospfv3_address_family(device, pid, address_family, modifier='',
    redistribute=None):
    """
        Configures address family for an ospfv3 process

        Args:
            pid ('int') : ospfv3 process id
            address_family ('str') : Address family (ipv4 or ipv6)
            modifier ('str', optional) : Address family modifier. Default None.
            redistribute ('str', optional) : Routing protocol to redistribute
                                             info from. Default None.

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = [
        f'router ospfv3 {pid}',
        f'address-family {address_family} {modifier}'
    ]
    if redistribute:
        cmd.append(f'redistribute {redistribute}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure address family. Error:\n{e}'
        )

def configure_ospf_routing(device, ospf_process_id, router_id=None,
                           router_config=True, nsf=None, nsf_options=None, nsr=None, nsr_options=None,
                           vrf_name=None, vrf_id=None, log_adjacency=False):
    """ Configures ospf and ip routing on device

        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            router_id ('str', optional): Router id to use, default value is None
            router_config ('bool', optional): To configure router-id or not,
                                              default value is None
            nsf ('bool', optional): nsf configuration, default value is None
            nsf_options ('str', optional): nsf params, default value is None
            nsr ('bool', optional): nsf configuration, default value is None
            nsr_options ('str', optional): nsr params, default value is None
            vrf_name ('str', optional): vrf name, default value is None
            vrf_id ('str', optional): vrf id, default value is None
            log_adjacency ('bool', optional): log-adjacency-changes, default value is False

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    config = []
    if router_config:
        if vrf_name:
            config.extend(
                [
                'router ospf {ospf_process_id} vrf {vrf_name} {vrf_id}'.format(
                    ospf_process_id=ospf_process_id, vrf_name=vrf_name,
                    vrf_id=vrf_id),
                    'router-id {router_id}'.format(router_id=router_id)
            ])
        else:
            config.extend(
                [
                    'router ospf {ospf_process_id}'.format(
                        ospf_process_id=ospf_process_id),
                    'router-id {router_id}'.format(router_id=router_id)
                ]
        )
    else:
        if vrf_name:
            config.append('router ospf {ospf_process_id} vrf {vrf_name}'.format(
                ospf_process_id=ospf_process_id, vrf_name=vrf_name))
        else:
            config.append('router ospf {ospf_process_id}'.format(
                ospf_process_id=ospf_process_id))
    if nsf:
        if nsf_options:
            config.append('nsf {nsf_options}'.format(
                        nsf_options=nsf_options))
        else:
            config.append('nsf')

    if nsr:
        if nsr_options:
            config.append('nsr {nsr_options}'.format(
                        nsr_options=nsr_options))
        else:
            config.append('nsr')

    if log_adjacency:
        config.append('log-adjacency-changes')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the device {device} "
            "with OSPF process id {ospf_process_id}, Error: {error}".format(
                ospf_process_id=ospf_process_id,
                device=device.name, error=e
            )
        )


def redistribute_route_map_under_ospf(device, ospf_process_id, route_map_name,
                                      redistributed_ospf):
    """ configure route-map to redistribute routes between dynamic routing protocols.

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number
            redistributed_ospf (`int`): ospf to be redistributed
            route_map_name (`str`): route map name
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "router ospf {ospf_process_id}".format(
                        ospf_process_id=ospf_process_id),
               "redistribute ospf {redistributed_ospf} match internal"
                " route-map {route_map_name}".format(
                redistributed_ospf=redistributed_ospf,
                route_map_name=route_map_name)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf route-map {route_map_name} configuration failed for "
            " for ospf {ospf_process_id}, Error: {error}".format(
               route_map_name=route_map_name, ospf_process_id=ospf_process_id,
               error=e
            )
        )


def configure_ospf_routing_on_interface(device, interface, ospf_process_id,
        areaid):
    """ Configures ospf and ip routing on Interface

        Args:
            device ('obj'): Device to use
            interface ('str'): Interface to use
            ospf_process_id ('str'): Process id for ospf process
            areaid ('str'): Area id to use

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                'interface {interface}'.format(interface=interface),
                'ip ospf {ospf_process_id} area {areaid}'.format(
                    ospf_process_id=ospf_process_id, areaid=areaid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the interface {interface} "
            "with OSPF process id {ospf_process_id} and area {areaid}, "
            "Error: {error}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                areaid=areaid, error=e
            )
        )


def configure_ip_prefix_list(device, prefix_list_name, seq, ip_address, subnet_id=32):
    """ configure prefix-list to pass a prefix

        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            seq (`int`): Sequence to insert to existing route-map entry
            ip_address (`str`): ip address to be used
            subnet_id (`int`): subnet_id to be used, default value is 32
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "ip prefix-list {prefix_list_name} seq {seq} permit {ip_address}/{subnet_id}"
            .format(prefix_list_name=prefix_list_name, seq=seq,
                    ip_address=ip_address, subnet_id=subnet_id)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure prefix-list {prefix_list_name} for "
            "{ip_address}, Error: {error}".format(
                prefix_list_name=prefix_list_name, ip_address=ip_address,
                error=e
            )
        )

def unconfigure_ospf_on_device(device, ospf_process_id, vrf_name=None):
    """ Unconfigures ospf and ip routing on device

        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            vrf_name ('str', optional): vrf name, default value is None

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    if vrf_name:
        cmd = "no router ospf {ospf_process_id} vrf {vrf_name}".format(
            ospf_process_id=ospf_process_id, vrf_name=vrf_name)
    else:
        cmd = "no router ospf {ospf_process_id}".format(
            ospf_process_id=ospf_process_id)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Failed to unconfigure router ospf {ospf_process_id} on device, \
                    Error: {error}".format(ospf_process_id=ospf_process_id, error=e))

def unconfigure_ip_prefix_list(device, prefix_list_name, seq, ip_address, subnet_id=32):
    """ unconfigure prefix-list

        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix-list name
            seq (`int`): Sequence number of a prefix list
            ip_address (`str`): ip address to be pass
            subnet_id('int'): default value is 32
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no ip prefix-list {prefix_list_name} seq {seq} permit "
            "{ip_address}/{subnet_id}".format(prefix_list_name=prefix_list_name,
                                     seq=seq, ip_address=ip_address, subnet_id=subnet_id)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure prefix-list {prefix_list_name} for "
            "{ip_address}, Error: {error}".format(
               prefix_list_name=prefix_list_name, ip_address=ip_address,
               error=e
            )
        )


def configure_route_map(device, route_map_name, permit, prefix_list_name=None, acl_name=None, acl_namev6=None, ip=None, ipv6=None, interface=None, set_extcommunity=None):

    """ configure route map

        Args:
            device ('obj'): device to execute on
            route_map_name ('int'): route map name
            permit ('int'): Sequence to insert to existing route-map entry
            prefix_list_name ('str',optional): prefix-list name to be used
            acl_name ('str',optional): IPv4 ACL to be used
            acl_namev6 ('str',optional): IPv6 ACL to be used
            ip ('str',optional): ip address
            ipv6 ('str',optional): ipv6 address
            interface ('str',optional): Interface to be used
            set_extcommunity ('str', optional): extcommunity value

        Return:
            None

        Raises:
            SubCommandFailure
    """
    # Build config string
    cfg_str = "route-map {route_map_name} permit {permit}\n".format(route_map_name=route_map_name, permit=permit)

    if prefix_list_name:
        cfg_str +="match ip address prefix-list {prefix_list_name}".format(
                prefix_list_name=prefix_list_name)
    if acl_name:
        cfg_str +="match ip address {acl_name}\n".format(
                acl_name=acl_name)
    if acl_namev6:
        cfg_str +="match ipv6 address {acl_namev6}\n".format(
                acl_namev6=acl_namev6)
    if interface:
        cfg_str +="set interface {interface}\n".format(
                interface=interface)
    if ip:
        cfg_str +="set ip next-hop {ip}\n".format(
                ip=ip)
    if ipv6:
        cfg_str +="set ipv6 next-hop {ipv6}\n".format(
                ipv6=ipv6)
    if set_extcommunity:
        cfg_str += f"set extcommunity {set_extcommunity}"
    try:
        device.configure(cfg_str)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route map {route_map_name}, Error: {error}"\
                .format(route_map_name=route_map_name, error=e
            )
        )


def configure_ospf_network_point(device, interface):
    """configure ospf point to point network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "ip ospf network point-to-point"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf network point-to-point is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )




def unconfigure_route_map(device, route_map_name, permit=None):

    """ unconfigure route map

        Args:
            device (`obj`): device to execute on
            route_map_name (`int`): route map name
            permit (`int`, optional): Sequence to insert to existing route-map entry
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if permit:
            device.configure(f"no route-map {route_map_name} permit {permit}")
        else:
            device.configure(f"no route-map {route_map_name}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route map {route_map_name}, Error: {error}"\
                .format(route_map_name=route_map_name, error=e
            )
        )

def configure_ospf_bfd(device, interface):
    """configure ospf ip bfd

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "ip ospf bfd"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf bfd is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ospf_redistributed_connected(device, ospf_process_id,vrf=None):

    """ configure redistribute connected under ospf

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): process id of ospf
            vrf ('str',optional): VRF name
        Return:
            None

        Raises:
            SubCommandFailure
    """
    if vrf:
        config = ["router ospf {} vrf {}".format(ospf_process_id,vrf)]
    else:
        config = ["router ospf {}".format(ospf_process_id)]

    config.append("redistribute connected")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure redistribute connected under ospf "
            "{ospf_process_id}, Error: {error}".format(
               ospf_process_id=ospf_process_id,
               error=e
            )
        )

def unconfigure_ospf_vrf_on_device(
    device, ospf_process_id, vrf=None):
    """ unonfigure destination in vrf
        Args:
            device ('obj'): Device object
            ospf_process_id('str'): ospf processid to unconfig
            vrf ('str'): Vrf name
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    
    cmd = "no router ospf {ospf_process_id}".format(
        ospf_process_id=ospf_process_id)
    if vrf:
        cmd += (" vrf {vrf}".format(
                    vrf=vrf
                )
            )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure router ospf {ospf_process_id}".format(
                ospf_process_id=ospf_process_id
            )
        )

def configure_maximum_path_under_ospf(
    device, ospf_process_id, max_path):
    """ configure maximum-path under ospf
        Args:
            device ('obj'): Device object
            ospf_process_id('int'): ospf processid to unconfig
            max_path('int'): maximum path to be installed
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """

    cmd=['router ospf {}'.format(ospf_process_id),'maximum-path {}'.format(max_path)]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure maximum-path under router ospf {ospf_process_id}".format(
                ospf_process_id=ospf_process_id
            )
        )

def configure_ospfv3_network_point(device, interface):
    """configure ospfv3 point to point network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "ipv6 ospf network point-to-point"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospfv3 network point-to-point is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def unconfigure_ospfv3_network(device, interface):
    """unconfigure ospfv3 network type

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "no ipv6 ospf network"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospfv3 network point-to-point is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ipv6_ospf_bfd(device, interface):
    """configure ipv6 ospf bfd

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "ipv6 ospf bfd"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ipv6 Ospf bfd is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def unconfigure_ipv6_ospf_bfd(device, interface):
    """unconfigure ipv6 ospf bfd

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "no ipv6 ospf bfd"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ipv6 Ospf bfd is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ipv6_ospf_mtu_ignore(device, interface):
    """configure ipv6 ospf mtu-ignore

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               " ipv6 ospf mtu-ignore"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ipv6 Ospf mtu-ignore is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def unconfigure_ipv6_ospf_mtu_ignore(device, interface):
    """unconfigure ipv6 ospf mtu-ignore

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "no ipv6 ospf mtu-ignore"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "failed to remove the ipv6 ospf mtu-ignore on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ipv6_ospf_routing_on_interface(device, interface, ospf_process_id,
                                        areaid):
    """ Configures ipv6 ospf  on Interface

        Args:
            device ('obj'): Device to use
            interface ('str'): Interface to use
            ospf_process_id ('str'): Process id for ospf process
            areaid ('int'): Area id to use

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                'interface {interface}'.format(interface=interface),
                'ipv6 ospf {ospf_process_id} area {areaid}'.format(
                    ospf_process_id=ospf_process_id, areaid=areaid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure the interface {interface} "
            "with OSPF process id {ospf_process_id} and area {areaid}, "
            "Error: {error}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                areaid=areaid, error=e
            )
        )

def unconfigure_ipv6_ospf_routing_on_interface(device, interface, ospf_process_id,
                                        areaid):
    """ UnConfigures ipv6 ospf  on Interface

        Args:
            device ('obj'): Device to use
            interface ('str'): Interface to use
            ospf_process_id ('str'): Process id for ospf process
            areaid ('int'): Area id to use

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                'interface {interface}'.format(interface=interface),
                'no ipv6 ospf {ospf_process_id} area {areaid}'.format(
                    ospf_process_id=ospf_process_id, areaid=areaid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure the interface {interface} "
            "with OSPF process id {ospf_process_id} and area {areaid}, "
            "Error: {error}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                areaid=areaid, error=e
            )
        )

def configure_ospf_redistributed_static(device, ospf_process_id):

    """ configure redistribute static under ospf
        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): process id of ospf
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config=["router ospf {ospf_process_id}".format(
                                    ospf_process_id=ospf_process_id), "redistribute static"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure redistribute static under ospf "
            "{ospf_process_id}, Error: {error}".format(
               ospf_process_id=ospf_process_id,
               error=e
            )
        )


def configure_ip_ospf_mtu_ignore(device, interface):
    """configure ip ospf mtu-ignore
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "ip ospf mtu-ignore"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ip Ospf mtu-ignore is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def unconfigure_ip_ospf_mtu_ignore(device, interface):
    """unconfigure ip ospf mtu-ignore
        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
               "interface {interface}".format(interface=interface),
               "no ip ospf mtu-ignore"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "failed to remove the ip ospf mtu-ignore on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_ospf_nsf_ietf(device, ospf_process_id):

    """ configure nsf ietf under ospf
        Args:
            device ('obj'): device to execute on
            ospf_process_id ('int'): process id of ospf
        Return:
            None
        Raises:
            SubCommandFailure :Failed to configure nsf ietf under ospf
    """
    log.debug(f"configure nsf ietf under ospf {ospf_process_id}")

    configs=[
        f"router ospf {ospf_process_id}",
        "nsf ietf"
    ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure nsf ietf under ospf {ospf_process_id}. Error:\n{e}")

def configure_ospf_area_type(device,ospf_process_id,area_id,area_type,area_subcmd="",nssa_translate_subcmd=None):
    """ configure area type under ospf
        Args:
            device ('obj'): device to execute on
            ospf_process_id ('int'): process id of ospf
            area_id ('int'): area number
            area_type ('str'): area type of ospf
            ex:
                stub or nssa
            area_subcmd ('str'): sub command for area type
            ex:
                area 5 stub <no-summary/no-ext-capability>
                area 5 nssa < default-information-originate/no-ext-capability/no-redistribution/
                            no-summary/translate>
            nssa_translate_subcmd ('str'): nssa translate sub commands
        Return:
            None
        Raises:
            SubCommandFailure : Failed to configure area type under ospf
    """

    config = []
    config.append(f'router ospf {ospf_process_id}')

    if area_type.lower() == 'stub':
        if area_subcmd:
            config.append(f'area {area_id} {area_type} {area_subcmd}')
        else:
            config.append(f'area {area_id} {area_type}')
    elif area_type.lower() == 'nssa':
        if area_subcmd:
            if area_subcmd.lower() == "translate":
                if nssa_translate_subcmd:
                    config.append(f'area {area_id} {area_type} {area_subcmd} type7 {nssa_translate_subcmd}')
                else:
                    log.error('missing nssa translate type')
            else:
                config.append(f'area {area_id} {area_type} {area_subcmd}')
        else:
            config.append(f'area {area_id} {area_type}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure area type under ospf {ospf_process_id}. Error:\n{e}")

def redistribute_eigrp_under_ospf(device,ospf_process_id,eigrp_as,vrf=None):
    """Redistribute eigrp prefixes under ospf
        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            vrf (str): ospf with vrf

        Returns:
            None

        Raises:
            SubCommandFailure : Failed to configure redistribute eigrp under ospf
    """

    cfg_cmd = []
    if vrf:
        cfg_cmd.append(f'router ospf {ospf_process_id} vrf {vrf}')
    else:
        cfg_cmd.append(f'router ospf {ospf_process_id}')

    cfg_cmd.append(f'redistribute eigrp {eigrp_as}')
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure redistribute eigrp under ospf {ospf_process_id}. Error:\n{e}")

def unconfigure_ospf_area_type(device,ospf_process_id,area_id,area_type):
    """ unconfigure area type under ospf
        Args:
            device ('obj'): device to execute on
            ospf_process_id ('int'): process id of ospf
            area_id ('int'): area number
            area_type ('str'): area type of ospf
            ex:
                stub or nssa
        Return:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure area type under ospf
    """

    config = []
    config.append(f'router ospf {ospf_process_id}')
    config.append(f'no area {area_id} {area_type}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure area type under ospf {ospf_process_id}. Error:\n{e}")

def unconfigure_redistribute_eigrp_under_ospf(device,ospf_process_id,eigrp_as,vrf=None):
    """unconfigure Redistribute eigrp prefixes under ospf
        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            vrf (str): ospf with vrf

        Returns:
            None

        Raises:
            SubCommandFailure : Failed to unconfigure redistribute eigrp under ospf
    """

    cfg_cmd = []
    if vrf:
        cfg_cmd.append(f'router ospf {ospf_process_id} vrf {vrf}')
    else:
        cfg_cmd.append(f'router ospf {ospf_process_id}')

    cfg_cmd.append(f'no redistribute eigrp {eigrp_as}')
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure redistribute eigrp under ospf {ospf_process_id}. Error:\n{e}")

def configure_ospf_network_non_broadcast(device, interface):
    """configure ospf non broadcast network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "ip ospf network non-broadcast"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf network non-broadcast is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def unconfigure_ospf_network_non_broadcast(device, interface):
    """unconfigure ospf non broadcast network

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {}".format(interface),
                 "no ip ospf network non-broadcast"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf network non-broadcast is not unconfigured on device"
            " {device} for interface {interface}, Error: {error}".format(
               device=device.name, interface=interface, error=e
            )
        )

def configure_neighbor_under_ospf(device, ospf_process_id, ip_address, ospf_cost=None):
    """ configure neighbor ip address under ospf process id.

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number
            ip_address (`str`): ip address to be used
            ospf_cost (`int`,optional): ospf cost
        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = []
    config.append(f'router ospf {ospf_process_id}')
    if ospf_cost:
        config.append(f'neighbor {ip_address} cost {ospf_cost}')
    else:
        config.append(f'neighbor {ip_address}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "neighbor {ip_address} configuration failed for "
            " for ospf {ospf_process_id}, Error: {error}".format(
               ospf_process_id=ospf_process_id,
               error=e
            )
        )

def unconfigure_neighbor_under_ospf(device, ospf_process_id, ip_address, ospf_cost=None):
    """ unconfigure neighbor ip address under ospf process id.

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number
            ip_address (`str`): ip address to be used
            ospf_cost (`int`,optional): ospf cost
        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = []
    config.append(f'router ospf {ospf_process_id}')
    if ospf_cost:
        config.append(f'no neighbor {ip_address} cost {ospf_cost}')
    else:
        config.append(f'no neighbor {ip_address}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "no neighbor {ip_address} configuration failed for "
            " for ospf {ospf_process_id}, Error: {error}".format(
               ospf_process_id=ospf_process_id,
               error=e
            )
        )

def configure_ospfv3_redistributed_connected(device, ospf_process_id):

    """ configure redistribute connected under ospf
        Args:
            device ('obj'): device to execute on
            ospf_process_id (int): process id of ospf
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config=[f"ipv6 router ospf {ospf_process_id}",
            "redistribute connected"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure redistribute connected under ospf "
            "{ospf_process_id}. Error:\n{e}"
        )

def configure_distribute_prefix_list_under_ospf(device, ospf_process_id,
                                                prefix_list_name, filter, vrf=None):
    """ Distribute prefix-list under ospf
        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            prefix_list_name (`str`): ip prefix list name to be used
            filter (`str`): filter option
            ex:)
                gateway  Filtering incoming updates based on gateway
                in       Filter incoming routing updates
                out      Filter outgoing routing updates
            vrf (`str`,optional): ospf with vrf
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cfg_cmd = []
    if vrf:
        cfg_cmd.append(f'router ospf {ospf_process_id} vrf {vrf}')
    else:
        cfg_cmd.append(f'router ospf {ospf_process_id}')

    cfg_cmd.append(f'distribute-list prefix {prefix_list_name} {filter}')
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure distribute prefix-list under ospf. Error:\n{e}")

def unconfigure_distribute_prefix_list_under_ospf(device, ospf_process_id,
                                                  prefix_list_name, filter, vrf=None):
    """ Unconfigure distribute prefix-list under ospf
        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            prefix_list_name (`str`): ip prefix list name to be used
            filter (`str`): filter option
            ex:)
                gateway  Filtering incoming updates based on gateway
                in       Filter incoming routing updates
                out      Filter outgoing routing updates
            vrf (`str`,optional): ospf with vrf
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cfg_cmd = []
    if vrf:
        cfg_cmd.append(f'router ospf {ospf_process_id} vrf {vrf}')
    else:
        cfg_cmd.append(f'router ospf {ospf_process_id}')

    cfg_cmd.append(f'no distribute-list prefix {prefix_list_name} {filter}')
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure distribute prefix-list under ospf. Error:\n{e}")

def redistribute_bgp_metric_route_map_under_ospf(device, ospf_process_id,
                                                bgp_as, ospf_metric,
                                                route_map=None):
    """ redistributes bgp metric route-map under ospf
        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            bgp_as('int'): BGP as number
            ospf_metric ('int'): Metric for redistributed routes
            route_map('str'): Route map reference
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cfg_cmd = []
    cfg_cmd.append(f'router ospf {ospf_process_id}')
    if route_map:
        cfg_cmd.append(f'redistribute bgp {bgp_as} metric {ospf_metric} route-map {route_map}')
    else:
        cfg_cmd.append(f'redistribute bgp {bgp_as} metric {ospf_metric}')
    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to redistribute bgp metric under ospf. Error:\n{e}")

def configure_ospfv3_max_lsa_limit(device, pid, lsa_limit):
    """configure ospfv3 max lsa limit
        Args:
            device (`obj`): Device object
            pid (`str`): Ospfv3 process id
            lsa_limit(int): configure the maximum lsa limit
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config = [
                  f'router ospfv3 {pid}',
                  f'max-lsa {lsa_limit}'
             ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ospfv3 max lsa limit. Error:\n{e}")

def configure_ospf_max_lsa_limit(device, pid, lsa_limit):
    """configure ospf max lsa limit
        Args:
            device (`obj`): Device object
            pid (`str`): Ospf process id
            lsa_limit(int): configure the maximum lsa limit
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config = [
                  f'router ospf {pid}',
                  f'max-lsa {lsa_limit}'
             ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ospf max lsa limit. Error:\n{e}")


def unconfigure_ospf_cost(device, interface, ospf_cost):
    """unconfigure ospf cost in interface

        Args:
            device ('obj'): Device object
            ospf_cost ('int'): Ospf cost value
            interface ('str'): interface to configure
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config = []
    config.append(f"interface {interface}")
    config.append(f"no ip ospf cost {ospf_cost}")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Error unconfiguring {ospf_cost} on device"
            " {device} with interface {interface}".format(
                ospf_cost=ospf_cost, device=device, interface=interface
            )
        ) from e


def configure_router_ospf_redistribute_internal_external(device, process_id, redistribute_ospf_route, redistribute_type, redistribute_type_route ):
    """configure router ospf redistribute internal/external
      Args:
            device ('obj'): device object
            process_id ('int'): process ID
            redistribute_ospf_route ('str'): redistribute ospf routes for external or internal
            redistribute_type('str'): resdistribute external or internal type routes
            redistribute_type_route('str'): Redistribute external type 2 routes

       Return:
            None
       Raises:
            SubCommandFailure : Failed configuring ospf  under redistribute
    """
    cmd=[f'router ospf {process_id}',
         f'redistribute ospf {process_id} match internal {redistribute_ospf_route} \
            {redistribute_type} {redistribute_ospf_route} {redistribute_type_route}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure router redistribute ospf with {redistribute_ospf_route}. Error:\n{e}")
       

def configure_ipv6_ospf_router_id(device, process_id, ospf_ip):
    """configure router-id under ipv6 ospf process
        Args:
            device ('obj'): Device object
            process_id ('str'): ospf process id
            ospf_ip(int): configure ospf router id in ip address format
        Return:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 ospf router
    """
    config = [f'ipv6 router ospf {process_id}',
              f'router-id {ospf_ip}'
             ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ipv6 router ospf. Error:\n{e}")


def unconfigure_ospf_from_interface(device, interface, ospf_process_id, area_id):
    """ unconfigure ospf from interface 
        Args:
            device (`obj`): device to execute on
            interface('str'): interface name            
            ospf_process_id (`int`): In range (1-65535)
            area_id('int'):In range (0-4294967295)
    Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}',
           f'no ip ospf {ospf_process_id} area {area_id}']   
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure ospf from interface Error:\n{e}")        

def configure_ospfv3_ipsec_ah(device, pid, areaid, spi, method, ah_key, ah_key_type=None):
    '''
    configure ospfv3 ipsec authentication
        Args:
            device (`obj`): Device object
            pid (`str`): ospfv3 process id
            areaid ('str'): Area id to use
            spi('str'): Security Policy Index  id to use
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["router ospfv3 {pid}".format(pid=pid)]
    if ah_key_type is None:
        config.append(
            "area {area} authentication ipsec spi {spi} {method} {ah_key}".format(area=areaid,
                                                                                  spi=spi,
                                                                                  method=method,
                                                                                  ah_key=ah_key))
    else:
        config.append(
            "area {area} authentication ipsec spi {spi} {method} {ah_key_type} {ah_key}".format(
                area=areaid, spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec authentication is not configured on device"
            " {device} Error: {error}".format(device=device, error=e)
        )


def configure_ospfv3_ipsec_esp(device, pid, areaid, spi, esp, esp_key, method, ah_key,
                               bit=128, esp_key_type=None, ah_key_type=None):
    '''
    configure ospfv3 ipsec encryption
        Args:
            device (`obj`): Device object
            pid (`str`): ospfv3 process id
            areaid ('str'): Area id to use
            spi('str'): Security Policy Index  id to use
            esp('str'):  encapsulating security payold id
            esp_key('str') encapsulation key
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            bit(int optional): aes-cbc uses bit value ,default value is 128
            esp_key_type('`str`, optional): Authentication key type,default value is None
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["router ospfv3 {pid}".format(pid=pid)]
    if esp == 'null':
        if ah_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp null {method} {ah_key}".format(
                    area=areaid, spi=spi, method=method, ah_key=ah_key))
        else:
            config.append(
                "area {area} encryption ipsec spi {spi} esp null {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    if esp == '3des' or esp == 'des':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == 'aes-cbc':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec encryption is not configured on device"
            " {device} Error: {error}".format(device=device, error=e)
        )


def configure_interface_ospfv3_ipsec_ah(device, interface, spi, method, ah_key,
                                        ah_key_type=None):
    '''
    configure ospfv3 ipsec authentication on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to use
            spi('str'): Security Policy Index  id to use
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["interface {interface}".format(interface=interface)]
    if ah_key_type is None:
        config.append(
            "ospfv3 authentication ipsec spi {spi} {method} {ah_key}".format(spi=spi, method=method,
                                                                             ah_key=ah_key))
    else:
        config.append(
            "ospfv3 authentication ipsec spi {spi} {method} {ah_key_type} {ah_key}".format(
                spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec authentication is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
                device=device, interface=interface, error=e
            )
        )


def configure_interface_ospfv3_ipsec_esp(device, interface, spi, esp, esp_key, method, ah_key,
                                   bit=128, esp_key_type=None, ah_key_type=None):
    '''
    configure ospfv3 ipsec encryption on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to use
            spi('str'): Security Policy Index  id to use
            esp('str'):  encapsulating security payold id
            esp_key('str') encapsulation key
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            bit(int optional): aes-cbc uses bit value ,default value is 128
            esp_key_type('`str`, optional): Authentication key type,default value is None
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["interface {interface}".format(interface=interface)]
    if esp == 'null':
        if ah_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp null {method} {ah_key}".format(spi=spi,
                                                                                      method=method,
                                                                                      ah_key=ah_key))
        else:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp null {method} {ah_key_type} {ah_key}".format(
                    spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == '3des' or esp == 'des':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key}".format(
                    spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key_type=ah_key_type,
                    ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == 'aes-cbc':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key}".format(
                    spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key_type=ah_key_type,
                    ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec encryption is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
                device=device, interface=interface, error=e
            )
        )


def unconfigure_ospfv3_ipsec_ah(device, pid, areaid, spi, method, ah_key, ah_key_type=None):
    '''
    unconfigure ospfv3 ipsec authentication
        Args:
            device (`obj`): Device object
            pid (`str`): ospfv3 process id
            areaid ('str'): Area id to use
            spi('str'): Security Policy Index  id to use
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["router ospfv3 {pid}".format(pid=pid)]
    if ah_key_type is None:
        config.append(
            "no area {area} authentication ipsec spi {spi} {method} {ah_key}".format(area=areaid,
                                                                                  spi=spi,
                                                                                  method=method,
                                                                                  ah_key=ah_key))
    else:
        config.append(
            "no area {area} authentication ipsec spi {spi} {method} {ah_key_type} {ah_key}".format(
                area=areaid, spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec authentication is not configured on device"
            " {device} Error: {error}".format(device=device, error=e)
        )


def unconfigure_ospfv3_ipsec_esp(device, pid, areaid, spi, esp, esp_key, method, ah_key,
                               bit=128, esp_key_type=None, ah_key_type=None):
    '''
    unconfigure ospfv3 ipsec encryption
        Args:
            device (`obj`): Device object
            pid (`str`): ospfv3 process id
            areaid ('str'): Area id to use
            spi('str'): Security Policy Index  id to use
            esp('str'):  encapsulating security payold id
            esp_key('str') encapsulation key
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            bit(int optional): aes-cbc uses bit value ,default value is 128
            esp_key_type('`str`, optional): Authentication key type,default value is None
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["router ospfv3 {pid}".format(pid=pid)]
    if esp == 'null':
        if ah_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp null {method} {ah_key}".format(
                    area=areaid, spi=spi, method=method, ah_key=ah_key))
        else:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp null {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    if esp == '3des' or esp == 'des':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == 'aes-cbc':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "no area {area} encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    area=areaid, spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key,
                    method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec encryption is not configured on device"
            " {device} Error: {error}".format(device=device, error=e)
        )


def unconfigure_interface_ospfv3_ipsec_ah(device, interface, spi, method, ah_key,
                                        ah_key_type=None):
    '''
    unconfigure ospfv3 ipsec authentication on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to use
            spi('str'): Security Policy Index  id to use
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["interface {interface}".format(interface=interface)]
    if ah_key_type is None:
        config.append(
            "no ospfv3 authentication ipsec spi {spi} {method} {ah_key}".format(spi=spi, method=method,
                                                                             ah_key=ah_key))
    else:
        config.append(
            "no ospfv3 authentication ipsec spi {spi} {method} {ah_key_type} {ah_key}".format(
                spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "no ospfv3 ipsec authentication is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
                device=device, interface=interface, error=e
            )
        )


def unconfigure_interface_ospfv3_ipsec_esp(device, interface, spi, esp, esp_key, method, ah_key,
                                   bit=128, esp_key_type=None, ah_key_type=None):
    '''
    unconfigure ospfv3 ipsec encryption on interface
        Args:
            device (`obj`): Device object
            interface ('str'): Interface to use
            spi('str'): Security Policy Index  id to use
            esp('str'):  encapsulating security payold id
            esp_key('str') encapsulation key
            method('str'): authentication alogrightm md5|sh1
            ah_key('str'): Authentication key
            bit(int optional): aes-cbc uses bit value ,default value is 128
            esp_key_type('`str`, optional): Authentication key type,default value is None
            ah_key_type('`str`, optional): Authentication key type,default value is None
        Return:
            None
        Return:
            None
        Raises:
            SubCommandFailure
    '''
    config = ["interface {interface}".format(interface=interface)]
    if esp == 'null':
        if ah_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp null {method} {ah_key}".format(spi=spi,
                                                                                      method=method,
                                                                                      ah_key=ah_key))
        else:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp null {method} {ah_key_type} {ah_key}".format(
                    spi=spi, method=method, ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == '3des' or esp == 'des':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key}".format(
                    spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, esp=esp, esp_key=esp_key, method=method, ah_key_type=ah_key_type,
                    ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp {esp} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, esp=esp, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
    if esp == 'aes-cbc':
        if ah_key_type is None and esp_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key}".format(
                    spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key=ah_key))
        elif ah_key_type is not None and esp_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, bit=bit, esp_key=esp_key, method=method, ah_key_type=ah_key_type,
                    ah_key=ah_key))
        elif esp_key_type is not None and ah_key_type is None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key}".format(
                    spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))
        elif (esp_key_type and ah_key_type) is not None:
            config.append(
                "no ospfv3 encryption ipsec spi {spi} esp aes-cbc {bit} {esp_key_type} {esp_key} {method} {ah_key_type} {ah_key}".format(
                    spi=spi, bit=bit, esp_key_type=esp_key_type, esp_key=esp_key, method=method,
                    ah_key_type=ah_key_type, ah_key=ah_key))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "ospfv3 ipsec encryption is not configured on device"
            " {device} for interface {interface}, Error: {error}".format(
                device=device, interface=interface, error=e
            )
        )


def clear_ospfv3_process_all(device):
    '''
     clear ospfv3 process
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to clear ospfv3 process
    '''
    log.info("clear ospfv3 process")
    ospfv3_res = Statement(
        pattern=r'Reset selected OSPFv3 processes\? \[no\]\:',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)
    try:
        device.execute("clear ospfv3 process", reply=Dialog([ospfv3_res]))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            " Failed to clear ospfv3 process,  Error: {error}".format(error=e)
        )


def configure_ospfv3_network_range(device, pid, router_id, address_family=None,
    traffic_type=None, adjacency=None, area=None, network_range=None):
    """configure_ospfv3_network_range

        Args:
            device (`obj`): Device object
            pid (`str`): Ospfv3 process id
            router_id (`str`): Router id
            address_family (`str`, optional): Address family to be configured,
                                              default value is None
            traffic_type (`str`, optional): configure the traffic_type
            adjacency('bool' optional): option to log adjacency changes
            area ('str',optional): Area to configure under. default value is None
            network_range ('str',optional) : network_range ip address . default value is None

        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = [f'router ospfv3 {pid}',
              f'router-id {router_id}']
    if adjacency:
        config.append("log-adjacency-changes")
    if address_family and traffic_type:
        config.append([f'address-family {address_family} {traffic_type}'])
    elif address_family:
        config.append([f'address-family {address_family}'])
    if area and network_range:
        config.append([f'area {area} range {network_range}'])
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Ospfv3 network range is not configured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e
            )
        )

def configure_ospfv3_on_interface(device, interface, pid, area):
    """confue_ospfv3_on_interface
        Args:
            device (`obj`): Device object
            interface ('str'): interface details
            pid (`str`): Ospfv3 process id
            area (int): Area to configure under.

        Return:
            None

        Raises:
            SubCommandFailure
    """
    config = [f'interface {interface}',
              f'ospfv3 {pid} area {area} ipv6']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Ospfv3 is not configured on interface"
            " {interface}, Error: {error}".format(
               interface=interface.name, error=e
            )
        )


def configure_ospf_redistributed_eigrp_metric(device, ospf_process_id, eigrp_as, metric=None):
    """configuring ospf redistributed eigrp with metric-type
    Args:
        device ('obj'): Device object
        ospf_process_id ('int'): OSPF process id
        eigrp_as ('str'): <1-65535>  AS number
        metric('str', optional): Set OSPF External Type 1/ Type 2 metrics
    Returns:
        None
    Raises:
        SubCommandFailure : Failed to configure redistribute eigrp with metric-type under ospf
    """

    config=[f'router ospf {ospf_process_id}']
    if metric:
       config.append(f'redistribute eigrp {eigrp_as} metric-type {metric} subnets')
    else:
       config.append(f'redistribute eigrp {eigrp_as}')
    
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure redistribute eigrp with metric-type under ospf {ospf_process_id}. Error:\n{e}")


def configure_snmp_if_index_on_ospfv3_process_id(device, ospf_process_id):
    """ configure snmp interface index on OSPFv3 process id
        Args:
            device ('obj'): Device object
            ospf_process_id ('str'): Process id for ospfv3 process
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure snmp if index on ospfv3 process id
    """
    log.debug("configure snmp interface index on OSPFv3 process id")
    cmd = [f"ipv6 router ospf {ospf_process_id}", 
           f"interface-id snmp-if-index"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure snmp interface index on OSPFv3 process id. Error:\n{error}".format(
                error=e
            )
        )

def redistribute_route_metric_vrf_green(device, ospf_process_id,vrf_name,
                                                bgp_asn, ospf_metric
                                                ):
    """ redistribute_route_metric_vrf_green
        Args:
            device ('obj'): Device to use
            ospf_process_id ('int'): Process id for ospf process
            vrf_name ('str'): Ospf vrf name
            bgp_asn('int'): BGP as Autonomous system number
            ospf_metric ('int'): Metric for redistributed routes
            
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"router ospf {ospf_process_id} vrf {vrf_name}",
           f"redistribute static metric {ospf_metric}",
           f"redistribute connected metric {ospf_metric}",
           f"redistribute bgp {bgp_asn} metric {ospf_metric}"
           ]    

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to redistribute metric under ospf. Error:\n{e}")        


def redistribute_bgp_on_ospfv3(device, pid, type, as_num):
    """redistribute bgp on ospfv3
        Args:
            device (`obj`): Device object
            pid (`str`): Ospfv3 process id
            type (`str`): ipv4 or ipv6
            as_num (`str`): Autonomous system number
        Return:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"router ospfv3 {pid}", f"address-family {type} unicast",
              f"redistribute bgp {as_num}", "exit-address-family"]
    try:
        device.configure(config)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to redistribute bgp on ospfv3 {device}, Error: {e}"
        )

def unconfigure_ipv6_router_ospf(device, ospf_process_id):

    """Remove ipv6 ospf on device
        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(f"no ipv6 router ospf {ospf_process_id}")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed in configuring, Please verify") from e 

def configure_ospfv3_network_type(device, interface, network_type):
    """Configure OSPFv3 network type on the specified interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g., 'GigabitEthernet1/0/24')
            network_type (`str`): OSPFv3 network type ('point-to-point', 'broadcast', 'non-broadcast', 'point-to-multipoint')
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        cmd = [
            f"interface {interface}",
            f"ospfv3 network {network_type}"
        ]

        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure OSPFv3 network type as '{network_type}' on interface {interface}. Error:\n{e}"
        )

def configure_ospfv3_interface(device, interface, process_id):
    """Configure OSPFv3 settings on the specified interface.
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (e.g., 'GigabitEthernet1/0/24')
            process_id (`int`): OSPFv3 Process ID (1-65535)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        cmd = [f"interface {interface}", 
        f"ospfv3 {process_id}"]
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure OSPFv3 on interface {interface}. Error:\n{e}"
        )
    
def configure_ospf_vrf_lite(device, ospf_process_id, vrf_name):
    """Configure vrf-lite capabilty for OSPF process.
        Args:
            device (`obj`): Device object
            ospf_process_id (`str`): OSPF Process ID (1-65535)
            vrf_name (`str`): VRF name (Eg : 'vrf1')
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        cmd = [f"router ospf {ospf_process_id} vrf {vrf_name}", 
        f"capability vrf-lite"]
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure vrf-lite capability for OSPF process {ospf_process_id}. Error:\n{e}"
        )
