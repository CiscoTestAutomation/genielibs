"""Utility type functions for interacting with Jinja templates"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def change_configuration_using_jinja_templates(device, template, **kwargs):
    """Use Jinja templates to change the device configuration

        Args:
            device (`obj`): Device object
            template (`obj`): Jinja template to be used in configuration
            parameters (`dict`): Dictionary of all the parameters
                                 to be passed to the Jinja template

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """

    out = [x.lstrip() for x in template.render(**kwargs).splitlines()]

    try:
        device.configure(out)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in applying the following "
            "configuration:\n{config}, error:\n{e}".format(config=out, e=e)
        )

    log.info("Successfully changed configuration using the jinja template")
