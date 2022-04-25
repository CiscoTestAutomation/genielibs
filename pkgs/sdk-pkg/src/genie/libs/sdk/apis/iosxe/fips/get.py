"""Common get info functions for fips"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_fips_authorization_key(device):
    """Gets the fips authorization-key

    Args:
        device (obj): Device object

    Returns:
        fips authorization-key
    """
    try:
        out = device.parse('show fips authorization-key')
    except SchemaEmptyParserError as e:
        log.info("Command has not returned any results")
        return None
    stored_key = out.get("stored_key", None)

    if stored_key:
        log.info(
            "Found Stored Key {st_key}".format(
                st_key=stored_key
            )
        )

    return stored_key
