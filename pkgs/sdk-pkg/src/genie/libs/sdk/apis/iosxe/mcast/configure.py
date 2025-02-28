"""Common configure functions for ip multicast routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs.sdk.apis.utils import tftp_config

log = logging.getLogger(__name__)

def configure_ip_multicast_routing(device):
    
    """ configure ip multicast routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing. Error {e}".format(e=e)
        )

def unconfigure_ip_multicast_routing(device):

    """Unconfigure ip multicast routing on device

        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing. Error {e}".format(e=e)
        )

def configure_ip_multicast_routing_distributed(device):
    """ configure ip multicast routing on device
        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing distributed")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing. Error {e}".format(e=e)
        )
        
def unconfigure_ip_multicast_routing_distributed(device):
    """Unconfigure ip multicast routing on device
        Args:
            device (`obj`): Device object
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing distributed")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing. Error {e}".format(e=e)
        )
        
def configure_ip_multicast_vrf_routing(device, vrf_name):

    """ configure ip multicast routing vrf on device
        Example : 

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf 
        Returns:
            None
    """
    try:
        device.configure("ip multicast-routing vrf {}".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Configure ip multicast-routing vrf vrf_name. Error {e}".format(e=e)
        )

def unconfigure_ip_multicast_vrf_routing(device, vrf_name):

    """Unconfigure ip multicast routing vrf on device
        Example : 

        Args:
            device (`obj`): Device object
            vrf_name('str'): name of the vrf 
        Returns:
            None
    """
    try:
        device.configure("no ip multicast-routing vrf {}".format(vrf_name))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            "Unconfigure ip multicast-routing vrf Error {e}".format(e=e)
        )


def configure_scale_ip_multicast_vrf_distribute_tftp(device,
                                                     server,
                                                     vrf_name,
                                                     vrf_name_step,
                                                     vrf_count,
                                                     unconfig=False,
                                                     tftp=False):
    """ configure ip multicast-routing vrf distributed on device
        Example :
        ip multicast-routing vrf 2 distributed
        ip multicast-routing vrf 3 distributed

        Args:
            device ('obj'): Device to use
            server ('str'): Testbed.servers
            vrf_name ('int'): Start of vrf name. eg. 100
            vrf_name_step ('int'): Size of vlan range step
            vrf_count ('int'): How many vrfs
            unconfig ('bool'): Unconfig or not
            tftp ('bool'): Tftp config or not
        Returns:
            None
            cmds_block str if not tftp configure
    """
    cmds = ''
    if unconfig:
        no_str = 'no'
    else:
        no_str = ''

    for count in range(vrf_count):
        cmds += '''
        {no_str} ip multicast-routing vrf {vrf} distributed
        '''.format(no_str=no_str, vrf=vrf_name)

        vrf_name += vrf_name_step

    if tftp:
        try:
            tftp_config(device, server, cmds)
        except Exception:
            raise Exception('tftp_config failed.')
    else:
        return cmds


def configure_interface_pim(device,interface,pim_mode):

    """ Configure pim in interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            pim_mode (`str`): PIM mode (sparse-mode | sparse-dense-mode)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append("ip pim {mode}".format(mode=pim_mode))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure PIM mode {mode} on  interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                mode=pim_mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_interface_pim(device,interface,pim_mode):

    """ unconfigure pim in interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            pim_mode (`str`): PIM mode (sparse-mode | sparse-dense-mode)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append("no ip pim {mode}".format(mode=pim_mode))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure PIM mode {mode} on  interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                mode=pim_mode,
                interface=interface,
                dev=device.name,
                error=e,
            )
        )

def configure_pim_ssm_default(device):

    """ Configure PIM SSM Default
    Example : ip pim ssm default

        Args:
            device ('obj'): Device object
           
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    
    configs = f"ip pim ssm default"
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure IP PIM SSM default on device {device.name}. Error:\n{e}")

def unconfigure_pim_ssm_default(device):

    """ Unconfigure PIM SSM Default
    Example : no ip pim ssm default

        Args:
            device ('obj'): Device object
           
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    
    configs = f"no ip pim ssm default"
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure IP PIM SSM default on device {device.name}. Error:\n{e}")
        
def configure_pim_vrf_ssm_default(device, vrf):

    """ Configure PIM SSM Default
    Example : ip pim vrf <> ssm default

        Args:
            device ('obj'): Device object
            vrf (`str`): name of the vrf
           
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    
    configs = f"ip pim vrf {vrf} ssm default"
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure IP pim vrf {vrf} ssm default device {device.name}. Error:\n{e}')

def unconfigure_pim_vrf_ssm_default(device, vrf):

    """ Unconfigure PIM SSM Default
    Example : no ip pim vrf <> ssm default

        Args:
            device ('obj'): Device object
            vrf (`str`): name of the vrf
           
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    
    configs = f"no ip pim vrf {vrf} ssm default"
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure IP pim vrf {vrf} ssm default device {device.name}. Error:\n{e}')

def configure_pim_autorp_listener(device, vrf, intf=None, ttl=None, announce=True, discovery=True):
    
    """ Config pim autorp listener
        Args:
            device ('obj'): Device object
            intf ('str'): Name of the interface
            vrf ('str'): Name of the vrf
            ttl ('int'): TTL value
            announce ('bool'): True or False
            discovery ('bool'): True or False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''
    Configuring ip pim vrf <vrf> autorp listener
    ip pim vrf red send-rp-discovery scope <ttl>
    ip pim vrf red send-rp-announce <intf> scope <ttl>
    '''
     
    configs = [f"ip pim vrf {vrf} autorp listener"]
               
    if discovery and ttl:
        configs.append(f"ip pim vrf {vrf} send-rp-discovery scope {ttl}")
                       
    if announce and intf and ttl:
        configs.append(f"ip pim vrf {vrf} send-rp-announce {intf} scope {ttl}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure pim autorp listener. Error:{e}")

def unconfigure_pim_autorp_listener(device, vrf, intf=None, ttl=None, announce=True, discovery=True):
    
    """ Unconfig multicast advertise sync-only
        Args:
            device ('obj'): Device object
            intf ('str'): Name of the interface
            vrf ('str'): Name of the vrf
            ttl ('int'): TTL value
            announce ('bool'): True or False
            discovery ('bool'): True or False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''
    Unconfiguring no ip pim vrf <vrf> autorp listener
    no ip pim vrf red send-rp-discovery scope <ttl>
    no ip pim vrf red send-rp-announce <intf> scope <ttl>
    '''
     
    configs = [f"no ip pim vrf {vrf} autorp listener"]
               
    if discovery and ttl:
        configs.append(f"no ip pim vrf {vrf} send-rp-discovery scope {ttl}")
                       
    if announce and intf and ttl:
        configs.append(f"no ip pim vrf {vrf} send-rp-announce {intf} scope {ttl}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure pim autorp listener. Error:{e}")

def configure_ip_pim_vrf_ssm_range(device, vrf, acl_name):

    """ Configures ip pim vrf <vrf> ssm range
        Args:
            device ('obj')    : device to use
            vrf ('str')  : Name of the vrf
            acl_name ('str') : Name of the acl
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip pim vrf {vrf} ssm range {acl_name}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configures ip pim vrf {vrf} ssm range. Error: {e}')

def unconfigure_ip_pim_vrf_ssm_range(device, vrf, acl_name):

    """ Unconfigures ip pim vrf <vrf> ssm range
        Args:
            device ('obj')    : device to use
            vrf ('str')  : Name of the vrf
            acl_name ('str') : Name of the acl
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no ip pim vrf {vrf} ssm range {acl_name}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigures ip pim vrf {vrf} ssm range. Error: {e}')
    
def configure_pim_auto_rp_listener(device, loopback_number=None, ttl=None, announce=True, discovery=True):
    
    """ Config pim autorp listener
        Args:
            device ('obj'): Device object
            loopback_number ('int') : Loopback number
            ttl ('int'): TTL value
            announce ('bool'): True or False
            discovery ('bool'): True or False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
  
    '''
    Configuring ip pim autorp listener
    ip pim  send-rp-announce loopback {ttl} scope {ttl}
    ip pim  send-rp-discovery loopback {ttl} scope {ttl}
    '''
    configs = [f"ip pim autorp listener"]
               
    if discovery and loopback_number and ttl:
        configs.append(f"ip pim  send-rp-announce loopback {loopback_number} scope {ttl}")
                       
    if announce and loopback_number and ttl:
        configs.append(f"ip pim  send-rp-discovery loopback {loopback_number} scope {ttl}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure pim autorp listener. Error:{e}")