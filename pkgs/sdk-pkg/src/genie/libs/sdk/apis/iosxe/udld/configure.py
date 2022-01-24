"""Common configure functions for udld"""

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_udld_alert_mode(device, interface):
    """ Configures UDLD alert mode on Interface 
        Args:
            device (`obj`): Device object
            interface (`str`): interface
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    try:
        output = device.configure([
                         f"interface {interface}", 
                         "udld port alert"
                         ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure udld alert on {interface}, Error: {error}'.format(
                interface=interface, error=e))
    return output
        
def configure_udld(device, interface):
    """ Configures UDLD on Interface 
    Args:
        device (`obj`): Device object
        interface (`str`): interface
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring interface
    """
    try:
        output = device.configure([
                         f"interface {interface}",
                         "udld port"
                        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
        'Could not configure udld on {interface}, Error: {error}'.format(
            interface=interface, error=e))
    return output