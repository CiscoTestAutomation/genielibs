"""Common clear functions for bgp"""

def clear_bgp_neighbor(device, command='clear bgp neighbor all', alternative_command='clear bgp neighbor',
                       fail_regex=None):
    """ Clear bgp neighbor using one of two commands
        Args:
            device ('obj'): Device object
            command ('str'): Command with a higher priority
            alternative_command ('str'): An alternative command that would be executed if the given command creates an error
            fail_regex ('str'): A regex string to look for which would indicate failure

        Returns:
            bool

        Raises:
            N/A or SubcommandFailure
    """

    out = device.api.execute(
            command=command,
            alternative_command=alternative_command,
            fail_regex=fail_regex
        )
    if out is not None:
        return True

    return False

def clear_bgp_neighbor_soft(device, command='clear bgp neighbor soft all', alternative_command='clear bgp neighbor soft',
                       fail_regex=None):
    """ Clear bgp neighbor soft using one of two commands
        Args:
            device ('obj'): Device object
            command ('str'): Command with a higher priority
            alternative_command ('str'): An alternative command that would be executed if the given command creates an error
            fail_regex ('str'): A regex string to look for which would indicate failure

        Returns:
            bool

        Raises:
            N/A or SubcommandFailure
    """

    out = device.api.execute(
            command=command,
            alternative_command=alternative_command,
            fail_regex=fail_regex
        )
    if out is not None:
        return True

    return False    