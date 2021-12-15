# Python
import re
import logging
import pathlib

# Logger
log = logging.getLogger(__name__)

# unicon
from unicon.eal.dialogs import Dialog, Statement
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


def execute_by_jinja2(device,
                      templates_dir,
                      template_name,
                      post_commands=None,
                      failure_commands=None,
                      **kwargs):
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
        filename=template_name, device=device.alias))
    template = device.api.get_jinja_template(templates_dir=templates_dir,
                                             template_name=template_name)

    if not template:
        raise Exception('Could not get template')

    timeout = kwargs.pop('timeout', None)
    out = [x.lstrip() for x in template.render(**kwargs).splitlines()]

    if post_commands:
        out += post_commands

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
        raise SubCommandFailure("Failed in applying the following "
                                "configuration:\n{config}, error:\n{e}".format(
                                    config=out, e=e))

    log.info("Successfully changed configuration using the jinja template")


def get_md5_hash_of_file(device, file, timeout=60):
    """ Return the MD5 hash of a given file.

    Args:
        device (obj): Device to execute on
        file (str): File to calculate the MD5 on
        timeout (int, optional): Max time in seconds allowed for calculation.
            Defaults to 60.

    Returns:
        MD5 hash (str), or None if something went wrong
    """
    # md5sum test_file.bin
    # 5a06abf1ce541d311de335ce6bd9997a  /test_file.bin
    try:
        return device.execute('md5sum {}'.format(file),
                              timeout=timeout).split()[0]
    except Exception as e:
        log.warning(e)
        return None


def scp(device,
        local_path,
        remote_path,
        remote_device,
        remote_user=None,
        remote_pass=None,
        remote_via=None,
        creds=None,
        timeout=None,
        **kwargs):
    """ copy files from local device to remote device via scp

        Args:
            device (`obj`) : Device object (local device)
            local_path (`str`): path with file on local device
            remote_device (`str`): remote device name
            remote_path (`str`): path with file on remote device
            remote_user (`str`): use given username to scp
                                 Default to None
            remote_pass (`str`): use given password to scp
                                 Default to None
            remote_via (`str`): specify connection to get ip
                                Default to None
            creds (`str`): Name of the credentials for the remote device
                           Defaults to "default"
            timeout (`timeout`, optional): timeout for scp in seconds. Defaults to None
        Returns:
            result (`bool`): True if scp successfully done
    """
    # convert from device name to device object
    remote_device = device.testbed.devices[remote_device]
    # set credential for remote device
    username, password = remote_device.api.get_username_password(creds=creds)
    if remote_user:
        username = remote_user
    if remote_pass:
        password = remote_pass

    # find ip for remote server from testbed yaml
    if remote_via:
        remote_device_ip = remote_device.connections.get(remote_via, {}).get('ip') or \
            remote_device.connections.get(remote_via, {}).get('host')
    else:
        remote_connections = list(remote_device.connections.keys())
        if 'defaults' in remote_connections:
            remote_connections.remove('defaults')
        via = remote_device.connections.get('defaults', {}).get(
            'via', remote_connections[0] if remote_connections else None)
        remote_device_ip = remote_device.connections.get(via, {}).get('ip') or \
            remote_device.connections[via].get('host')
    if not remote_device_ip:
        raise ValueError('Please specify remote_via with a connection'
                         ' name that has an ip or host attribute.')

    local_filename = pathlib.Path(local_path).name

    # complete remote_path with credential and ip
    remote_path = "{id}@{ip}:{rp}".format(id=username,
                                          ip=remote_device_ip,
                                          rp=remote_path)

    s1 = Statement(pattern=r".*[pP]assword:",
                   action="sendline({pw})".format(pw=password),
                   args=None,
                   loop_continue=True,
                   continue_timer=False)
    dialog = Dialog([s1])

    try:
        out = device.execute("scp {lp} {rp}".format(lp=local_path,
                                                    rp=remote_path),
                             reply=dialog,
                             timeout=timeout,
                             **kwargs)

    except Exception as e:
        log.warning("Failed to copy from {lp} to {rp} via scp: {e}".format(
            lp=local_path, rp=remote_path, e=e))
        return False

    # return True/False depending on result
    return bool(re.search(r'{}\s*100%'.format(local_filename), out))
