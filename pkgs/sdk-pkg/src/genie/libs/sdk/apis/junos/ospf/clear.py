"""Common clear functions for ospf"""

def clear_ospf_neighbor(device, command='clear ospf neighbor all', alternative_command='clear ospf neighbor'):
    """ Clear ospf neighbor using one of two commands
        Args:
            device ('obj'): Device object
            command ('str'): Command with a higher priority
            alternative_command ('str'): An alternative command that would be executed if the given command creates an error

        Returns:
            bool

        Raises:
            N/A or SubcommandFailure
    """
    out = device.api.execute(
            command=command,
            alternative_command=alternative_command
        )
    if out is not None:
        return True

    return False