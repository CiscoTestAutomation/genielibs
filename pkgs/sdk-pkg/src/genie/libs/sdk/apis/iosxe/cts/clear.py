# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure
# Logger
log = logging.getLogger(__name__)

def clear_sxp_filter_counters(device):
    """ clear cts sxp filter-counters
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('clear cts sxp filter-counters')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear cts sxp filter-counters on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
 
