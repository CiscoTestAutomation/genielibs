# Python
import re
import jinja2
from jinja2.exceptions import TemplateNotFound

from unicon.core.errors import SubCommandFailure

def get_jinja_template(templates_dir, template_name):
    """ Get free and total space on disk
        Args:
            templates_dir ('str'): Templates directory
            template_name ('str'): Template name
        Return: 
            Template object
        Raise:
            SubCommandFailure
    """

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_dir)
    )

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        raise SubCommandFailure('Could not find template {template}' \
                            .format(template=template_name))

    return template