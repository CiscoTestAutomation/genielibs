# Python
import re
import logging
# unicon
from unicon.core.errors import SubCommandFailure
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.utils import get_config_dict
from genie.utils import Dq

def get_task_memory_information(device):
    """ Currently just gets size value of memory currently
        in use, but can be enhanced to get more values in the future.

        Args:
            device (`obj`): Device object
        Returns:
            result (`str`): size of memory currently in use
    """

    try:
        out = device.parse('show task memory')
    except SchemaEmptyParserError:
        return None

    # Example dictionary structure:
    # "task-memory-information":{
    #         "task-memory-free-size":"2078171",
    #         "task-memory-free-size-avail":"100",
    #         "task-memory-free-size-status":"now",
    #         "task-memory-in-use-avail":"1",
    #         "task-memory-in-use-size":"26857",
    #         "task-memory-in-use-size-status":"now",
    #         "task-memory-max-avail":"1",
    #         "task-memory-max-size":"27300",
    #         "task-memory-max-when":"20/10/01 01:27:19"
    #     }

    return out.q.get_values('task-memory-in-use-size',0)
