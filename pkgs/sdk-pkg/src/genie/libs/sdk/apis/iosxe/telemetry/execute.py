"""Execute telemetry report related command"""

# Python
import logging
import time
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def execute_test_platform_sw_product_analytics_report(device):
    """   
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test platform software product-analytics report"

    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform pa report generation on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_platform_sw_product_analytics_send(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test platform software product-analytics send"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform pa report send on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_license_smart_telemetry_show(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test license smart telemetry show"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show rum report on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_license_smart_sync_all(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "license smart sync all"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform license smart sync all on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_telemetry_show_logging(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "show logging"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show logging on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_license_smart_dev_cert_enable(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test license smart dev-cert Enable"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to enable dev Certificate on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_show_license_boot_level_config(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "show running-config | i license boot level"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show license boot level running config on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_show_license_dev_cert(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "show license tech support | inc Cert"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show license tech support certificate on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_show_license_rum_id_telemetry(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "show license rum id all | inc TELEMETRY"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show license rum id all on Telemetry on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_clear_platform_software_product_analytics_report(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "clear platform software product-analytics report"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform clear product analytics report on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_platform_software_product_analytics_tdl_periodic(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test platform software product-analytics tdl periodic"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform test platform software product analytics tdl periodic on {device}. Error:\n{error}".format(device=device, error=e))
    return out

def execute_test_platform_software_product_analytics_data_proc_sql_periodic(device):
    """ 
        Args:
            device ('obj'): device to use  
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test platform software product-analytics data-proc sql periodic"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to perform test platform software product-analytics data-proc sql periodic on {device}. Error:\n{error}".format(device=device, error=e))
    return out
