#python
import logging

#genie
from unicon.core.errors import SubCommandFailure

#unicon
log = logging.getLogger(__name__)

def clear_fqdn_database_all(device):
    """ clear fqdn database all
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear fqdn database on {device}".format(device=device))

    try:
        device.execute("clear fqdn database all")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear fqdn database entries on {device}. Error:\n{error}".format(device=device, error=e)
        )

def clear_fqdn_packet_stats(device):
    """ clear fqdn packet statistics
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear fqdn packet statistics on {device}".format(device=device))

    try:
        device.execute("clear fqdn packet statistics")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear fqdn packet statistics on {device}. Error:\n{error}".format(device=device, error=e)
        )

