"""Generic health API stubs — fallback for any OS without a specific implementation."""

# Python
import logging

log = logging.getLogger(__name__)


def health_cpu(device, health=True, *args, **kwargs):
    """Generic fallback for health_cpu on devices without a specific implementation.

    Args:
        health (`bool`): Return health_data dict format when True,
                         cpu_load_dict when False. Defaults to True.

    Returns:
        health_data (`dict`): empty result when health=True.
        cpu_load_dict (`dict`): empty dict when health=False.
    """
    log.warning(
        f"health_cpu is not supported on '{device.name}' "
        f"(os: {getattr(device, 'os', 'unknown')}). Skipping."
    )
    
    if health:
        return {'health_data': []}
    else:
        return {}


def health_memory(device, health=True, *args, **kwargs):
    """Generic fallback for health_memory on devices without a specific implementation.

    Args:
        health (`bool`): Return health_data dict format when True,
                         memory_usage_dict when False. Defaults to True.

    Returns:
        health_data (`dict`): empty result when health=True.
        memory_usage_dict (`dict`): empty dict when health=False.
    """
    log.warning(
        f"health_memory is not supported on '{device.name}' "
        f"(os: {getattr(device, 'os', 'unknown')}). Skipping."
    )
    
    if health:
        return {'health_data': []}
    else:
        return {}


def health_logging(device, health=True, num_of_logs=False, *args, **kwargs):
    """Generic fallback for health_logging on devices without a specific implementation.

    Args:
        health (`bool`): Return health_data dict format when True,
                         raw logs when False. Defaults to True.
        num_of_logs (`bool`): When health=False, return count instead of list.
                              Defaults to False.

    Returns:
        health_data (`dict`): empty result when health=True.
        logs (`list`): empty list when health=False and num_of_logs=False.
        count (`int`): 0 when health=False and num_of_logs=True.
    """
    log.warning(
        f"health_logging is not supported on '{device.name}' "
        f"(os: {getattr(device, 'os', 'unknown')}). Skipping."
    )
    
    if health:
        return {'health_data': {'num_of_logs': 0, 'lines': []}}
    elif num_of_logs:
        return 0
    else:
        return []


def health_core(device, health=True, *args, **kwargs):
    """Generic fallback for health_core on devices without a specific implementation.

    Args:
        health (`bool`): Return health_data dict format when True,
                         flat list when False. Defaults to True.

    Returns:
        health_data (`dict`): empty result when health=True.
        all_corefiles (`list`): empty list when health=False.
    """
    log.warning(
        f"health_core is not supported on '{device.name}' "
        f"(os: {getattr(device, 'os', 'unknown')}). Skipping."
    )
    
    if health:
        return {'health_data': {'num_of_cores': 0, 'corefiles': []}}
    else:
        return []


def health_crashinfo(device, health=True, *args, **kwargs):
    """Generic fallback for health_crashinfo on devices that do not support
    the crashinfo: filesystem (IOS XR, NX-OS, etc.).

    IOS XE has a full implementation under iosxe/health/health.py which the
    pyATS abstraction layer resolves first for IOS XE devices.  All other
    OS types fall back here and are skipped gracefully.

    Args:
        health (`bool`): Return health_data dict format when True,
                         flat list when False. Defaults to True.

    Returns:
        health_data (`dict`): empty result when health=True.
        all_crashfiles (`list`): empty list when health=False.
    """
    log.warning(
        f"health_crashinfo is not supported on '{device.name}' "
        f"(os: {getattr(device, 'os', 'unknown')}). Skipping."
    )
    
    if health:
        return {
            'health_data': {
                'num_of_crashfiles': 0,
                'crashfiles': []
            }
        }
    else:
        return []
