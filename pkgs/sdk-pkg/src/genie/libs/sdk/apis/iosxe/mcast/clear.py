# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


# Logger

log = logging.getLogger(__name__)

def clear_ip_mroute_vrf(device, vrf_name):
    """ clear ipv6 mld group
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.execute('clear ip mroute vrf {vrf_name} *'.format(vrf_name=vrf_name))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear ip mroute vrf on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
