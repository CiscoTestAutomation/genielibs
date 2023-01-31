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
            "Failed to configure IP pim ssm default device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )
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
            "Failed to unconfigure IP pim ssm default device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )
        
