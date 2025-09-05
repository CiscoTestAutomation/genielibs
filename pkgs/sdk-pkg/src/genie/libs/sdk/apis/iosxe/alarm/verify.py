'''IOSXE verify functions for alarms '''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement
from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def verify_alarm_settings(device,
                          expected_alarm_relay_mode=None,
                          expected_alarm_logger_level=None,
                          expected_settings=None,
                          max_time=15,
                          check_interval=5):
    """
    Verify alarm settings on the device using Genie parsed output.

    Args:
        device (`obj`): Genie device object
        expected_alarm_relay_mode (`str`): Expected relay mode (e.g. 'Positive')
        expected_alarm_logger_level (`str`): Expected logger level (e.g. 'Disabled')
        expected_settings (`dict`): Alarm settings per component.
            Example:
            expected_settings = {
            'power_supply': {
                'alarm': 'Enabled',
                'relay': '',
                'notifies': 'Disabled',
                'syslog': 'Enabled'
            },
            'temperature_primary': {
                'alarm': 'Enabled',
                'relay': 'MAJ',
                'notifies': 'Enabled',
                'syslog': 'Enabled',
                'thresholds': {
                    'max_temp': '80C',
                    'min_temp': '0C'
                }
            },
            }

        max_time (`int`): Max time to wait
        check_interval (`int`): Time between retries

    Returns:
        bool: True if all checks pass, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show alarm settings")
        except SchemaEmptyParserError:
            log.warning("Empty output from 'show alarm settings', retrying...")
            continue

        result = True
        
        # Top-level checks
        if expected_alarm_relay_mode:
            actual_mode = output.get("alarm_relay_mode", "")
            if actual_mode != expected_alarm_relay_mode:
                log.error(f"Alarm relay mode mismatch: expected '{expected_alarm_relay_mode}', got '{actual_mode}'")
                result = False
            else:
                log.info(f"Alarm relay mode matched: {actual_mode}")

        if expected_alarm_logger_level:
            actual_logger = output.get("alarm_logger_level", "")
            if actual_logger != expected_alarm_logger_level:
                log.error(f"Alarm logger level mismatch: expected '{expected_alarm_logger_level}', got '{actual_logger}'")
                result = False
            else:
                log.info(f"Alarm logger level matched: {actual_logger}")

        # Section-wise checks
        if expected_settings:
            for section, expected_fields in expected_settings.items():
                actual_fields = output.get(section.lower().replace("-", "_"), {})
                if not actual_fields:
                    log.error(f"Section '{section}' not found in device output.")
                    result = False
                    continue
                
                for field, expected_val in expected_fields.items():
                    if field == "thresholds":
                        actual_thresholds = actual_fields.get("threshold", {})
                        for t_key, t_expected in expected_val.items():
                            threshold_key = f"{t_key.lower()}"
                            t_actual = actual_thresholds.get(threshold_key)
                            if t_actual != t_expected:
                                log.error(f"{section} threshold '{t_key}' mismatch: expected '{t_expected}', got '{t_actual}'")
                                result = False
                            else:
                                log.info(f"{section} threshold '{t_key}' matched: {t_actual}")
                    else:
                        actual_val = actual_fields.get(field)
                        if actual_val != expected_val:
                            log.error(f"{section} -> '{field}' mismatch: expected '{expected_val}', got '{actual_val}'")
                            result = False
                        else:
                            log.info(f"{section} -> '{field}' matched: {actual_val}")

        if result:
            return True
        
        # If we reach here, some checks failed
        log.warning("Verification failed, retrying...")
        timeout.sleep()        

    return False