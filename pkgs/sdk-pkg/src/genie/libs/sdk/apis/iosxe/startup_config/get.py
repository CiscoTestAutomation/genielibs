"""Utility type functions that do not fit into another category"""

# Python
import logging
import time

# Running-Config
from genie.libs.sdk.apis.utils import get_config_dict

log = logging.getLogger(__name__)


def get_startup_config_dict(device, section=None, options=None):
    """ Get section information from show startup-config

        Args:
            device ('str'): Device str
            section ('str'): Section str
        Returns:
            Configuration dict
    """
    if options and section:
        cmd = "show startup-config {options} | section {section}".format(
            options=options, section=section
        )
    elif options:
        cmd = "show startup-config {options}".format(options=options)

    elif section:
        cmd = "show startup-config | section {section}".format(section=section)
    else:
        cmd = "show startup-config"

    try:
        output = device.execute(cmd)
    except Exception as e:
        raise Exception(
            "Could not execute command {cmd}\nError:{e}".format(
                cmd=cmd, e=str(e)
            )
        )
    config_dict = get_config_dict(output)

    return config_dict
