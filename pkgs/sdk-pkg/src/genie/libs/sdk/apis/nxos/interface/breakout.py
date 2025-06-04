import re
import logging
from genie.libs.conf.interface import ParsedInterfaceName

logger = logging.getLogger(__name__)


def breakout_interface_names(device, interface, breakout_mode):
    parsed_interface = ParsedInterfaceName(name=interface, device=device)

    breakout_mode = breakout_mode.upper()
    count, _iftype = breakout_mode.split('X')
    count = int(count)

    ifname = 'Ethernet'

    if not ifname:
        logger.warning(f'Unkown breakout {breakout_mode}')
        return []

    names = []
    for c in range(count):
        names.append(f'{ifname}{parsed_interface.number}/{c+1}')

    return names