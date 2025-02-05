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

def configure_evpn_l2_instance_vlan_association(device,vlan_id,evpn_instance,vni_id,protected=False):
    """ Configure configure VLAN association to EVPN instance
        Args:
            device (`obj`): Device object
            vlan_id (`int`): Vlan id
            evpn_instance('int'): EVPN Instance id
            vni_id('int'): VNI id
            protected('bool'): protected knob True or False
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("vlan configuration {vlan_id}".format(vlan_id = vlan_id))
    if protected is True:
        configs.append("member evpn-instance  {evpn_instance} vni {vni_id} protected".format(evpn_instance=evpn_instance,vni_id = vni_id))
    else:
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

def configure_evpn_l3_instance_bd_association(device, bd_id, vni_id):
    """ configure BD association to EVPN l3 vni instance

        Args:
            device (`obj`): Device object
            bd_id (`int`): Bridge Domain id
            vni_id('int'): VNI id
        Returns:
            None

        Raises:
            SubCommandFailure

    """

    configs = [
        f"bridge-domain {bd_id}",
        f"member vni {vni_id}"
    ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure BD association to EVPN L3 instance on device "
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
                                              evpn_instance, vni_id=None, eth_tag=None):
    """ Configure evpn instance association with bd
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            evpn_instance('int'): EVPN Instance id
            vni_id('int'): VNI id, default is None
            eth_tag('int'): Ethernet tag, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = ["bridge-domain {bd_id}".format(bd_id=bd_id)]
    if eth_tag:
        configs.append(
            "member evpn-instance {evpn_instance} vni {vni_id} ethernet-tag {eth_tag}".format(
                evpn_instance=evpn_instance, vni_id=vni_id, eth_tag=eth_tag
            )
        )
    elif vni_id:
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
            "Failed to configure EVPN Instance association with bd on device "
            'Error:\n{e}'.format(e=e)
        )

def unconfigure_evpn_l2_instance_bd_association(device, bd_id, evpn_instance):
    """ Unconfigure EVPN Instance association with bd
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
            "Failed to unconfigure EVPN Instance association with bd"
            'Error:\n{e}'.format(e=e)
        )

def configure_evpn_l2_profile_bd_association(device, bd_id,
                                              evpn_name):
    """ Configure EVPN profile association with bd
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            evpn_name('str'): EVPN Instance Profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [
        f"bridge-domain {bd_id}",
        f"member evpn-instance profile {evpn_name}"
    ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure EVPN Profile assosication with bd on device"
            'Error:\n{e}'.format(e=e)
        )

def unconfigure_evpn_l2_profile_bd_association(device, bd_id,
                                              evpn_name):
    """ Unconfigure EVPN profile association with bd
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            evpn_name('str'): EVPN Instance Profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [
          f"bridge-domain {bd_id}",
          f"no member evpn-instance profile {evpn_name}"
         ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure EVPN Profile assosication with bd on device"
            'Error:\n{e}'.format(e=e)
        )
def configure_vlan_service_instance_bd_association(device, bd_id,
                                                   vlan_instance, service_instance):
    """Configure configure VLAN Service Instance Association to EVPN instance
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            vlan_instance('str'): VLAN Instance
            service_instance('int'): Service Instance Id
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [
          f"bridge-domain {bd_id}",
          f"member {vlan_instance} service-instance {service_instance}"
         ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure VLAN Service Instance association to EVPN L2 instance on device "
            'Error:\n{e}'.format(e=e)
        )

def unconfigure_vlan_service_instance_bd_association(device, bd_id,
                                                     vlan_instance, service_instance):
    """ Configure unconfigure VLAN Service Instance Association to EVPN instance
        Args:
            device ('obj'): Device object
            bd_id ('int'): bridge-domain id
            vlan_instance('str'): VLAN Instance
            service_instance('int'): Service Instance Id
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [
            "bridge-domain {bd_id}".format(bd_id=bd_id),
            "no member {vlan_instance} service-instance {service_instance}".format(
              vlan_instance=vlan_instance, service_instance=service_instance
            )
           ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure VLAN Service Instance association to EVPN L2 instance on device "
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

def unconfigure_interface_evpn_ethernet_segment(device, interface):
    """ Unconfigure interface evpn ethernet-segment
        Args:
            device ('obj'): device to use
            interface ('str'): Interface Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", f"no evpn ethernet-segment"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure interface evpn ethernet-segment. Error: {e}')
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


def configure_evpn_instance_evi(device, evi, srv_inst, conf_command_list=None, encap_type=None, mode_type=None):
    """ Configure evpn instance evi
        Args:
            device ('obj'): Device object
            evi ('int'): evi id
            srv_inst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware
            conf_command_list('list',optional): L2VPN EVPN instance configuration commands, default value is None
            encap_type ('str',optional): encapsulation, default value is None
                                         vxlan | mpls
            mode_type ('str',optional): ip local-learning, default value is None
                                        disable | enable
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'evpn instance' on evi {evi}".format(evi=evi)
    )

    configs = [f'l2vpn evpn instance {evi} {srv_inst}'.format(evi=evi,srv_inst=srv_inst)]

    for conf_command in conf_command_list:
        if srv_inst == "vlan-based":
            if  conf_command == "encapsulation":
                configs.append(f"{conf_command} {encap_type}")
            elif conf_command == "ip":
                configs.append(f"{conf_command} local-learning {mode_type}")
            elif conf_command == "auto-route-target":
                configs.append(f"{conf_command}")
            elif conf_command == "default":
                configs.append(f"{conf_command}")
            elif conf_command == "default-gateway":
                configs.append(f"{conf_command} advertise enable")
            elif conf_command == "exit":
                configs.append(f"{conf_command}")
            elif conf_command == "no":
                configs.append(f"{conf_command} encapsulation")
            elif conf_command == "rd":
                configs.append(f"{conf_command}")
            elif conf_command == "replication-type":
                configs.append(f"{conf_command} ingress")
            elif conf_command == "route-target":
                configs.append(f"{conf_command} import")
    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
           f"Failed to configure evpn instance evi. Error:\n{e}"
        )


def unconfigure_evpn_instance_evi(device, evi, srv_inst):
    """ Unconfigure evpn instance evi
        Args:
            device ('obj'): Device object
            evi ('int'): evi id
            srv_inst ('str'): service instance type
                              vlan-based|vlan-bundle|vlan-aware

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring ' evpn instance ' on evi {evi}".format(evi=evi)
    )

    configs = [
        f'no l2vpn evpn instance {evi} {srv_inst}',
    ]

    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure evpn instance evi .Error:\n{e}"
        )


def configure_evpn_profile(device, name, srv_inst, evi_id=None, l2vni=None, ethernet_tag=None, encap=None):
    """ Configure evpn profile
        Args:
            device ('obj'): Device object
            name ('str'): Name of the evpn profile
            srv_inst ('str'): service instance type
                              vlan-bundle|vlan-aware
            evi_id('int',optional): <1-65535> EVPN evi id, default value is None
            l2vni ('int',optional): <4096-16777215> VxLAN L2VNI base, default value is None
            etherent_tag ('str',optional): EVPN Ethernet Tag, default value is None
                                           auto-vlan | auto-vni
            encap('str',optional): Encapsulation type
                                   vxlan | mpls
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring evpn profile"
    )

    configs = [f'l2vpn evpn profile {name} {srv_inst}'.format(name=name,srv_inst=srv_inst)]

    if evi_id:
        configs.append(f"evi-id {evi_id}")
    if l2vni:
        configs.append(f"l2vni-base {l2vni}")
    if ethernet_tag:
        configs.append(f"ethernet-tag {ethernet_tag}")
    if encap:
        configs.append(f"encapsulation {encap}")
    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
           f"Failed to configure evpn profile. Error:\n{e}"
        )

def unconfigure_evpn_profile(device, name, srv_inst):
    """ Unconfigure evpn profile
        Args:
            device ('obj'): Device object
            name ('str'): Name of the evpn profile
            srv_inst ('str'): service instance type
                              vlan-bundle|vlan-aware
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring evpn profile"
    )

    configs = [f"l2vpn evpn profile {name} {srv_inst}",
               f"no evi-id",
               f"exit",
               f"no l2vpn evpn profile {name} {srv_inst}"
              ]
    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
           f"Failed to unconfigure evpn profile. Error:\n{e}"
        )
def configure_vfi_context_evpn(device, word, id, ethernet_segment=None, value=None, ip_address=None, vc_id=None, encapsulation=None, mpls=None, temp=None, temp_name=None):
    """ Configure vfi context evpn
        Args:
            device ('obj'): Device object
            word('str'): Virtual Forwarding Instance (VFI) name
            id('int'):  VPN id
            ethernet_segment('str'):  Ethernet segment
            value('int'): <1-65535>  Ethernet segment local discriminator value
            ip_address('int',optional): A.B.C.D     IP address of the peer , default value is None
            vc_id('str',optional): <1-4294967295>  Enter VC ID value , default value is None
            encapsulation('str',optional): Data encapsulation method , default value is None
            mpls('str',optional): Use MPLS encapsulation , default value is None
            temp('str',optional): Template to use for encapsulation and protocol configuration , default value is None
            temp_name('str',optional): WORD  template name (Max size 32) , default value is None

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring 'l2vpn vfi context evpn' on vfi {word}".format(word=word)
    )

    configs = [
                f'l2vpn vfi context {word}',
                f'vpn id {id}']

    if ethernet_segment:
        configs.append(f'evpn {ethernet_segment} {value}')
    if vc_id:
        if encapsulation:
               configs.append(f'member {ip_address} {vc_id} {encapsulation} mpls')
        if temp:
               configs.append(f'member {ip_address} {vc_id} {temp} {temp_name}')
    elif encapsulation:
        configs.append(f'member {ip_address} {encapsulation} mpls')
    elif temp:
        configs.append(f'member {ip_address} {temp} {temp_name}')

    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure l2vpn vfi context. Error:\n{e}"
        )


def unconfigure_vfi_context_evpn(device, word):

    """ Unconfigure vfi context evpn
        Args:
            device ('obj'): Device object
            word('str'): Virtual Forwarding Instance (VFI) name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring 'l2vpn vfi context evpn' on vfi {word}".format(word=word)
    )

    configs = [
    f'no l2vpn vfi context {word}'
    ]

    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
           f"Failed to unconfigure l2vpn vfi context evpn. Error:\n{e}"
        )

def configure_l2vpn_evpn_advertise_sync(device, instance=None):

    """ Config multicast advertise sync-only
        Args:
            device ('obj'): Device object
            instance ('int'): instance ID
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    '''Configuring 'multicast advertise sync-only' on l2vpn evpn'''

    configs = ["l2vpn evpn",
               "multicast advertise sync-only"]

    if instance is not None:
        configs.extend([f"l2vpn evpn instance {instance} vlan-based",
                        "multicast advertise sync-only"])

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure 'multicast advertise sync-only' on l2vpn evpn. "
            f"Error: {e}"
        )
