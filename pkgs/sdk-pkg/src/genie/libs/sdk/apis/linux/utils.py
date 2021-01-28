# Python
import logging

# Logger
log = logging.getLogger(__name__)
# unicon
from unicon.core.errors import SubCommandFailure

def extract_tar_gz(device, path, files, option='-zxvf'):
    """ extract tar.gz file
        Args:
            files (`list`): list of tar.gz files
            option (`str`): option to tar command for extraction
                            Default to `-zxvf`
        Raises:
            N/A
        Returns:
            extracted_files (`list`): extracted file list
    """
    extracted_files = []

    log.debug('files : {f}'.format(f=files))

    for file in files:
        # check if the file has extention `.tar.gz`
        if '.tar.gz' not in file:
            raise Exception('file {f} is not tar.gz file'.format(f=file))
        # create folder_name from filename
        folder_name = file.split('.tar.gz')[0]
        # extract tar.gz file
        output = device.api.execute("cd {p} && mkdir {d} && cd {d} && tar {op} ../{f}".\
            format(p=path, d=folder_name, op=option, f=file))
        # based on output, `extracted_files` list will be created as return
        if output:
            for file in output.split():
                extracted_files.append('{p}/{d}/{f}'.format(p=path,
                                                            d=folder_name,
                                                            f=file))
        if 'cannot create directory' in output:
            raise Exception(
                "Directory {d} already exists and couldn't create".format(
                    d=folder_name))

    return extracted_files

def execute_by_jinja2(device, templates_dir, template_name, post_commands=None, failure_commands=None, **kwargs):
    """ Configure using Jinja template
        Args:
            device ('obj'): Device object
            templates_dir ('str'): Template directory
            template_name ('str'): Template name
            post_commands ('list'): List of post commands
            failure_commands ('list'): List of commands required after failure
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

    timeout = kwargs.pop('timeout', None)
    out = [x.lstrip() for x in template.render(**kwargs).splitlines()]

    if post_commands:
        out = out + post_commands
    
    try:
        for cmd in out:
            if timeout:
                log.info('{} timeout value used for device: {}'.format(
                    timeout, device.name))
                device.execute(cmd, timeout=timeout)
            else:
                device.execute(cmd)
    except SubCommandFailure as e:
        if failure_commands:
            device.execute(failure_commands)   
        raise SubCommandFailure(
            "Failed in applying the following "
            "configuration:\n{config}, error:\n{e}".format(config=out, e=e)
        )

    log.info("Successfully changed configuration using the jinja template")
