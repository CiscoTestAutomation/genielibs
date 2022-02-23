# Python
import jinja2
from jinja2.exceptions import TemplateNotFound
import logging

log = logging.getLogger(__name__)


def get_jinja_template(templates_dir, template_name, trim_blocks=True, lstrip_blocks=True, **kwargs):
    """ Gets the jinja template specified

        Args:
            templates_dir ('str'): Templates directory
            template_name ('str'): Template name
            trim_blocks (`bool`): Whether to trim newlines or not. Defaults to True
            lstrip_blocks (`bool`): Whether to trim leading whitespace or not. Defaults to True
            kwargs (`dict`): Key value pairs

        Returns:
            ('obj') jinja template
            None

        Raises:
            None
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=templates_dir),
        undefined=jinja2.StrictUndefined,
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks)

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        return

    return template


def load_jinja_template(path, file, trim_blocks=True, lstrip_blocks=True, **kwargs):
    """Use Jinja templates to build the device configuration

        Args:
            path (`str`): Path to file directory
            file (`str`): File name
            trim_blocks (`bool`): Whether to trim newlines or not. Defaults to True
            lstrip_blocks (`bool`): Whether to trim leading whitespace or not. Defaults to True
            kwargs (`dict`): Key value pairs
        Returns:
            out (`str`): Rendered template
        Raises:
            TemplateNotFound
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=path),
                             undefined=jinja2.StrictUndefined,
                             trim_blocks=trim_blocks,
                             lstrip_blocks=lstrip_blocks)
    try:
        template = env.get_template(file)
    except TemplateNotFound:
        log.error(f"Template was not found. path: {path} / file: {file}")
        raise
    return template.render(**kwargs)
