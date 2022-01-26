"""Common get functions for stackwise-virtual"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def get_switch_state(device,state):
    """ Get active/standby switch in SVL

        Args:
            device ('str'): Device str
            state ('str'): state of the device(active/standby)
        Returns:
            switch with mentioned state
    """
    output=device.parse("show switch")
    switch={}
    for swit in output.q.get_values('stack'):
        switch_state=output.q.contains(swit).get_values('role')
        switch.update({switch_state[0].lower():swit})
    return switch[state]