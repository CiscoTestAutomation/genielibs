import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def execute_clear_zone_pair(device, subcommand):
    """clear zone-pair {subcommand}
        Args:
            device ('obj'): Device object
            subcommand('str'): subcommand to clear zone-pair {subcommand} eg inspect session, counter
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"clear zone-pair {subcommand}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear zone-pair {subcommand} on device")