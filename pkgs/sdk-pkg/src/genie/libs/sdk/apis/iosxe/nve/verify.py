"""Common verify functions for NVE"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def verify_nve_vni_no_entry(device, max_time=16,
                            check_interval=2,
                            **kwargs):
    """ Verify NVE VNI has no member configured.
        Args:
            device ('obj'): device object
            max_time ('int' 4, Optional): maximum time to wait, default 4
            check_interval ('int' 2, Optional): how often to check, default 2
        Returns:
            True or False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        entry = device.api.get_nve_vnis()
        if not entry:
            return True

        timeout.sleep()

    log.info("NVE interface has VNI members configured")
    return False


def verify_nve_vni_members_cfg(device, nve_num, exp_vni_member_cfg):
    """
    Verify the NVE member configuration is the same as provided

    Args:
        device (): Device used to run commands
        nve_num ('str'): NVE interface number
        exp_vni_member_cfg ('dict'): Dictionary of expected vni members config

    Returns:
        True or False
    Raises:
        None
    """

    nve_cfg = device.parse(f"show run interface nve {nve_num}")

    for vni, exp_vni_dict in exp_vni_member_cfg.items():
        log.info(f"Verify vni {vni} in running-config")
        vni_dict =  nve_cfg['interfaces'][f"nve{nve_num}"]['member_vni'].get(vni)
        if not vni_dict:
            log.info(f"vni {vni} is not found in run-config")
            return False
        for key, exp_val in exp_vni_dict.items():
            val = vni_dict.get(key)
            if val != exp_val:
                log.info(f"{key} is not a match for vni {vni}: exp {exp_val}, got {val}")
                return False
    return True
