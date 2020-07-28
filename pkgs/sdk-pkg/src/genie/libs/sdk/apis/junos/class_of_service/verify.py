"""Common verification functions for class-of-service"""

# Python
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_class_of_service_object_exists(device, interface, expected_object, invert=False, max_time=60, check_interval=10):
    """ Verifies class_of_service object exists

    Args:
        device (obj): Device object
        interface (str): Interface to check
        expected_object (str): Object name to check for
        invert (bool, optional): Whether to check if it doesn't exist or not. Defaults to False.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        True/False
    """

    op = operator.contains
    if invert:
        op = lambda lst, entry : operator.not_(operator.contains(lst, entry))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show class-of-service interface {interface}'.format(
                interface=interface
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # {
        #     "cos-interface-information": {
        #         "interface-map": {
        #             "i-logical-map": {
        #                 "cos-objects": {
        #                     "cos-object-type": [
        #                         str
        #                     ]
        #                 },
        #             },
        #         }
        #     }
        # }

        object_types_ = out.q.get_values("cos-object-type")

        if not op(object_types_, expected_object):
            timeout.sleep()
            continue

        return True
    return False

        
        