'''Generic implementation of ShowRun class'''


class ConfigureSnapshotCommand(object):
    """ConfigureSnapshotCommands class

    `ConfigureSnapshotCommands` class provides the functionality to
    retrieve the platform specific configurations command.

    """

    @property
    def command(self):
        """Method to return the configurations fetch command.
        Default will be 'show running-config'

        Args:
            None

        Returns:
            `str`: a `str` of the command

        Examples:
            # Creating an instnace of ConfigureSnapshotCommand
            >>> configure_snapshot_command = Lookup.from_device(device).sdk.\
                libs.abstracted_libs.configure_snapshot_command.ConfigureSnapshotCommand()

            # Calling get_commands method
            >>> configure_snapshot_command = configure_snapshot_command.command
                'show running-config'

        """
        # return cisco default command
        return 'show running-config'