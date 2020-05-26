# Python
import os
import re
import logging

# pyATS
from pyats.utils.objects import R, find

# Genie
from genie.utils import Dq
from genie.utils.diff import Diff
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError

# Logger
log = logging.getLogger(__name__)


def get_platform_standby_rp(device, max_time=1200, interval=120):
    """ Get standby router slot on device
        Args:
            device ('obj'): Device object
            max_time ('int'): Max time in seconds retrieving router information
            interval ('int'): Interval in seconds retrieving router information
        Raise:
            None
        Return:
            Integer: Number of RP
    """

    log.info("Getting standby slot")

    rs = R(
        ["slot", "(?P<val1>.*)", "rp", "(?P<val2>.*)", "state", "ok, standby"]
    )

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            standby_rp = ret[0][1][1]
            srp = re.search("(?P<srp>(\d))", standby_rp).groupdict()["srp"]
            if srp:
                log.info(
                    "Standby RP on '{dev}' is: '{standby_rp}'".format(
                        dev=device.name, standby_rp=standby_rp
                    )
                )
                return srp

        timeout.sleep()

    return None


def get_diffs_platform(platform_before, platform_after):
    """ Check differences between two parsed outputs from 'show platform'

        Args:
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
        Return:
            True
            False
        Raises:
            None
    """

    dd = Diff(platform_before, platform_after, exclude=["insert_time"])
    dd.findDiff()

    for slot in platform_after["slot"]:
        for rp_lc in platform_after["slot"][slot]:
            for type_ in platform_after["slot"][slot][rp_lc]:
                state_after = platform_after["slot"][slot][rp_lc][type_][
                    "state"
                ]

                state_before = (
                    platform_before["slot"]
                    .get(slot, {})
                    .get(rp_lc, {})
                    .get(type_, {})
                    .get("state", False)
                )

                if not state_before:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False

                for subslot in platform_before["slot"][slot][rp_lc].get(
                    "subslot", []
                ):

                    subslot_state = (
                        platform_after["slot"][slot][rp_lc]
                        .get(subslot, {})
                        .get("state", False)
                    )

                    if not subslot_state:
                        log.info(
                            "Found differences between outputs:\n{out}".format(
                                out=dd
                            )
                        )

                if state_after == state_before or ("ok" in state_after and "ok" in state_before):
                    continue
                else:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False
    return True


def get_file_size(device, file, output=None):
    '''Get file size on the device
        Args:
            device (`obj`): Device object
            file (`str`): File name
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            file size in `int` type or None if file size is not available
    '''

    directory = ''.join([os.path.dirname(file), '/'])
    filename = os.path.basename(file)
    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    size = Dq(dir_output).contains(filename).get_values('size')
    if size:
        return int(size[0])
    else:
        log.error("File '{}' is not found on device".format(file))


def get_running_image(device):
    '''Get running image on the device
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    '''

    try:
        # Execute 'show version'
        output = device.parse("show version")
        return output.get('version', {}).get('system_image')
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    return None


def get_available_space(device, directory='', output=None):
    '''Gets available space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): Directory to check space
                               If not provided, checks current working directory
                               i.e. media:/path/to/my/dir
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            space available in bytes in `int` type or 
            None if failed to retrieve available space
    '''

    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None

    bytes_free = Dq(dir_output).get_values(key='bytes_free')
    if bytes_free:
        return int(bytes_free[0])
    else:
        log.error("Failed to get available space for {}".format(directory))


def get_total_space(device, directory='', output=None):
    '''Gets total space on a given directory
        Args:
            device ('str'): Device object
            directory ('str'): Directory to check space
                               If not provided, checks current working directory
                               i.e. media:/path/to/my/dir
            output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            space available in bytes in `int` type or 
            None if failed to retrieve available space
    '''

    try:
        dir_output = device.parse('dir {}'.format(directory), output=output)
    except Exception as e:
        log.error("Failed to parse the directory listing due to: {}".\
                  format(str(e)))
        return None
    else:
        return int(dir_output.get('dir').get(directory).get('bytes_total'))


def get_boot_variables(device, boot_var, output=None):
    '''Get current or next-reload boot variables on the device
        Args:
            device (`obj`): Device object
            boot_var (`str`): Type of boot variable to return to caller
            output (`str`): output from show boot
        Returns:
            List of boot images or []
    '''

    # Check type
    assert boot_var in ['current', 'next']

    boot_images = []
    try:
        boot_out = device.parse("show bootvar", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show bootvar' did not return any output\n{}".\
                  format(str(e)))
    else:
        # Get current or next
        if boot_var == 'current':
            boot_variables = boot_out.get("current_boot_variable")
        else:
            boot_variables = boot_out.get("next_reload_boot_variable")

        # Trim
        if boot_variables:
            for item in boot_variables.split(';'):
                if not item:
                    continue
                if ',' in item:
                    item, num = item.split(',')
                if " " in item:
                    item, discard = item.split(" ")
                boot_images.append(item)

    return boot_images


def get_config_register(device, next_reload=False, output=None):
    '''Get current config-register setting on the device
        Args:
            device (`obj`): Device object
            next_reload (`bool`): Determine if returning next-reload value
        Returns:
            config-register value or None
    '''

    try:
        boot_out = device.parse("show bootvar", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show bootvar' did not return any output\n{}".\
                  format(str(e)))
        return None

    # Set keys
    nr_key = 'next_reload_configuration_register'
    cr_key = 'configuration_register'

    # Check if next_reload is set
    if next_reload and nr_key in boot_out.get('active'):
        return boot_out.get('active').get(nr_key)
    else:
        return boot_out.get('active').get(cr_key)
