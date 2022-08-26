import logging
log = logging.getLogger(__name__)
from genie.metaparser.util.exceptions import SchemaEmptyParserError
# Unicon
from unicon.core.errors import SubCommandFailure

def get_processes_five_seconds_cpu_usage(device):
    """ Get average CPU usage for last 5 seconds

        Args:
            device ('obj'): Device objecte

        Returns:
            CPU usage for last 5 seconds
            None
        Raises:
            None
    """

    try:
        output = device.parse("show processes cpu")
    except SchemaEmptyParserError:
        return None

    return output["five_sec_cpu_total"]

def get_cpu_processes_details_include_with_specific_process(device, process):
    ''' Get the cpu processes details include with specific_process
        Args:
            device('obj'): device to configure on
            process('str'): process name
        Return:
            None
        Raises:
            SubCommandFailure: Failed executing command
    '''
    log.info(
        "Get the cpu processes details include with specific_process".format(process=process)
    )
    cmd = f'show processes cpu | include {process}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute the cpu processes details include with specific {process} on device".format(process=process, e=e)
        )
