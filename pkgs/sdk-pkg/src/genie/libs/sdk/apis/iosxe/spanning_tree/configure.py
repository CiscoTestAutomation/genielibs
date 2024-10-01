''' Common Config functions for IOX / app-hosting '''

import logging
from sqlite3 import IntegrityError
import time

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout

def configure_spanning_tree(device, vlan_range='1-4093'):
    """
    Configures spanning-tree vlan with input vlan or vlan range
    e.g.
    spanning-tree vlan 666
    spanning-tree vlan 1-999
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
    Returns:
        None
    """

    try:
        output = device.configure("spanning-tree vlan {vlan}".format(vlan=vlan_range))
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree - Error:\n{error}".format(error=e)
        )

def unconfigure_spanning_tree(device, vlan_range='1-4093'):
    """ 
    UnConfigures spanning-tree vlan with input vlan or vlan range
    e.g.
    no spanning-tree vlan 666
    no spanning-tree vlan 1-999
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
    Returns:
        None
    """

    try:
        output = device.configure("no spanning-tree vlan {vlan}".format(vlan=vlan_range))
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure Spanning Tree - Error:\n{error}".format(error=e)
        )


def configure_spanning_tree_priority(device, vlan, priority):
    """
    Configures spanning-tree vlan with priority
    e.g.
    spanning-tree vlan 666 priority 4096
    Args:
        device ('obj') : Device object
        vlan ('str'): vlan
        priority ('int'): priority to be configured

    Returns:
        None
        
    Raise:
        SubCommandFailure: Failed configuring spanning-tree vlan with priority
    """

    try:
        output = device.configure(f"spanning-tree vlan {vlan} priority {priority}")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree with priority- Error:\n{error}".format(error=e)
        )


def unconfigure_spanning_tree_priority(device, vlan, priority=None):
    """
    Unconfigures spanning-tree vlan with priority
    e.g.
    no spanning-tree vlan 666 priority 4096
    Args:
        device ('obj') : Device object
        vlan ('str'): vlan
        priority ('int', optional): priority to be configured(Default None)

    Returns:
        None
        
    Raise:
        SubCommandFailure: Failed unconfiguring spanning-tree vlan with priority
    """
    command = f"no spanning-tree vlan {vlan} priority {priority}" if priority else f"no spanning-tree vlan {vlan} priority"
    try:
        output = device.configure(command)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Spanning Tree with priority- Error:\n{error}".format(error=e)
        )
        
def configure_spanning_tree_mode(device, mode, system_id=None):
    """
    Configures spanning-tree mode
    Args:
        device ('obj') : Device object
        mode ('str'): configure the spanning tree mode
        system_id('str',optinal): provide the system_id
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring spanning-tree mode
    """
    config = []
    config.append('spanning-tree mode {mode}'.format(mode=mode))
    if system_id:
        config.append('spanning-tree {system_id}'.format(system_id=system_id))
    try:
        device.configure(config)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree mode - Error:\n{error}".format(error=e)
        )
        
def unconfigure_spanning_tree_mode(device):
    """
    Unconfigures spanning-tree mode
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raises:
        SubCommandFailure: Failed unconfigure_spanning_tree mode
    """
    config = 'no spanning-tree mode'
    try:
        device.configure(config)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Spanning Tree mode - Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_mst_configuration(device, instance, vlan_id, mappedvlan_id=None):
    """
    Configure spanning-tree configuration with vlan mappings
    Args:
        device ('obj') : Device object
        instance (int): instance details
        vlan_id (int): vlanid details
        mappedvlan_id (int, optional): mapped vlanid details
    Returns:
        None
    Raise:
        SubCommandFailure: Failed to configure the spanning-tree mst configuration
    """
    log.info(
        "configuring the spanning tree mst configuration on {device}".format(device=device)
    )
    config = []
    config.append("spanning-tree mst configuration")
    if mappedvlan_id:
        config.append("instance {instance} vlan {vlan_id}, {mappedvlan_id}".format(instance=instance, vlan_id=vlan_id, mappedvlan_id=mappedvlan_id))
    else:
        config.append("instance {instance} vlan {vlan_id}".format(instance=instance, vlan_id=vlan_id))
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the spanning tree mst configuration on {device} "
            .format(device=device, e=e)
        )

def unconfigure_spanning_tree_mst_configuration(device):
    """
    Unconfigure spanning-tree mst configuration
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raise:
        SubCommandFailure: Failed to unconfigure the spanning-tree mst configuration
    """
    log.info(
        "unconfiguring the spanning tree mst configuration on {device}".format(device=device)
    )
    config = [
                'no spanning-tree mst configuration',
            ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure the spanning tree mst configuration on {device} "
            .format(device=device, e=e)
        )


def configure_spanning_tree_guard_loop(device, interface):

    """ Enable spanning-tree guard loop over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): enable spanning-tree guard loop on this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree guard loop"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable the spanning-tree guard loop. Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_guard_root(device, interface):

    """ Enable spanning-tree guard root over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): enable spanning-tree guard root on this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree guard root"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable the spanning-tree guard root. Error:\n{error}".format(error=e)
        )


def unconfigure_spanning_tree_guard_root(device, interface):

    """ Disable spanning-tree guard root over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): disable spanning-tree guard root over this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"no spanning-tree guard root"
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable the spanning-tree guard root. Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_portfast(device, default=False, bpduguard=False, bpdufilter=False):
    """ Configures Spanning Tree Portfast
        Args:
            device ('obj')    : device to use
            default ('boolean', optional) : Options are True/False. Default is False
            bpdugaurd ('boolean',optional) : Options are True/Flase. Default is False
            bpdufilter ('boolean', optional) : Options are True/False. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "spanning-tree portfast "
    if bpduguard:
        config += "bpduguard default" if default else "bpduguard"
    elif bpdufilter:
        config += "bpdufilter default"
    elif default:
        config += "default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree portfast - Error:\n{error}'
        )

def unconfigure_spanning_tree_portfast(device, default=False, bpduguard=False, bpdufilter=False):
    """ Unconfigures Spanning Tree Portfast
        Args:
            device ('obj')    : device to use
            default ('boolean', optional) : Options are True/False. Default is False
            bpdugaurd ('boolean',optional) : Options are True/Flase. Default is False
            bpdufilter ('boolean', optional) : Options are True/False. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "no spanning-tree portfast "
    if bpduguard:
        config += "bpduguard default" if default else "bpduguard"
    elif bpdufilter:
        config += "bpdufilter default"
    elif default:
        config += "default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree portfast - Error:\n{error}'
        )

def unconfigure_spanning_tree_guard_loop(device, interface):

    """ Disable spanning-tree guard loop over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): disable spanning-tree guard loop over this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"no spanning-tree guard loop"
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable the spanning-tree guard loop. Error:\n{error}".format(error=e)
        )


def configure_spanning_tree_uplinkfast(device, max_rate=int()):
    """ Configures Spanning Tree Uplinkfast
        Args:
            device ('obj')    : device to use
            max_rate ('int', optional) : Options are 0-32000. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "spanning-tree uplinkfast"
    if max_rate:
        config += f" max-update-rate {max_rate}"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree uplinkfast - Error:\n{error}'
        )

def configure_spanning_tree_bpdufilter(device, interface):

    """ Enable spanning-tree bpdufilter over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): enable spanning-tree bpdufilter on this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree bpdufilter enable"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable the spanning-tree bpdufilter. Error:\n{error}".format(error=e)
        )

def unconfigure_spanning_tree_uplinkfast(device, max_rate=int()):
    """ Unconfigures Spanning Tree Uplinkfast
        Args:
            device ('obj')    : device to use
            max_rate ('int', optional) : Options are 0-32000. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "no spanning-tree uplinkfast"
    if max_rate:
        config += f" max-update-rate"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree uplinkfast - Error:\n{error}'
        )


def unconfigure_spanning_tree_bpdufilter(device, interface):

    """ Disable spanning-tree bpdufilter over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): disable spanning-tree bpdufilter over this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"no spanning-tree bpdufilter"
          ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable the spanning-tree bpdufilter. Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_backbonefast(device):
    """ Configures Spanning Tree Backbonefast
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure("spanning-tree backbonefast")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree backbonefast - Error:\n{error}'
        )

def unconfigure_spanning_tree_backbonefast(device):
    """ Unconfigures Spanning Tree Backbonefast
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no spanning-tree backbonefast")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree backbonefast - Error:\n{error}'
        )

def configure_spanning_tree_portfast_default(device):
    """ Configures Spanning Tree portfast default
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure("spanning-tree portfast default")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree portfast default - Error:\n{error}'
        )

def configure_spanning_tree_vlan_root(device, vlan_range, mode, diameter=int()):
    """ 
    Configures spanning-tree vlan root with input vlan or vlan range
    e.g.
    spanning-tree vlan 666 root primary
    spanning-tree vlan 1-999 root secondary diameter 4
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
        mode ('str'): primary or secondary 
        diameter ('int', optional): Network diameter of this spanning tree. (Default is None)
    Returns:
        None
    """
    config = f"spanning-tree vlan {vlan_range} root {mode}"
    if diameter:
        config += f" diameter {diameter}"
    try:
        device.configure(config)
        
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not Configure Spanning Tree Vlan Root.- Error:\n{error}"
        )

def unconfigure_spanning_tree_vlan_root(device, vlan_range):
    """ 
    Unconfigures spanning-tree vlan root with input vlan or vlan range
    e.g.
    no spanning-tree vlan 666 root
    no spanning-tree vlan 1-999 root
    Args:
        device ('obj') : Device object
        vlan_range ('str'): vlan or vlan range
    Returns:
        None
    """

    try:
        device.configure(f"no spanning-tree vlan {vlan_range} root")
        
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not Unconfigure Spanning Tree Vlan Root.- Error:\n{error}"
        )

def configure_spanning_tree_bpdufilter_disable(device, interface):

    """ Disable spanning-tree bpdufilter over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): Disable spanning-tree bpdufilter on this interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree bpdufilter disable"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable the spanning-tree bpdufilter. Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_bpdugaurd(device, interface, option):

    """ Configure spanning-tree bpdugaurd over interface 
        Args:
            device ('obj'): device to use
            interface ('str'): spanning-tree bpdufilter on this interface
            option('str'): enable/disable
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree bpduguard {option}"           
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the spanning-tree bpdugaurd enable/diable. Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_mst_configuration_name(device, name):
    """
    Configure spanning-tree configuration with configuration name
    Args:
        device ('obj') : Device object
        name ('str') : configuration name
    Returns:
        None
    Raise:
        SubCommandFailure
    """
    log.info(
        "configuring the spanning tree mst configuration name "
    )
    config = [
        "spanning-tree mst configuration",
        f"name {name}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the spanning tree mst configuration name on {device} "
            .format(device=device, e=e)
        )

def configure_spanning_tree_mst_configuration_revision(device, rev_num):

    """
    Configure spanning-tree configuration with revision
    Args:
        device ('obj') : Device object
        rev_num ('int') : Configuration revision number
    Returns:
        None
    Raise:
        SubCommandFailure
    """
    log.info(
        "configuring the spanning tree mst configuration revision "
    )
    config = [
        "spanning-tree mst configuration",
        f"revision {rev_num}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the spanning tree mst configuration revision on {device} "
            .format(device=device, e=e)
        )

def configure_default_spanning_tree(device, spanning_tree, mst="", portfast="", range=""):
    """ Configure spanning-tree mode mst
        Args:
            device ('obj'): Device object]
            spanning_tree ('str'): spanning tree 
            mst ('str'): instance range, example: 0-3,5,7-9
            portfast ('str'): enable portfast
            range ('str'): vlan range, example: 1,3-5,7,9-11
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if spanning_tree == "bridge":
        cmd = f"default spanning-tree {spanning_tree} assurance" 
    if spanning_tree == "etherchannel":
        cmd = f"default spanning-tree {spanning_tree} guard misconfig" 
    if spanning_tree == "extend":
        cmd = f"default spanning-tree {spanning_tree} system-id" 
    if spanning_tree == "mst":
        cmd = f"default spanning-tree {spanning_tree} {mst}" 
    if spanning_tree == "pathcost":
        cmd = f"default spanning-tree {spanning_tree} method" 
    if spanning_tree == "portfast":
        cmd = f"default spanning-tree {spanning_tree} {portfast}" 
    if spanning_tree == "sso":
        cmd = f"default spanning-tree {spanning_tree} block-tcn" 
    if spanning_tree == "transmit":
        cmd = f"default spanning-tree {spanning_tree} hold-count" 
    if spanning_tree == "uplinkfast":
        cmd = f"default spanning-tree {spanning_tree} max-update-rate" 
    if spanning_tree == "vlan":
        cmd = f"default spanning-tree {spanning_tree} {range}" 
    else:
        cmd = f"default spanning-tree {spanning_tree}" 

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure spanning-tree mode mst on device. Error:\n{e}") 

def configure_spanningtree_sso_block_tcn(device):
    """ 
    Configure spanning-tree sso block-tcn
    Args:
        device ('obj') : Device object
    Returns:
        None
    """
    cmd = [f"spanning-tree sso block-tcn"]
    try:
        device.configure(cmd) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure spanning-tree sso block-tcn on {device}. Error:\n{error}".format(device=device, error=e)
        )

def configure_spanningtree_cost_on_interface(device, interface, path_cost):
    """ 
    Configures spanning-tree cost
    Args:
        device ('obj') : Device object
        interface ('str') : interface name
        path_cost('str') :  In between 1-200000000
    Returns:
        None
    """
    cmd = [f"interface {interface}", "spanning-tree cost {path_cost}".format(path_cost=path_cost)]
    try:
        device.configure(cmd) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure spanning-tree cost on {device}. Error:\n{error}".format(device=device, error=e)
        )

def unconfigure_spanningtree_cost_on_interface(device, interface, path_cost):
    """
    Unconfigures spanning-tree cost
    Args:
        device ('obj') : Device object
        interface ('str') : interface name
        path_cost('str') : In between 1-200000000
    Returns:
        None
    """
    cmd = [f"interface {interface}", "no spanning-tree cost {path_cost}".format(path_cost=path_cost)]
    try:
        device.configure(cmd) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure spanning-tree sso block-tcn on {device}. Error:\n{error}".format(device=device, error=e)
        )

def unconfigure_spanningtree_sso_block_tcn(device):
    """ 
    Unconfigure spanning-tree sso block-tcn
    Args:
        device ('obj') : Device object
    Returns:
        None
    """
    cmd = [f"no spanning-tree sso block-tcn"]
    try:
        device.configure(cmd) 
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure spanning-tree cost on {device}. Error:\n{error}".format(device=device, error=e)
        )

def configure_default_spanning_tree_mode(device):
    '''Configures default spanning-tree mode
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring default spanning-tree mode
    '''
    config = 'default spanning-tree mode'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed configuring default spanning-tree mode. Error:\n{e}")

def configure_spanning_tree_portfast_on_interface(device, interface, option=None):
    """ Configures Spanning Tree Portfast on interface
        Args:
            device ('obj'): device to use
            interface('str'): configure the interface
            option('str', optional): configure the portfast edge / disable / network /trunk
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}"]
    if option:
        config.append(f'spanning-tree portfast {option}')
    else:
        config.append('spanning-tree portfast')
 
    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree portfast - Error:\n{error}'
        )

def unconfigure_spanning_tree_etherchannel_misconfig(device):
    '''Unconfigures spanning tree etherchannel misconfig
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure spanning tree etherchannel misconfig
    '''
    config = 'no spanning-tree etherchannel guard misconfig'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure spanning tree etherchannel misconfig.Error:\n{e}")

def configure_spanning_tree_etherchannel_misconfig(device):
    '''configures spanning tree etherchannel misconfig
    Args:
        device ('obj') : Device object
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure spanning tree etherchannel misconfig
    '''
    config = 'spanning-tree etherchannel guard misconfig'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure spanning tree etherchannel misconfig.Error:\n{e}")

def configure_spanning_tree_mst_priority(device, instance_range, priority_id):
    '''configure spanning-tree mst 0 priority 4096
    Args:
        device ('obj') : Device object
        instance_range('int') : MST instance range, example: 0-3,5,7-9
        range('int') : <0-61440>  bridge priority in increments of 4096
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configures spanning-tree mst 0 priority 4096
    '''
    config = [f'spanning-tree mst {instance_range} priority {priority_id}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure configures spanning-tree mst 0 priority 4096.Error:\n{e}")


def unconfigure_spanning_tree_portfast_on_interface(device, interface, option=None):
    """ UnConfigures Spanning Tree Portfast on interface
        Args:
            device ('obj'): device to use
            interface('str'): Unconfigure on the interface
            option('str', optional): configure the portfast edge / disable / network /trunk
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"interface {interface}"]
    if option:
        config.append(f'no spanning-tree portfast {option}')
    else:
        config.append('no spanning-tree portfast')

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree portfast - Error:\n{error}'
        )


def configure_default_spanning_tree_vlan(device, vlan_range, option_type=None):
    """ Configure default spanning-tree vlan {vlan_range}
        Args:
            device ('obj'): Device object]
            vlan_range ('str'): vlan range, example: 1,3-5,7,9-11
            option_type ('str'): optional attribute, example: 'forward-time', 'hello-time', 'max-age'. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"default spanning-tree vlan {vlan_range}{f' {option_type}' if option_type else ''}" 

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure spanning-tree mode mst on device. Error:\n{e}")

def configure_spanning_tree_bridge_assurance(device):
    """
    Configures spanning-tree Bridge Assurance
    Args:
        device ('obj') : Device object
    Returns:
        None
    """

    try:
        output = device.configure("spanning-tree bridge assurance")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Configure Spanning Tree Bridge Assurance - Error:\n{error}".format(error=e)
        )

def unconfigure_spanning_tree_bridge_assurance(device):
    """ 
    UnConfigures spanning-tree Bridge assurance
    Args:
        device ('obj') : Device object
    Returns:
        None
    """
    try:
        output = device.configure("no spanning-tree bridge assurance")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not UnConfigure Spanning Tree Bridge Assurance - Error:\n{error}".format(error=e)
        )

def configure_spanning_tree_portfast_bridge_assurance(device, option):
    """ Configures Spanning Tree Portfast_bridge_assurance
        Args:
            device ('obj')    : device to use
            option ('str'): normal / edge / network / edge bpduguard / edge bpdufilter
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "spanning-tree portfast "
    if option:
        config += f" {option} default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not configure spanning-tree portfast bridge assurance - Error:\n{error}'
        )

def unconfigure_spanning_tree_portfast_bridge_assurance(device, option):
    """ Unconfigures Spanning Tree Portfast
        Args:
            device ('obj')    : device to use
            option ('str'): normal / edge / network / edge bpduguard / edge bpdufilter
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "no spanning-tree portfast "
    if option:
        config += f" {option} default"

    try:
        device.configure(config)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Could not unconfigure spanning-tree portfast bridge assurance - Error:\n{error}'
        )

def configure_spanning_tree_portfast_bridge_assurance_on_interface(device, interface, option):
    """ Configures Spanning Tree Portfast bridge assurance on interface
        Args:
            device ('obj')    : device to use
            interface ('str'): enable spanning-tree portfast bridge assurance on this interface
            option('str'): edge trunk/network
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"spanning-tree portfast {option}"
          ]  

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure the spanning-tree portfast bridge assurance on interface Error:\n{error}".format(error=e)
        )

def unconfigure_spanning_tree_portfast_bridge_assurance_on_interface(device, interface, option):
    """ Unconfigures Spanning Tree Portfast bridge assurance on interface
        Args:
            device ('obj')    : device to use
            interface ('str'): enable spanning-tree portfast bridge assurance on this interface
            option('str'): edge trunk/network
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
                f"interface {interface}",
                f"no spanning-tree portfast {option}"
          ]  
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure the spanning-tree portfast bridge assurance on interface Error:\n{error}".format(error=e)
        )

