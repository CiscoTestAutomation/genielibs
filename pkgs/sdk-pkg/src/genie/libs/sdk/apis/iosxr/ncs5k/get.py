import logging

from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError,
    SchemaMissingKeyError)

log = logging.getLogger(__name__)

def get_software_version(device):
    """ Gets the version of the current running image
        Args:
            device (`obj`): Device object
        Returns:
            Image or None
    """
    try:
        # Execute 'show version'
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    else:
        return output.get('software_version')

    return None
