'''Default implementation of InitExecCommands class'''


class InitExecCommands(object):
    """InitExecCommands class

    `InitExecCommands` class provides the functionality to retrieve the
    platform specific initiation executed commands.

    """

    def get_commands(self):
        """Method to return the list of the platform specific initiation
        executed commands

        Args:
            None

        Returns:
            `list`: a `list` of the initiation commands

        Examples:
            # Creating an instnace of InitExecCommands
            >>> init_exec_commands_instance = Lookup.from_device(device).sdk.\
                libs.abstracted_libs.init_exec_commands.InitExecCommands()

            # Calling get_commands method
            >>> init_exec_commands = init_exec_commands_instance.get_commands()
                ['term length 0','term width 511','terminal session-timeout 0']

        """

        # Create parser object
        init_commands = []

        return init_commands