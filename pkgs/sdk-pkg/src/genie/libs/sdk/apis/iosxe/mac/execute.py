'''IOSXE execute functions for mac'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def monitor_event_trace_clear(device, trace_type, category):
    """ Clears ip arp inspection
        Args:
            device (`obj`): Device object
            trace_type (`str`):  protocaltracetype
            category(`str`): trace category critical or events or errors or allevents 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"monitor event-trace {trace_type} {category} clear"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to clear event trace  {device} . Error:\n{e}")
            