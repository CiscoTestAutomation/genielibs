"""Common configure/unconfigure functions for evpn"""

# Python
import logging
import re
from unicon.eal.dialogs import Dialog, Statement

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_evpn_instance_vlan_based_with_reoriginate_rt5(device, instance):
    """ Configuring l2vpn evpn instance vlan based by re-originating RT-5
        Args:
            device (`obj`): Device object
            instance (`int`): instance number
        Returns:
            console ouput ('str'): incase of successful configuration
        Raises:
            SubCommandFailure
    """
    config = []
    config.append("l2vpn evpn instance {} vlan-based".format(instance))
    config.append("re-originate route-type5")

    try:
        output = device.configure(config)
    except SubCommandFailure as e:
        log.error("Configuration failed for re-origination of route-type 5"
            "of instance: {} with exception:\n{}".format(instance, str(e))
        )

    return output


def unconfigure_evpn_instance_vlan_based(device, instance):
    """ Unconfiguring l2vpn evpn instance configuration
        Args:
            device (`obj`): Device object
            instance (`int`): instance number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            "no l2vpn evpn instance {instance} vlan-based".format(
                instance=instance)
        )
    except SubCommandFailure as e:
        log.error("Could not unconfig l2vpn evpn instance {instance},"
             "Error:\n{error}".format(instance=instance, error=e)
        )
        raise

def configure_l2vpn_evpn(device):
    """ Config l2vpn evpn
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn evpn' globally"
    )
    
    configs = []
    configs.append("l2vpn evpn")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn' globally"
            'Error:{e}'.format(e=e)
        )

def unconfigure_l2vpn_evpn(device):
    """ unconfig l2vpn evpn 
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring 'l2vpn evpn' globally"
    )
    
    configs = []
    configs.append("no l2vpn evpn")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure 'l2vpn evpn' globally"
            'Error:{e}'.format(e=e)
        )

def configure_l2vpn_evpn_router_id(device,interface):
    """ Config l2vpn evpn
        Args:
            device ('obj'): Device object
            interface ('str'): interface type 
                               loopback | physical
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''Configuring 'l2vpn evpn router_id ' globally'''
 
    
    configs = []
    configs.append("l2vpn evpn")
    configs.append("router-id {interface}".format(interface=interface))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn router_id' globally "
            'Error:{e}'.format(e=e)
        )

def unconfigure_l2vpn_evpn_router_id(device,interface):
    """ unconfig l2vpn evpn 
        Args:
            device (`obj`): Device object
            interface ('str'): interface type 
                               loopback | physical
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring 'l2vpn evpn router_id' globally"
    )
    
    configs = []
    configs.append("l2vpn evpn")
    configs.append("no router-id {interface}".format(interface=interface))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unnconfigure 'l2vpn evpn router_id' globally "
            'Error:{e}'.format(e=e)
        )

def configure_evpn_replication_type(device,rep_type):
    """ Config l2vpn evpn instance
        Args:
            device (`obj`): Device object
            rep_type ('str'): replication type 
                              static | ingress
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn evpn multicast replication type' {rep_type} globally ".format(rep_type=rep_type)
    )
    
    configs = []
    configs.append("l2vpn evpn")
    configs.append("replication-type {rep_type}".format(rep_type=rep_type))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn multicast replication type' globally"
            'Error:{e}'.format(e=e)
        )

def unconfigure_evpn_replication_type(device, rep_type ):
    """ Config l2vpn evpn instance
        Args:
            device (`obj`): Device object
            rep_type ('str'): replication type 
                              static | ingress
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring 'l2vpn evpn multicast replication type' {rep_type}  globally".format(rep_type=rep_type)
    )

    configs = []
    configs.append("l2vpn evpn")
    configs.append("no replication-type {rep_type}".format(rep_type=rep_type))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure 'l2vpn evpn multicast replication type' globally"
            'Error:{e}'.format(e=e)
        )

def configure_evpn_instance_encapsulation_type(device, evi, srvinst , encap_type):
    """ Config l2vpn evpn replication type on evi
        Args:
            device (`obj`): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            encap_type ('str): encapsulation 
                               vxlan | mpls 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn evpn evi instance - encapsulation type' on evi {evi}".format(evi=evi) 
    )

    configs = []
    configs.append("l2vpn evpn instance {evi} {srvinst}".format(evi=evi, srvinst=srvinst))
    configs.append("encapsulation {encap_type}".format(encap_type=encap_type))

    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn multicast replication type "
            'Error:{e}'.format(e=e) 
        )

def unconfigure_evpn_instance_encapsulation_type(device, evi, srvinst , encap_type):
    """ Config l2vpn evpn replication type on evi
        Args:
            device (`obj`): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            encap_type ('str): encapsulation 
                               vxlan | mpls 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unconfiguring 'l2vpn evpn evi instance - encapsulation type' on evi {evi}".format(evi=evi) 
    )

    configs = []
    configs.append("l2vpn evpn instance {evi} {srvinst}".format(evi=evi, srvinst=srvinst))
    configs.append("no encapsulation {encap_type}".format(encap_type=encap_type))

    try:
        device.configure(configs)

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn multicast replication type ' "
            "on evi {evi}".format(evi=evi, srvinst=srvinst, encap_type=encap_type) 
            
        )

def configure_evpn_evi_replication_type(device, evi, srvinst , rep_type):
    """ Config l2vpn evpn replication type on evi
        Args:
            device (`obj`): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            rep_type ('str'): replication type 
                              static | ingress
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn evpn evi - multicast replication type' on evi {evi}".format(evi=evi) 
    )

    configs = []
    configs.append("l2vpn evpn instance {evi} {srvinst}".format(evi=evi, srvinst=srvinst))
    configs.append("replication-type {rep_type}".format(rep_type=rep_type))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2vpn evpn multicast replication type under evi "
            'Error:{e}'.format(e=e)
        )

def unconfigure_evpn_evi_replication_type(device, evi, srvinst, rep_type):
    """ Config l2vpn evpn multicast advertise disable on evi
        Args:
            device (`obj`): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            rep_type ('str'): replication type 
                              static | ingress
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn evpn evi - multicast replication type' on evi {evi}".format(evi=evi))

    configs = []
    configs.append("l2vpn evpn instance {evi} {srvinst}".format(evi=evi, srvinst=srvinst))
    configs.append("no replication-type {rep_type}".format(rep_type=rep_type))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure 'l2vpn evpn multicast replication type under evi "
            'Error:{e}'.format(e=e)
        )

def configure_evpn_default_gateway_advertise_global(device):
    """ Configure default-gateway advertise in l2vpn evpn globally

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = []
    configs.append("l2vpn evpn")
    configs.append("default-gateway advertise")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure default-gateway advertise on globally "
            'Error:{e}'.format(e=e)
        )

def unconfigure_evpn_default_gateway_advertise_global(device):
    """ Unconfigure default-gateway advertise in l2vpn evpn globally

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = []
    configs.append("l2vpn evpn")
    configs.append("no default-gateway advertise")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure default-gateway advertise on globally "
            'Error:{e}'.format(e=e)
        )
        
def configure_evpn_l2_instance_vlan_association(device,vlan_id,evpn_instance,vni_id):
    """ Configure configure VLAN association to EVPN instance
        Args:
            device (`obj`): Device object
            vlan_id (`int`): Vlan id
            evpn_instance('int'): EVPN Instance id
            vni_id('int'): VNI id

        Returns:
            None

        Raises:
            SubCommandFailure

    """

    configs = []
    configs.append("vlan configuration {vlan_id}".format(vlan_id = vlan_id))
    configs.append("member evpn-instance  {evpn_instance} vni {vni_id}".format(evpn_instance=evpn_instance,vni_id = vni_id))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VLAN association to EVPN L2 instance on device "
            'Error:{e}'.format(e=e)
        )

def unconfigure_evpn_l2_instance_vlan_association(device,vlan_id,evpn_instance,vni_id):
    """ unconfigure VLAN association to EVPN instance

        Args:
            device (`obj`): Device object
            vlan_id (`int`): Vlan id
            evpn_instance('int'): EVPN Instance id
            vni_id('int'): VNI id

        Returns:
            None

        Raises:
            SubCommandFailure

    """

    configs = []
    configs.append("vlan configuration {vlan_id}".format(vlan_id = vlan_id))
    configs.append("no member evpn-instance  {evpn_instance} vni {vni_id}".format(evpn_instance=evpn_instance,vni_id = vni_id))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure VLAN association to EVPN L2 instance on device "
            'Error:{e}'.format(e=e)
        )

def configure_evpn_l3_instance_vlan_association(device,vlan_id,vni_id):
    """ configure VLAN association to EVPN l3 vni instance

        Args:
            device (`obj`): Device object
            vlan_id (`int`): Vlan id
            vni_id('int'): VNI id
        Returns:
            None

        Raises:
            SubCommandFailure

    """

    configs = []
    configs.append("vlan configuration {vlan_id}".format(vlan_id = vlan_id))
    configs.append("member vni {vni_id}".format(vni_id = vni_id))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VLAN association to EVPN L3 instance on device "
            'Error:{e}'.format(e=e)
        )

def unconfigure_evpn_l3_instance_vlan_association(device,vlan_id,vni_id):
    """ unconfigure VLAN association to EVPN l3 vni instance

        Args:
            device (`obj`): Device object
            vlan_id (`int`): Vlan id
            vni_id('int'): VNI id

        Returns:
            None

        Raises:
            SubCommandFailure

    """

    configs = []
    configs.append("vlan configuration {vlan_id}".format(vlan_id = vlan_id))
    configs.append("no member vni {vni_id}".format(vni_id = vni_id))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure VLAN association to EVPN L3 instance on device "
            'Error:{e}'.format(e=e)
        )

def configure_nve_interface(device,nve_num,src_intf,protocol,vni_id,replication_type,mcast_group=None, l3vni=False,vrf_name=None):
    """ Configure nve interface

        Args:
            device (`obj`): Device object
            nve_num (`str`): nve interface number
            src_intf (`str`): source interface
            protocol (`str`): host-reachability protocol
            vni_id (`str`): vni id
            replication_type (`str`): replication type (static | ingress)
            mcast_group (`str`, optional): Multicast group address , default value is None
            l3vni (`str`, optional): l3vni enable/disable , default value is False
            vrf_name (`str`, optional): VRF Name , default value is None
        
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = []
    configs.append("interface nve {nve_num}".format(nve_num=nve_num))
    configs.append("source-interface {intf}".format(intf=src_intf))
    configs.append("host-reachability protocol {protocol}".format(protocol=protocol))
    
    if l3vni is True:
        if vrf_name is None :
            raise Exception("missing required  argument: 'vrf_name'")
        else:
            configs.append("member vni {vni_id} vrf {vrf_name}".format(vni_id=vni_id, vrf_name=vrf_name))
   
    else:
        if replication_type.lower() == 'static': 
            if mcast_group is None:
                raise Exception("missing required  argument: 'mcast_group'")
            else:
                configs.append("member vni {vni_id} mcast-group {mcast_group}".format(vni_id=vni_id, mcast_group=mcast_group))

        else:
            configs.append("member vni {vni_id} ingress-replication".format(vni_id=vni_id))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure nve interface on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )

def unconfigure_nve_interface(device,nve_num):
    """ unconfigure nve interface

        Args:
            device (`obj`): Device object
            nve_num (`str`): nve interface number

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = []
    configs.append("no interface nve {nve_num}".format(nve_num=nve_num))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure nve interface on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )


def change_nve_source_interface(device, nve_num, source_interface):
    """ change source-interface for nve interface

        Args:
            device (`obj`)         : Device object
            nve_num (`str`)        : nve interface number
            source_interface('str'): source-interface to change to
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [
        f"int nve{nve_num}",
        f"source-interface {source_interface}",
        ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to change source-interface for NVE. Error:\n{e}")
            
def enable_multicast_advertise_on_evi(device, evi, srvinst):
    """ Enable multicast advertise on evi
        Args:
            device ('obj'): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to enable multicast advertise on evi
    """
    log.info(
        f"Configuring 'l2vpn evpn evi instance - enable multicast advertise' on evi {evi}"
    )

    configs = [
        f"l2vpn evpn instance {evi} {srvinst}",
        "multicast advertise enable"
    ]
    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"enable multicast advertise on evi {evi}. Error:\n{e}" 
        )
        
def configure_replication_type_on_evi(device, evi, srvinst, replication_type):
    """ Configure replication-type on evi
        Args:
            device ('obj'): Device object
            evi ('int'): evi id
            srvinst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            replication_type ('str'): replication type
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure replication-type on evi
    """
    log.info(
        f"Configuring 'l2vpn evpn evi instance - replication-type' on evi {evi}"
    )

    configs = [
        f"l2vpn evpn instance {evi} {srvinst}",
        f"replication-type {replication_type}"
    ]
    
    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"configure replication-type {replication_type} on evi {evi}. Error:\n{e}" 
        )


def configure_nve_interface_group_based_policy(device, nve_num):
    """ Configure group-based-policy for nve interface
        Args:
            device (`obj`): Device object
            nve_num (`int`): nve interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = []
    configs.append("interface nve {nve_num}".format(nve_num=nve_num))
    configs.append("group-based-policy")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure nve interface on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,))
            
def unconfigure_nve_interface_group_based_policy(device, nve_num):
    """ Un-configure group-based-policy for nve interface
        Args:
            device (`obj`): Device object
            nve_num (`int`): nve interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface nve {nve_num}".format(nve_num=nve_num))
    configs.append("no group-based-policy")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure nve interface on device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,))


def clear_bgp_l2vpn_evpn(device):
    """ clear bgp l2vpn evpn
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear bgp l2vpn evpn on {device}".format(device=device))

    dialog = Dialog([Statement(pattern=r'\[confirm\].*', action='sendline(\r)',loop_continue=True,continue_timer=False)])

    try:
        device.execute("clear bgp l2vpn evpn *", reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear bgp l2vpn evpn on {device}. Error:\n{error}".format(device=device, error=e)
        )

