"""Common clear functions for ospf3"""

def clear_ospf3_neighbor(device, command='clear ospf3 neighbor all', alternative_command='clear ospf3 neighbor',fail_regex=None):
    """ Clear ospf3 neighbor using one of two commands
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