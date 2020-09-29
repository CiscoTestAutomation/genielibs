"""Common get functions for log"""

# Python
import re
import logging
from datetime import datetime

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_log_message_time(device, message, file_name="messages"):
    """ Gets the timestamp of a log message

    Args:
        device (obj): Device object
        message (str): Message
        file_name (str): File to check. Defaults to 'messages'

    Returns:
        (datetime): Timestamp object
    """

    try:
        out = device.parse('show log {file_name}'.format(
            file_name=file_name
        ))
    except SchemaEmptyParserError:
        return None

    messages_ = out.q.contains('.*{}.*'.format(message), regex=True)
    
    if not messages_:
        return None

    time_group = re.match(r'^(?P<month>\S+) +(?P<day>\d+) +(?P<time>[\d:\.]+)', messages_[0][1]).groupdict()

    time_text = f"{time_group['month']} {time_group['day']} {time_group['time']}"

    try:
        time_obj = datetime.strptime(time_text, '%b %d %H:%M:%S.%f')
    except:
        time_obj = datetime.strptime(time_text, '%b %d %H:%M:%S')

    return time_obj.replace(year=datetime.now().year)

