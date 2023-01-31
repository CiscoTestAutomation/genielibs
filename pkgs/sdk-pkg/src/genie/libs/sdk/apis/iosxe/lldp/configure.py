"""Common configure functions for lldp"""

# Python
import logging

#Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_lldp(device):
    """ Enables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.configure('lldp run')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP on interface"
            "Error: {error}".format(error=e)
            )

def unconfigure_lldp(device):
    """ Disables lldp on target device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.configure('no lldp run')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP"
            "Error: {error}".format(error=e)
            )

def configure_lldp_interface(device, interface, transmit=True, receive=True):
    """ Configure LLDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which LLDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure LLDP on interface")
    configs = []
    configs.append("lldp run")
    configs.append(f"interface {interface}")
    if transmit:
        configs.append("lldp transmit")
    if receive:
        configs.append("lldp receive")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP on interface"
            "Error: {error}".format(error=e)
            )

def unconfigure_lldp_interface(device, interface, transmit=True, receive=True):
    """ Unconfigure LLDP on interface

        Args:
            device ('obj'): Device object
            interface ('str'): interface on which LLDP to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure LLDP on interface")
    configs = []
    configs.append("no lldp run")
    configs.append(f"interface {interface}")
    if transmit:
        configs.append("no lldp transmit")
    if receive:
        configs.append("no lldp receive")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP on interface"
            "Error: {error}".format(error=e)
            )

def configure_lldp_holdtime(device, timer):
    """ Configure LLDP holdtime on target device globally on the device
        Args:
            device ('obj'): Device object
            timer ('int'): LLDP holdtime in seconds between 0-65535 seconds
        Returns:
            None
    """
    try:
        device.configure(f'lldp holdtime {timer}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP holdime"
            "Error: {error}".format(error=e)
        )

def unconfigure_lldp_holdtime(device):
    """ Disable LLDP holdtime on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    try:
        device.configure('no lldp holdtime')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP holdtime"
            "Error: {error}".format(error=e)
        )

def configure_lldp_timer(device, timer):
    """ Configure LLDP timer on target device globally on the device
        Args:
            device ('obj'): Device object
            timer ('int'): LLDP timer in seconds between 5-65534 seconds
        Returns:
            None
    """
    try:
        device.configure(f'lldp timer {timer}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP timer"
            "Error: {error}".format(error=e)
        )

def unconfigure_lldp_timer(device):
    """ Disable LLDP timer on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    try:
        device.configure('no lldp timer')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP timer"
            "Error: {error}".format(error=e)
        )

def configure_lldp_reinit(device, timer):
    """ Configure LLDP reinit on target device globally on the device
        Args:
            device ('obj'): Device object
            timer ('int'): LLDP reinit in seconds between 2-5 seconds
        Returns:
            None
    """
    try:
        device.configure(f'lldp reinit {timer}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP reinit"
            "Error: {error}".format(error=e)
        )

def unconfigure_lldp_reinit(device):
    """ Disable LLDP reinit on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """ 
    try:
        device.configure('no lldp reinit')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP reinit"
            "Error: {error}".format(error=e)
        )

def clear_lldp_counters(device):
    """ Clear LLDP counters on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.execute('clear lldp counters')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear LLDP counters"
            "Error: {error}".format(error=e)
        )

def clear_lldp_table(device):
    """ Clear LLDP table on target device globally on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    """
    try:
        device.execute('clear lldp table')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear LLDP table"
            "Error: {error}".format(error=e)
        )

def configure_lldp_tlv_select(device, tlv):
    """ Configure LLDP tlv-select on target device globally on the device
        Args:
            device ('obj'): Device object
            tlv ('list'/'str'): List of TLVs if multiple TLVs to select or a string.
        Returns:
            None
    """
    configs = [f'lldp tlv-select {each_tlv}' for each_tlv in tlv] if isinstance(tlv, list) else [f'lldp tlv-select {tlv}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure LLDP tlv-select"
            "Error: {error}".format(error=e)
        )

def unconfigure_lldp_tlv_select(device, tlv):
    """ Disable LLDP tlv-select on target device globally on the device
        Args:
            device ('obj'): Device object
            tlv ('list'/'str'): List of TLVs if multiple TLVs to unselect or a string.
        Returns:
            None
    """
    configs = [f'no lldp tlv-select {each_tlv}' for each_tlv in tlv] if isinstance(tlv, list) else [f'no lldp tlv-select {tlv}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure LLDP tlv-select"
            "Error: {error}".format(error=e)
        )
