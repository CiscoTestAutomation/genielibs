# Python
# Unicon
from unicon.core.errors import SubCommandFailure

def clear_ptp_corrections(device):
    """ clear ptp corrections
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('clear ptp corrections')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ptp corrections  on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )