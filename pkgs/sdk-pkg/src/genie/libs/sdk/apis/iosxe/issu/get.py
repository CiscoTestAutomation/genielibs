import re

from unicon.core.errors import SubCommandFailure


def get_issu_space_info_on_disk(device, disk, output=""):
    """ Get free and total space on disk
        Args:
            device ('obj'): Device object
            disk ('str'): Disk name
            output ('str'): Output from command 'dir {disk}'
        Return: 
            list: 
                bytes_total ('int'): Total space on disk in bytes
                bytes_free ('int'): Free space on disk in bytes
        Raise:
            SubCommandFailure: Failed executing dir command
    """

    if not output:
        try:
            output = device.execute("dir {disk}:".format(disk=disk))
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Unable to execute 'dir {disk}'".format(disk)
            )

    m = re.search(
        "(?P<total>(\d+)) +bytes +total +\((?P<free>(\d+)) " "+bytes +free\)",
        output,
    )

    bytes_total = int(m.groupdict()["total"])
    bytes_free = int(m.groupdict()["free"])

    return bytes_total, bytes_free


def get_issu_free_space_on_disk(device, disk, output=""):
    """ Get free space information on disk
        Args:
            device ('obj'): Device object
            disk ('str'): Disk name
            output ('str'): Output from command 'dir {disk}'
        Return:            
            Integer: Free space on disk in bytes
        Raises: 
            SubCommandFailure: Failed getting free space info on device
    """
    try:
        return get_issu_space_info_on_disk(
            device=device, disk=disk, output=output
        )[1]
    except SubCommandFailure as e:
        raise SubCommandFailure(str(e))
