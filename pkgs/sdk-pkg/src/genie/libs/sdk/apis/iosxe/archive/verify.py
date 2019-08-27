"""Common verify functions for archive"""

# Python
import logging

log = logging.getLogger(__name__)


def compare_archive_config_dicts(dict1, dict2, exclude=None):
    """ Checks for differences between two 'show archive' dictionaries

        Args:
            dict1('dict'): first dictionary
            dict2('dict'): seconds dictionary

        Returns:
            list of commands that are different between the two configs
        Raises:
            None
    """
    if not exclude:
        exclude = []

    log.info("Gathering differences between archive configs")

    if "list_of_commands" in dict1:
        list_of_commands1 = dict1["list_of_commands"]
    elif "diff" in dict1:
        list_of_commands1 = dict1["diff"]

    if "list_of_commands" in dict2:
        list_of_commands2 = dict2["list_of_commands"]
    elif "diff" in dict2:
        list_of_commands2 = dict2["diff"]

    diff = list(set(list_of_commands2) - set(list_of_commands1))
    diff.extend(list(set(list_of_commands1) - set(list_of_commands2)))
    for exc in exclude:
        try:
            diff.remove(exc)
        except ValueError:
            continue

    return diff
