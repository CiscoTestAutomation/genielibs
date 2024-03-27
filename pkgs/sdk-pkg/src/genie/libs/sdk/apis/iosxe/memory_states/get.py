from genie.metaparser.util.exceptions import SchemaEmptyParserError
import logging
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)

def get_platform_memory_status(device):
    """
    Extracts summary information from the platform status parser output.

    Args:
        device (`obj`): Device object.

    Returns:
        dict: A dictionary containing slot information including committed, free, total, and used memory
        multiplied by 1024.
    """
    try:
        # Parse the command output
        out = device.parse('show platform software status control-processor brief')
    except SchemaEmptyParserError as e:
        log.error("Command 'show platform software status control-processor brief' did not return any results: {e}".format(e=e))

    slot_info = {
        'slot': [],
        'committed': [],
        'free': [],
        'total': [],
        'used': []
    }

    # Extracting slot information from the parser output
    slots = out.get('slot', {})

    for slot, details in slots.items():
        # Adjust slot name format
        if '-' in slot:
            # If slot name contains '-', consider it as "Switch" + first part of the split
            adjusted_slot = "Switch" + slot.split('-')[0]
        elif slot.startswith("rp"):
            # If slot name starts with "rp", consider it as "slot R" + numeric part
            adjusted_slot = "slot R" + slot[2:]
        else:
            # Otherwise, keep the slot name as it is
            adjusted_slot = slot

        # Extracting memory details for each slot
        memory_details = details.get('memory', {})

        # Multiply memory values by 1024
        committed = memory_details.get('committed') * 1024
        free = memory_details.get('free') * 1024
        total = memory_details.get('total') * 1024
        used = memory_details.get('used') * 1024

        # Append values to corresponding lists in slot_info dictionary
        slot_info['slot'].append(adjusted_slot)
        slot_info['committed'].append(committed)
        slot_info['free'].append(free)
        slot_info['total'].append(total)
        slot_info['used'].append(used)

    return slot_info
