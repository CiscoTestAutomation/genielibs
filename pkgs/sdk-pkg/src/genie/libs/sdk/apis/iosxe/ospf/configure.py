"""Common configure functions for OSPF"""

# Python
import logging

# Genie
from genie.libs.parser.utils.common import Common

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
                             netmask=None, area=None,router_id=None):
    """ Configures ospf on networks

        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            ip_address ('list'): List of ip_address' to configure
            netmask ('str'): Netmask to use
            area ('str'): Area to configure under
            router_id('str'): ospf router id

        Returns:
            N/A

        Raises:
            SubCommandFailure
    """
    cmd = ['router ospf {ospf_process_id}'\
        .format(ospf_process_id=ospf_process_id)]

    if ip_address:
        for ip in ip_address:
            cmd.append('network {ip_address} {netmask} area {area}'
                   .format(ip_address=ip, netmask=netmask, area=area))
    if router_id:
        cmd.append('router-id {router_id}'.format(router_id=router_id))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to add network under ospf {ospf_process_id}".format(
                ospf_process_id=ospf_process_id
            )
        ) from e

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
    """configure ospf message digest key

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
    """
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
    graceful_restart=None, address_family=None, bfd=None):
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
    if address_family:
        config.extend([
            "address-family {addr}".format(addr=address_family),
            "router-id {id}".format(id=router_id)])
        if bfd:
            config.append("bfd {bfd}".format(bfd=bfd))
    if vrf:
        config.append('address-family ipv6 unicast vrf {vrf}'.format(vrf=vrf))
        config.append('redistribute connected')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospfv3 is not configured on device"
            " {device}, Error: {error}".format(
               device=device.name, error=e
            )
        )

def configure_ospf_routing(device, ospf_process_id, router_id=None,
                           router_config=True, nsf=None,
                           vrf_name=None, vrf_id=None):
    """ Configures ospf and ip routing on device

        Args:
            device ('obj'): Device to use
            ospf_process_id ('str'): Process id for ospf process
            router_id ('str', optional): Router id to use, default value is None
            router_config ('bool', optional): To configure router-id or not, 
                                              default value is None
            nsf ('bool', optional): nsf configuration, default value is None
            vrf_name ('str', optional): vrf name, default value is None
            vrf_id ('str', optional): vrf id, default value is None

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
        config.append('router ospf {ospf_process_id}'.format(
            ospf_process_id=ospf_process_id))
    if nsf:
        config.append('nsf')

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
             
        
def configure_ip_prefix_list(device, prefix_list_name, seq, ip_address):
    """ configure prefix-list to pass a prefix

        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            seq (`int`): Sequence to insert to existing route-map entry
            ip_address (`str`): ip address to be used
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "ip prefix-list {prefix_list_name} seq {seq} permit {ip_address}/32"
            .format(prefix_list_name=prefix_list_name, seq=seq, 
                    ip_address=ip_address)  
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure prefix-list {prefix_list_name} for "
            "{ip_address}, Error: {error}".format(
                prefix_list_name=prefix_list_name, ip_address=ip_address,
                error=e
            )
        )

def unconfigure_ospf_on_device(device, ospf_process_id):
    """ Unconfigures ospf and ip routing on device

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
    
        
def unconfigure_ip_prefix_list(device, prefix_list_name, seq, ip_address):
    """ unconfigure prefix-list

        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix-list name
            seq (`int`): Sequence number of a prefix list
            ip_address (`str`): ip address to be pass
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no ip prefix-list {prefix_list_name} seq {seq} permit "
            "{ip_address}/32".format(prefix_list_name=prefix_list_name, 
                                     seq=seq, ip_address=ip_address)  
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure prefix-list {prefix_list_name} for "
            "{ip_address}, Error: {error}".format(
               prefix_list_name=prefix_list_name, ip_address=ip_address,
               error=e
            )
        )

        
def configure_route_map(device, route_map_name, permit, prefix_list_name):

    """ configure route map

        Args:
            device (`obj`): device to execute on
            route_map_name (`int`): route map name
            permit (`int`): Sequence to insert to existing route-map entry
            prefix_list_name (`str`): prefix-list name to be used
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure([
            "route-map {route_map_name} permit {permit}".format(
                route_map_name=route_map_name, permit=permit),
            "match ip address prefix-list {prefix_list_name}".format(
                prefix_list_name=prefix_list_name)]     
        )
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


    

def unconfigure_route_map(device, route_map_name, permit):

    """ unconfigure route map

        Args:
            device (`obj`): device to execute on
            route_map_name (`int`): route map name
            permit (`int`): Sequence to insert to existing route-map entry
        Return:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure([
            "no route-map {route_map_name} permit {permit}".format(
                route_map_name=route_map_name, permit=permit)]     
        )
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

    
        
def configure_ospf_redistributed_connected(device, ospf_process_id):

    """ configure redistribute connected under ospf

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): process id of ospf
        Return:
            None

        Raises:
            SubCommandFailure
    """
    config=["router ospf {ospf_process_id}".format(
                                    ospf_process_id=ospf_process_id)]
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
