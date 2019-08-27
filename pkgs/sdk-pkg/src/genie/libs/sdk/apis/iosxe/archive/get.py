"""Common get info functions for archive"""

# Python
import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_archive_config_incremental_diffs(device, file):
    """ Gets the archive incremental diffs from file

        Args:
            device ('obj'): Device object
            file('str'): file to get diff from
        Returns:
            Parser output
            None
        Raises:
            None

    """
    log.info("Getting archive config incremental-diffs from {}".format(file))
    try:
        out = device.parse(
            "show archive config incremental-diffs " "{}".format(file)
        )
    except SchemaEmptyParserError:
        return None

    return out


def get_archive_config_differences(device, file1, file2):
    """ Gets the archive differences between {file1} and {file2}

        Args:
            device ('obj'): Device object
            file1('str'): file1 to get diff from
            file2('str'): file2 to get diff from

        Returns:
            Parser output
            None
        Raises:
            None
    """
    log.info(
        "Getting archive differences between {} and {}".format(file1, file2)
    )
    try:
        out = device.parse(
            "show archive config differences {} " "{}".format(file1, file2)
        )
    except SchemaEmptyParserError:
        return None

    return out
