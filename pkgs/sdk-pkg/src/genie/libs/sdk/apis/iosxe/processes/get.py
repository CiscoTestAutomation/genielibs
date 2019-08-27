from genie.metaparser.util.exceptions import SchemaEmptyParserError


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
