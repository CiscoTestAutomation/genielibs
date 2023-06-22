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
            device ('obj'): Device object
            nve_num ('int'): nve interface number
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

def configure_l2vpn_evpn_flooding_suppression(device):
    """ Configure the flooding-suppression address-resolution disable on l2vpn evpn
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"l2vpn evpn",
                f"flooding-suppression address-resolution disable"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure the flooding-suppression address-resolution disable. Error:\n{error}".format(error=e)
        )

def configure_evpn_instance(device, evi, service_instance, encapsulation_type=None,
                         replication_type=None):
    """ Configure l2vpn evpn instance
        Args:
            device ('obj'): Device object
            evi ('int'): instance id
            service_instance ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            encapsulation_type ('str'): encapsulation type, vxlan|mpls
            replication_type ('str'): replication type, ingress|static
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info(
        "Configuring l2vpn evpn instance {evi}".format(evi=evi)
    )
    cmd = [
        "l2vpn evpn instance {evi} {service_instance}".format(
                evi=evi, service_instance=service_instance
            )
    ]
    if encapsulation_type:
        cmd.append(
            [
                "l2vpn evpn instance {evi}".format(evi=evi),
                "encapsulation {encap}".format(encap=encapsulation_type),
            ]
        )
    if replication_type:
        cmd.append(
            [
                "l2vpn evpn instance {evi}".format(evi=evi),
                "replication {replication_type}".format(replication_type=replication_type),
            ]
        )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Failed to configure l2vpn evpn instance {evi}. Error:\n{e}".format(
                    evi=evi,
                    e=e
                )
            )

def unconfigure_evpn_instance(device, evi):
    """ Unconfigure l2vpn evpn instance
        Args:
            device ('obj'): Device object
            evi ('int'): instance id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring l2vpn evpn instance {evi}".format(evi=evi)
    )
    cmd = "no l2vpn evpn instance {evi}".format(evi=evi)
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure l2vpn evpn instance {evi} Error:\n{e}".format(
                evi=evi,
                e=e
            )
        )

def unconfigure_l2vpn_evpn_flooding_suppression(device):
    """ Unconfigure the flooding-suppression address-resolution disable on l2vpn evpn
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"l2vpn evpn",
                f"no flooding-suppression address-resolution disable"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure the flooding-suppression address-resolution disable. Error:\n{error}".format(error=e)
        )


def configure_evpn_l2_instance_bd_association(device, bd_id,
                                              evpn_instance, vni_id=None):
    """ Configure configure VLAN association to EVPN instance
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            evpn_instance('int'): EVPN Instance id
            vni_id('int'): VNI id, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = ["bridge-domain {bd_id}".format(bd_id=bd_id)]
    if vni_id:
        configs.append(
            "member evpn-instance {evpn_instance} vni {vni_id}".format(
                evpn_instance=evpn_instance, vni_id=vni_id
            )
        )
    else:
        configs.append(
            "member evpn-instance {evpn_instance}".format(
                evpn_instance=evpn_instance
            )
        )

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VLAN association to EVPN L2 instance on device "
            'Error:\n{e}'.format(e=e)
        )

def unconfigure_evpn_l2_instance_bd_association(device, bd_id, evpn_instance):
    """ Configure configure VLAN association to EVPN instance
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            evpn_instance('int'): EVPN Instance id
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [
            "bridge-domain {bd_id}".format(bd_id=bd_id),
            "no member evpn-instance {evpn_instance}".format(
                evpn_instance=evpn_instance
            )
        ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VLAN association to EVPN L2 instance on device "
            'Error:\n{e}'.format(e=e)
        )

def configure_evpn_floodsuppress_dhcprelay_disable_globally(device):
    """ Configure l2vpn evpn flooding suppression dhcp-relay disable globally
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring "
        "'l2vpn evpn flooding suppression dhcp-relay disable' globally"
    )

    cmd = [
            "service internal",
            "l2vpn evpn",
            "flooding-suppression dhcp-relay disable",
            "no service internal"
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure "
            "'l2vpn evpn flooding suppression dhcp-relay disable' globally"
            'Error:\n{e}'.format(e=e)
        )

def unconfigure_evpn_floodsuppress_dhcprelay_disable_globally(device):
    """ Unconfigure l2vpn evpn flooding suppression dhcp-relay disable globally
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring "
        "'l2vpn evpn flooding suppression dhcp-relay disable' globally"
    )
    cmd = [
            "service internal",
            "l2vpn evpn",
            "no flooding-suppression dhcp-relay disable",
            "no service internal"
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure "
            "'l2vpn evpn flooding suppression dhcp-relay disable' globally"
            'Error:\n{e}'.format(e=e)
        )


def configure_evpn_ethernet_segment(device, segment_value, identifier_type=None, system_mac=None, esi_value=None, redundancy=True):
    """ Configure l2vpn evpn ethernet segment
        Args:
            device ('obj'): Device object
            segment_value ('obj'): Ethernet segment local discriminator value
            identifier_type ('obj', optional): Identifier type 0 or 3. Default is None
            system_mac ('obj', optional): MAC address. Default is None
            esi_value ('obj', optional): 9-octet ESI value in hex. Default is None
            redundancy ('bool', optional): Ethernet segment local discriminator value. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f'l2vpn evpn ethernet-segment {segment_value}']
    if identifier_type:
        cmd = f'identifier type {identifier_type}'
        if system_mac:
            cmd += f' system-mac {system_mac}'
        elif esi_value:
            cmd += f' {esi_value}'
        config.append(cmd)
    if redundancy:
        config.append('redundancy single-active')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure l2vpn evpn ethernet segment. Error:\n{e}")


def configure_interface_evpn_ethernet_segment(device, interface, segment_value):
    """ Configure interface evpn ethernet-segment
        Args:
            device ('obj'): device to use
            interface ('str'): Interface Name
            segment_value ('int'): Ethernet segment local discriminator value
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", f"evpn ethernet-segment {segment_value}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure interface evpn ethernet-segment. Error: {e}')


def configure_pvlan_loadbalancing_ethernetsegment_l2vpn_evpn(device, ethsegmentvalue, 
    esivalue='',  identifier_type='0', system_mac='', red_single_active='yes'):
    """ configure per vlan load balncing between PEs on ethernet segment 
        Args:
            device ('obj'): Device object
            ethsegmentvalue ('str'): Ethernet segment local discriminator value
            identifier_type ('str', optional): Identifier type {type 0 or type 3, default is type 0}
            esivalue  ('str', optional): 9-octet ESI value in hex {mandatory for type 0  identory type}
            system_mac  ('str', optional): system mac address{mandatory for type 3  identory type}
            red_single_active  ('str', optional): redundancy single active (yes or no, default value is "yes")
            
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("configure per vlan load balncing between PEs on ethernet segment")

    cmd = [f"l2vpn evpn ethernet-segment {ethsegmentvalue}"]
    if identifier_type=='0':
        cmd.append(f"identifier type {identifier_type} {esivalue}")
    else:
        cmd.append(f"identifier type {identifier_type} system-mac {system_mac}")
    if red_single_active=='yes':
        cmd.append(f"redundancy single-active")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure per vlan load balncing between PEs on ethernet segment {device}. Error:\n{e}"
        )


def unconfigure_mdt_config_on_vrf(device, vrfname, addressfamily, mdtparam1, mdtparam2, mdtparam3=''):
    """ unconfigure mdt bgp autodiscovery or mdt default group or mdt overlay protocol on VRF
        Args:
            device ('obj'): Device object
            vrfname ('str'): VRF Name            
            addressfamily ('str'): Address family ipv4 or ipv6
            mdtparam1  ('str'): "auto-discovery" for BGP auto-discovery for MVPN,
                                "default" for the default group,"overlay" for MDT Overlay Protocol 
            mdtparam2  ('str'): "vxlan" for BGP auto-discovery for MVPN and default group,"use-bgp" for MDT Overlay Protocol
            mdtparam3  ('str', optional): no values needed for BGP auto-discovery for MVPN, 
                                        "IP address" for default group,"spt-only" for MDT Overlay Protocol
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("unconfigure mdt bgp autodiscovery or mdt default group or mdt overlay protocol on VRF")
    cmd = [f"vrf definition {vrfname}", f"address-family {addressfamily}",
                f"no mdt {mdtparam1} {mdtparam2} {mdtparam3}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure mdt bgp autodiscovery on VRF {device}. Error:\n{e}"
        )
