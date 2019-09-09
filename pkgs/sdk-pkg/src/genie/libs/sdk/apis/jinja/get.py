# Python
import jinja2
from jinja2.exceptions import TemplateNotFound


def get_jinja_template(templates_dir, template_name):
    """ Gets the jinja template specified

        Args:
            templates_dir ('str'): Templates directory
            template_name ('str'): Template name

        Returns:
            ('obj') jinja template
            None

        Raises:
            None
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_dir),
        undefined=jinja2.StrictUndefined
    )

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        return

    return template
