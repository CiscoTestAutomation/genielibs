"""Common configure functions for flow monitor sampler fnf_sampler"""

# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_flow_monitor_sampler_fnf_sampler(device, protocol_type, name, flow, interface=None, interface_range=None):
    """ configure flow monitor sampler fnf sampler
        Args:
            device ('obj'): Device object
            protocol_type ('str'): protocols (Ex : ipv4,ipv6,datalink)
            name ('str'): Flow Monitor Name
            flow ('str'): Flow direction (Ex : Input or Output)
            interface ('str'): Interface to be configured on
            interface_range ('str'): Interfaces to be configured on

        Returns:
            None 
        
        Raises: 
            SubCommandFailure
    """
    log.debug("{protocol_type} flow monitor {name} sampler fnf_sampler {flow}")

    cmd = []

    if not any([interface, interface_range]):
        raise ValueError('Interface and Interface Range Both are Unavailable')
    
    if interface:
        cmd.append(f"interface {interface}")

    elif interface_range:
        cmd.append(f"interface range {interface_range}")  
        
    cmd.append(f"{protocol_type} flow monitor {name} sampler fnf_sampler {flow}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure flow monitor sampler fnf sampler. Error:\n{error}".format(error=e)
        )