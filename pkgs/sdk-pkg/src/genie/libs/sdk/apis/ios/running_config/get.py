"""Utility type functions that do not fit into another category"""

# Python
import logging
import re

# unicon
from unicon.core.errors import SubCommandFailure

# Running-Config
from genie.libs.sdk.apis.utils import get_config_dict
from genie.libs.sdk.apis.iosxe.running_config.get import \
    get_valid_config_from_running_config as base_get_valid_config_from_running_config

log = logging.getLogger(__name__)


def search_running_config(device, option):
    """ search config in show running-config output

        Args:
            device (`obj`): Device object
            option (`str`): key word to search
        Returns:
            config (`str`): search result
    """
    out = device.execute("show running-config | include {}".format(option))

    config = None

    m = re.search(r"{} +(?P<cfg>[\S]+)".format(option), out)
    if m:
        config = m.groupdict()["cfg"]
    return config


def get_running_config_dict(device, option=None):
    """ Get show running-config output

        Args:
            device (`obj`): Device object
            option (`str`): option command
        Returns:
            config_dict (`dict`): dict of show run output
    """
    if option:
        cmd = "show running-config {}".format(option)
    else:
        cmd = "show running-config"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not get running-config information "
            "on device {device}".format(device=device.name)
        )

    config_dict = get_config_dict(out)
    return config_dict


def get_running_config_hostname(device, iteration=5):
    """ Get device hostname from show run

        Args:
            device (`obj`): Device object
        Returns:
            hostname (`str`): Device hostname
    """
    log.info("Get hostname from {}".format(device.name))
    hostname = ""
    for i in range(iteration):
        try:
            out = device.execute("show running-config | include hostname")
            hostname = re.match(r"hostname +(?P<name>\S+)", out).groupdict()[
                "name"
            ]
        except Exception as e:
            log.error("Failed to get hostname:{}".format(e))
            continue

        return hostname


def get_running_config_section_dict(
    device, section=None, options=None
):
    """ Get section information from show run

        Args:
            device ('str'): Device str
            section ('str'): Section str
        Returns:
            Configuration dict
    """
    if options and section:
        cmd = "show run {options} | section {section}".format(
            options=options, section=section
        )
    elif options:
        cmd = "show run {options}".format(options=options)
    elif section:
        cmd = "show run | section {section}".format(section=section)
    else:
        cmd = "show run"

    try:
        output = device.execute(cmd)
    except SubCommandFailure:
        return None
        
    config_dict = get_config_dict(output)

    return config_dict


def get_running_config(device, keyword=None):
    """ Return list with configuration starting with passed keyword

        Args:
            device ('obj')  : Device object to extract configuration
            keyword ('str') : Configuration to be extracted from device
        Returns:
            List containing configuration
    """

    if keyword:
        output = device.execute(
            "show running-config | i ^{keyword}".format(keyword=keyword)
        )
    else:
        output = device.execute("show running-config")

    return output.splitlines()


def get_running_config_section(device, keyword):
    """ Return list with configuration section starting with passed keyword

        Args:
            device ('obj')  : Device object to extract configuration
            keyword ('str') : Configuration to be extracted from device
        Returns:
            Return list of configuration section starting with the passed keyword
    """

    output = device.execute(
        "show running-config | sec ^{keyword}".format(keyword=keyword)
    )

    return output.splitlines()


def get_config_commands_from_running_config(
    device, option
):
    """ Builds configuration command from running config

        Args:
            device ('obj'): device to run on
            option ('str'): running config sub option

        Returns:
            list of config commands
    """
    log.info(
        "Building configuration command from show running-config {}".format(
            option
        )
    )
    config_commands = []

    config_start = False

    out = device.execute("show running-config {}".format(option))
    for line in out.splitlines():
        line = line.strip()

        if not config_start and option.lower() in line.lower():
            config_start = True

        if config_start:
            if line in "end":
                break

            config_commands.append(line)

    return config_commands

def get_valid_config_from_running_config(device, exclude=None, begin='version'):
    """ Returns a configuration from 'show running-config | begin version'.
        The API will exclude any configuration and sub configuration that
        matches regex from exclude. The returned string can be used to
        configure a device.

        Args:
            device ('obj'): Device to run on
            exclude ('str'): Regex of config to exclude
            begin ('str'): Begin command for show run

        Returns:
            String of configuration
    """
    return base_get_valid_config_from_running_config(device, exclude, begin)