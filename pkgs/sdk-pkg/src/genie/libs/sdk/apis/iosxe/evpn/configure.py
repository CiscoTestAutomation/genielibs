"""Common configure/unconfigure functions for evpn"""

# Python
import logging
import re

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