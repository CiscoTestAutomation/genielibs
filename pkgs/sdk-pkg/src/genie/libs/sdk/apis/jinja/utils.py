"""Utility type functions that do not fit into another category"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq
# Pyats
from pyats.utils.objects import find, R

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_by_jinja2(device, templates_dir, template_name, **kwargs):
    """ Configure using Jinja template

        Args:
            device ('obj'): Device object
            templates_dir ('str'): Template directory
            template_name ('str'): Template name
            kwargs ('obj'): Keyword arguments
        Returns:
            Boolean
        Raises:
            None
    """

    log.info("Configuring {filename} on {device}".format(
        filename=template_name,
        device=device.alias))
    template = device.api.get_jinja_template(
        templates_dir=templates_dir,
        template_name=template_name)
    if not template:
        raise Exception('Could not get template')
    device.api.change_configuration_using_jinja_templates(
        template=template,
        **kwargs
    )
