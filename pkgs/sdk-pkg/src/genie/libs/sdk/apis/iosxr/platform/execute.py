'''IOSXR execute functions for platform'''

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.harness.utils import connect_device
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def execute_install_pie(device, image_dir, image, server=None,
    prompt_level="none", synchronous=True, install_timeout=600, _install=True):

    ''' Installs and activates given IOSXR pie on device
        Args:
            device (`obj`): Device object
            image_dir (`str`): Directory where pie file is located in
            image (`str`): Pie file name
            server(`str`): Hostname or IP address of server to use for install command
                           Default None (Optional - uses testbed YAML reverse lookup for protocol server)
            prompt_level(`str`): Prompt-level argument for install command
                                 Default 'none' (Optional)
            synchronous (`bool`): Synchronous option for install command
                                  Default True (Optional)
            install_timeout (`int`): Maximum time required for install command to complete
                                     Default 600 seconds (Optional)

            _install (`bool`): True to install, False to uninstall.
                Not meant to be changed manually.

        Raises:
            Exception
    '''

    # Verify prompt_level type is correct
    assert prompt_level in ['none', 'all']

    # Get protocol and address from testbed YAML
    protocol = 'tftp'
    if not server:
        if not hasattr(device.testbed, 'servers'):
            raise Exception("Server not provided and testbed YAML is missing "
                            "servers block section")
        else:
            if not device.testbed.servers.get(protocol, {}).get('address', {}):
                raise Exception("Unable to find valid {} server within testbed "
                                "YAML servers block".format(protocol))
            server = device.testbed.servers.get(protocol, {}).address

    # Build 'install' command
    if _install:
        cmd = "install add source {protocol}://{server}/{image_dir} {image} activate".\
                format(protocol=protocol, server=server, image_dir=image_dir,
                        image=image)
    else:
        cmd = "install deactivate {image}".format(image=image)

    if prompt_level:
        cmd += " prompt-level {}".format(prompt_level)

    if synchronous:
        cmd += " synchronous"
    elif not synchronous:
        cmd += " asynchronous"

    # Execute command
    try:
        device.admin_execute(cmd, timeout=install_timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Error while executing install command for pie {} "
                        "on device {}".format(image, device.name))

    if _install:
        log.info("Installed and activated pie {} on device {}".\
                format(image, device.name))
    else:
        log.info("Deactivated pie {} on device {}".format(image, device.name))


def execute_deactivate_pie(device, image, server=None, prompt_level="none",
    synchronous=True, install_timeout=600):

    ''' De-activates given IOSXR pie on device
        Args:
            device (`obj`): Device object
            image (`str`): Pie file name
            server(`str`): Hostname or IP address of server to use for install command
                           Default None (Optional - uses testbed YAML reverse lookup for protocol server)
            prompt_level(`str`): Prompt-level argument for install command
                                 Default 'none' (Optional)
            synchronous (`bool`): Synchronous option for install command
                                  Default True (Optional)
            install_timeout (`int`): Maximum time required for install command to complete
                                     Default 600 seconds (Optional)

        Raises:
            Exception
    '''

    execute_install_pie(device, None, image, server, prompt_level,
        synchronous, install_timeout, _install=False)


def execute_remove_inactive_pies(device, remove_timeout=300):

    ''' Removes given IOSXR pie on device
        Args:
            device (`obj`): Device object
            remove_timeout (`str`): Maximum time to execute command
                                    Default 300 seconds (Optional)
        Raises:
            Exception
    '''

    log.info("Removing inactive pies on device {}".format(device.name))

    # Execute command to remove pie if uninstall specified
    try:
        device.admin_execute("install remove inactive", timeout=remove_timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Error while removing inactive pies on device {}".\
                        format(device.name))
    else:
        log.info("Successfully removed inactive pies on device {}".format(device.name))


def execute_set_config_register(device, config_register, timeout=60):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
                             Default 60 seconds (Optional)
    '''

    try:
        device.admin_execute("config-register {}".format(config_register),
                             timeout=timeout)
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to set config register to '{}' on device {}".\
                        format(config_register, device.name))
    else:
        log.info("Set config-register to '{}' on device".\
                format(config_register, device.name))

