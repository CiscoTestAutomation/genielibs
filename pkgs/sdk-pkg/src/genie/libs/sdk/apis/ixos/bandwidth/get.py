""" Get type APIs for IXOS """
import re
import logging

log = logging.getLogger(__name__)


def get_bandwidth(pattern):
    """
    The API parses the given pattern to get the bandwidth
    and also does the unit conversion if exist

    Args:
        pattern (str): pattern to be matched
    Returns:
        bandwidth
    """

    unit_conversion = {"GE": 1000} # Gigabit Ethernet

    # 10/100/1000 Base T
    p = re.compile(r'^(?P<bandwidth>\d+\/\d+\/(\d+))+\s+Base T$')

    # 100GE SR10
    p1 = re.compile(r'^(?P<bandwidth>[\d\/]+)(?P<unit>GE)+\s+SR10$')

    # 10/100/1000 Base T
    m = p.match(pattern)
    if m:
        speed = int(m.group(2))
        return speed

    # 100GE SR10
    m = p1.match(pattern)
    if m:
        speed = int(m.group(1))
        unit = unit_conversion.get(m.group(2))
        return speed*unit

    return None
