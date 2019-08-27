'''Common verify functions for controllers'''
# Python
import re
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def verify_optics_in_state(device, optics, rx_power, controller_state='up', led_state='green', 
                           max_time=60, check_interval=20):
    ''' Verify optics state

        Args:
            device (`obj`): Device object
            optics (`str`): Optics port
            rx_power (`float`): Expected RX power
            controller_state (`str`): Expected controller state
            led_state (`str`): Expected LED state
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show controllers optics {}'.format(optics)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        cs = out.get(optics, {}).get('controller_state', '').lower()
        ls = out.get(optics, {}).get('led_state', '').lower()
        rx = out.get(optics, {}).get('optics_status', {}).get('rx_power', '')

        # -30 dBm
        p = re.compile(r'(?P<power>\S+) +dBm')
        m = p.search(rx)
        if m:
            rx = float(m.groupdict()['power'])

        log.info("Optics {} Controller State is {}, expected value is {}"
            .format(optics, cs, controller_state))

        log.info("Optics {} LED State is {}, expected value is {}"
            .format(optics, ls, led_state))

        log.info("Optics {} RX Power is {} dBm, expected value is higher than {} dBm"
            .format(optics, rx, rx_power))
        
        # if rx is not float
        if (m and cs == controller_state.lower() and 
            ls == led_state.lower() and 
            rx >= rx_power):
            return True

        timeout.sleep()

    return False


def verify_coherentDSP_in_state(device, dsp, controller_state='up', derived_state='in service', 
                             max_time=60, check_interval=20):
    ''' Verify coherentDSP state

        Args:
            device (`obj`): Device object
            dsp (`str`): CoherentDSP port
            controller_state (`str`): Expected controller state
            derived_state (`str`): Expected derived state
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): Verified result
    '''
    cmd = 'show controllers coherentDSP {}'.format(dsp)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        cs = out.get(dsp, {}).get('controller_state', '').lower()
        ds = out.get(dsp, {}).get('derived_state', '').lower()

        log.info("CoherentDSP {} controller state is {}, expected value is {}"
            .format(dsp, cs, controller_state))

        log.info("CoherentDSP {} derived state is {}, expected value is {}"
            .format(dsp, ds, derived_state))

        if cs == controller_state.lower() and ds == derived_state.lower():
            return True
        
        timeout.sleep()
    
    return False
