import re
import logging
from genie.libs.conf.interface import ParsedInterfaceName

logger = logging.getLogger(__name__)


def breakout_interface_names(device, interface, breakout_mode):
    parsed_interface = ParsedInterfaceName(name=interface, device=device)

    breakout_mode = breakout_mode.upper()
    count, iftype = breakout_mode.split('X')
    m = re.search(r'(\d+)', iftype)
    if m:
        ifspeed = m.group(1)
    else:
        logger.warning(f'Unkown breakout speed {iftype}')
        return []

    count = int(count)

    ifname_map = {
        '10': 'TenGigE',
        '25': 'TwentyFiveGigE',
        '50': 'FiftyGigE',
        '100': 'HunderdGigE',
        '200': 'TwoHunderdGigE'
    }
    ifname = ifname_map.get(ifspeed)

    if not ifname:
        logger.warning(f'Unkown breakout {breakout_mode}')
        return []

    names = []
    for c in range(count):
        names.append(f'{ifname}{parsed_interface.number}/{c}')

    return names