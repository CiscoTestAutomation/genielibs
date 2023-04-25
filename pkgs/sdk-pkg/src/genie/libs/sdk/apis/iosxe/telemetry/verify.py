"""Common verify functions for sudi"""
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def verify_telemetry_enabled(device, supported):
    """ Verify pae in show running-config all 
        Args:
            device ('obj'): Device object
            supported ('list') : ''
        Returns:
            result (`bool`): Verified result
    """
    out_1 = out_2 = None
    supported.append('yes')
    ret_v = False
    try:
        out_1 = device.execute("show running-config all | inc ^pae")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show PAE default running-config on {device}. Error:\n{error}".format(device=device, error=e))
    try:
        out_2 = device.execute("show running-config | inc pae")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show PAE non-default running-config on {device}. Error:\n{error}".format(device=device, error=e))

    if out_1:
        match = re.search('pae', out_1)
        if match:
            log.info("telemetry is enabled")
            ret_v =True
        else:
            supported[0] = 'no'
            log.info("verification failed: unexpected error1!")   
    elif out_2:
        match = re.search('no pae', out_2)
        if match:           
            log.info("telemetry is disabled")
        else:
            supported[0] = 'no'
            log.info("verification failed: unexpected error2!")
    else:
        supported[0] = 'no'
        log.info("telemetry is not supported")
    return ret_v

def verify_telemetry_report_in_show_summary(device, report_id):
    """ Verify telemetry report_id is in show summary
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = None
    ret_v = False
    try:
        out = device.parse("show product-analytics report summary")
    except SchemaEmptyParserError:
        pass
    if out:
        if (out.q.contains(report_id)):
            log.info("verify_telemetry_report_in_show_summary: found report_id [%d]", report_id)
            ret_v = True
        else:
            log.info("report_id in show summary validation failed")
    else:
        log.info("cli is not parsed or no reports is in system!")
    return ret_v

def verify_telemetry_report_kpi_in_show_kpi_summary(device, report_id, kpi_list):
    """ Verify telemetry report_id and kpi is in show kpi summary
        Args:
            device ('obj'): Device object
            kpi_list ('list'): Kpi list
        Returns:
            result (`bool`): Verified result
    """
    out = None
    status = True
    try:
        out = device.parse("show product-analytics kpi summary")
    except SchemaEmptyParserError:
        pass
    if out:
        for kpi in kpi_list:
            if (out.q.contains(report_id).contains(kpi)):
                log.info("verify_telemetry_report_kpi_in_show_kpi_summary: found {report_id [%d], kpi [%s]} pair", report_id, kpi)
                continue
            else:
                log.info("report_id [%d], kpi [%s] in show kpi summary validation failed", report_id, kpi)
                status = False
                break
    else:
        log.info("cli is not parsed or no reports is in system!")
        status = False
    return status

def verify_smart_account_is_activated(device):
    """ Verify smart account is configured and linked in show license summary
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = ''
    status = False
    try:
        out = device.parse("show license summary")
    except SchemaEmptyParserError:
        pass
    if out:
        if out.q.contains('account_information').contains('smart_account') and (out['account_information']['smart_account'] != '<none>'):
            log.info("smart account is configured and activated")
            status = True
        else:
            log.info("smart account is none, not configured or activated")
    else:
        log.info("cli is not parsed or no license exists in system!")
    return status

def verify_license_usage(device):
    """ Verify at least 1 license is in use in show license summary
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = ''
    status = False
    try:
        out = device.parse("show license summary")
    except SchemaEmptyParserError:
        pass
    if out:
        if out.q.contains('license_usage') and (len(out['license_usage']) >=1):
            log.info("at least one license is in use")
            status = True
    else:
        log.info("cli is not parsed or no license config/usage in system!")
    return status

def verify_license_boot_level_configured(device):
    """ Verify license boot level configured or not
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = ''
    ret_v = False

    try:
        out = device.execute("show running-config | inc license boot level")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show license boot level running-config on {device}. Error:\n{error}".format(device=device, error=e))
    if out:
        m = re.search("license boot level", out)
        if m:
            log.info("verify_license_boot_level_configured: Yes")
            ret_v = True
        else:
            log.info("verify_license_boot_level_configured: No")
    else:
        log.info("verify_license_boot_level_configured: No")
    return ret_v

def verify_license_smart_transport_configured(device):
    """ Verify license smart transport is configured
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = ''
    ret_v = False
    try:
        out = device.execute("show running-config | inc transport")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show transport running-config on {device}. Error:\n{error}".format(device=device, error=e))
    if out:
        m = re.search("license smart transport smart", out)
        if m:
            log.info("verify_license_smart_transport_configured: Yes")
            ret_v = True
        else:
            log.info("verify_license_smart_transport_configured: No")
    else:
        log.info("verify_license_smart_transport_configured: No")
    return ret_v

def verify_license_smart_transport_support_telemetry(device):
    """ Verify license smart transport support telemetry
        Args:
            device ('obj'): Device object
        Returns:
            result (`bool`): Verified result
    """
    out = ''
    ret_v = False
    try:
        out = device.parse("show license all")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to show license all on {device}. Error:\n{error}".format(device=device, error=e))
    if out:
        if out.q.contains('smart_licensing_status').contains('transport').contains('type'):
            t_type = out['smart_licensing_status']['transport']['type']
            if t_type == 'Smart' or t_type == 'Transport Off' or t_type == 'cslu':
                log.info("verify_license_smart_transport_support_telemetry: Yes")
                ret_v = True
            else:
                log.info("verify_license_smart_transport_support_telemetry: No")
        else:
           log.info("verify_license_smart_transport_support_telemetry: error, no transport type") 
    else:
        log.info("verify_license_smart_transport_support_telemetry: error, no output")
    return ret_v