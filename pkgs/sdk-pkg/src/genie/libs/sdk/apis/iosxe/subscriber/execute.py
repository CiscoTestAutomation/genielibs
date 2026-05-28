"""Common execute functions for subscriber"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_show_subscriber_session_feature(device, feature):
    """ Execute show subscriber session feature on device

        Args:
            device (`obj`): Device object
            feature (`str`): Feature name (e.g. 'l4redirect', 'policing',
                'qos-peruser', 'session-timer')
        Returns:
            output (`str`): Output of execution
        Raises:
            SubCommandFailure
    """
    try:
        output = device.execute(
            f"show subscriber session feature {feature}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute show subscriber session feature {feature}. "
            f"Error: {e}"
        )

    return output
