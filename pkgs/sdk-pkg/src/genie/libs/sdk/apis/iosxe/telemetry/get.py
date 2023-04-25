"""Common get functions for api"""

# Python
import logging
import re
import pprint
import json
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
# unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.utils import has_configuration

log = logging.getLogger(__name__)

def get_actv_switch(device):
    """ get the current active switch from show redundancy states
        Args:
            device (`obj`): Device object
        Returns:
            number (`int`): switch number
    """
    out = None
    switch_num = 0
    try:
        out = device.parse("show redundancy states")
    except SchemaEmptyParserError:
        pass
    if out:
        switch_num = out['unit_id']
    else:
        log.error("cli is not parsed or other error")
    return switch_num

def get_system_redundancy_states(device):
    """ get parsed output or dict from show redundancy states
        Args:
            device (`obj`): Device object
        Returns:
            config (`obj`): out obj
    """
    out = None
    try:
        out = device.parse("show redundancy states")
    except SchemaEmptyParserError:
        pass
    if out == None:
        log.error("cli is not parsed")
    return out

def get_the_number_of_telemetry_report_in_system(device, s_list):
    """ get the number of reports and report list
        Args:
            device (`obj`): Device object
            list   ('obj'): report id list
        Returns:
            total number (int): total number of reports 
    """
    out = None
    tempList = []
    try:
        out = device.parse("show product-analytics report summary")
    except SchemaEmptyParserError:
        pass
    if out:
        tempList = out['paReports'].keys()
        for x in tempList:
            s_list.append(x)
        return len(out['paReports'])
    else:
        log.info("cli is not parsed, or no reports in system!")
        return 0

def get_kpi_value_in_show_kpi_report_id(device, report_id, kpi_name):
    """ get the kpi value based on report id and kpi name from show
        Args:
            device (`obj`): Device object
            report_id   ('int'): report id
            kpi_name  ('str') : kpi_name
        Returns:
            kpi value (`list`): kpi value list
    """
    out = None
    r_list = []
    log.info("get_kpi_value: report_id [%d] kpi_name: %s", report_id, kpi_name)

    try:
        out = device.parse('show product-analytics kpi report {}'.format(report_id))
    except SchemaEmptyParserError:
        pass
    if out == None:
        log.info("cli is not parsed or no reports in system")
    else:
        if out.q.contains('report_id').contains(report_id).contains('kpi_name').contains(kpi_name):
            r_list = json.loads(out['report_id'][report_id]['kpi_name'][kpi_name]['kpi_value'])
    return r_list

def get_telemetry_report_all_kpis(device, report_id):
    """ get all kpi name:value pairs based on report id given
        Args:
            device (`obj`): Device object
            report_id   ('int'): report id
        Returns:
            kpi name to value list (`list`): list of kpi name:value dict 
    """
    out = None
    log.info("get_telemetry_report_all_kpis: report_id [%d]", report_id)

    try:
        out = device.parse('show product-analytics kpi report {}'.format(report_id))
    except SchemaEmptyParserError:
        pass
    if out == None:
        log.info("cli is not parsed or no reports in system")
    return out
