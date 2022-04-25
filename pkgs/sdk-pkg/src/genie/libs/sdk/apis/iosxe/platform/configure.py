'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_no_boot_manual(device):
    """ no boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove boot manual config on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_boot_manual(device):
    """ boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config boot manual on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_ip_local_pool(device,name,start,end):
    """ ip local pool
        Args:
            device (`obj`): Device object
            name ('str') : pool name
            start ('str') : pool start ip
            end ('str') : pool end ip
        
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f'ip local pool {name} {start} {end}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local pool on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_bba_group(device,name,vt_number):
    """ bba-group
        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cli = []
    cli.append(f"bba-group pppoe {name}")
    cli.append(f"virtual-template {vt_number}")
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config bba-group on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_bba_group(device,name,vt_number):
    """ bba-group
        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    cli = []
    cli.append(f"no bba-group pppoe {name}")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfig bba-group on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

