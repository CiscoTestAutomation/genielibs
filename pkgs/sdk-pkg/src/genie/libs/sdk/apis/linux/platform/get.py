# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)

def get_platform_logging(device,
                         command='cat',
                         files=['/var/log/syslog'],
                         keywords=None,
                         timeout=300,
                         prompt_pattern=None,
                         error_patterns=None,
                         output=None):
    '''Get logging messages

        Args:
            device          (`obj`): Device object
            command         (`str`): Override show command
            files          (`list`): List of syslog files
            keywords       (`list`): List of keywords to match
            timeout         (`int`): timeout (default: 300 secs)
            output          (`str`): Not Available on this platform
            prompt_pattern  (`str`): Prompt pattern
            error_patterns (`list`): Error patterns. if not specified, [](empty) is default.
        Returns:
            logs           (`list`): list of logging messages
    '''

    # check keywords and create strings for `egrep`

    # backup original error pattern and shell pattern
    err_pattern = device.settings.ERROR_PATTERN
    shell_pattern = device.state_machine.get_state('shell')
    if isinstance(error_patterns, list):
        device.jh.settings.ERROR_PATTERN = error_patterns
    else: 
        device.settings.ERROR_PATTERN = []

    # if prompt_pattern is given, override as temporary
    if prompt_pattern:
        device.state_machine.get_state('shell').pattern = prompt_pattern

    kw = ''
    if isinstance(keywords, list):
        kw = '|'.join(keywords)

    msg_logs = ''
    for filename in files:
        if '.gz' in filename:
            cmd = 'z' + command
        else:
            cmd = command
        if kw:
            msg_logs += device.execute("{command} {filename} | egrep '{kw}'".format(command=cmd, filename=filename, kw=kw), timeout=timeout)
        else:
            msg_logs += device.execute("{command} {filename}".format(command=cmd, filename=filename), timeout=timeout)

    logs = msg_logs.splitlines()

    # restore original error pattern and pt_pattern
    device.settings.ERROR_PATTERN = err_pattern
    device.state_machine.get_state('shell').pattern = shell_pattern
    return logs
