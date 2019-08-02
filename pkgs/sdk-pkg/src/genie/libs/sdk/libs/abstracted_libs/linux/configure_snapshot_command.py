'''Linux implementation of ShowRun class'''


class ConfigureSnapshotCommand(object):
    """ConfigureSnapshotCommands class

    `ConfigureSnapshotCommands` class provides the functionality to
    retrieve the platform specific configurations command.

    """

    @property
    def command(self):
        """Method to return the configurations fetch command.

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
                'show configuration'

        """
        # return Linux default command
        return None
