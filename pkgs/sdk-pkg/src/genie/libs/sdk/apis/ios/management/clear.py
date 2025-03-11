"""Clear Idle VTY sessions"""

# Python
import logging

from genie.libs.sdk.apis.iosxe.management.clear import \
    clear_idle_vty_sessions as iosxe_clear_idle_vty_sessions

log = logging.getLogger(__name__)


def clear_idle_vty_sessions(device, idle_timeout=60):
    ''' Execute clear line on idle vty sessions
        Agrs:
            device ('obj'): Device object
            idle_timeout (int, optional): idle session timeout. Defaults to 60
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    return iosxe_clear_idle_vty_sessions(
            device=device,
            idle_timeout=idle_timeout)