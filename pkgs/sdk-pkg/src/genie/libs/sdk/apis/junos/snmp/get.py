'''Common get info functions for snmp'''
# Python
import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.utils import Dq

log = logging.getLogger(__name__)


def get_snmp_information(device):
    """ Get snmp information

        Args:
            device (`obj`): Device object
        Returns:
            result (`list`): list of snmp information
    """
    snmp_information = []

    try:
        out = device.parse('show snmp mib walk system')
    except SchemaEmptyParserError:
        return snmp_information

    # Example dictionary structure:
    # "snmp-object-information": {
    #     "snmp-object": [
    #         {
    #             "name": "sysDescr.0",
    #             "object-value": "Juniper "
    #                             "Networks, Inc. "
    #                             "vmx internet "
    #                             "router, kernel "
    #                             "JUNOS 19.2R1.8, "
    #                             "Build date: "
    #                             "2019-06-21 "
    #                             "21:03:26 UTC "
    #                             "Copyright (c) "
    #                             "1996-2019 "
    #                             "Juniper "
    #                             "Networks, Inc.",
    #         },
    #         {"name": "sysObjectID.0", "object-value": "jnxProductNameVMX"},
    #         {"name": "sysUpTime.0", "object-value": "1805867174"},
    #         {"name": "sysContact.0", "object-value": "KHK"},
    #         {"name": "sysName.0", "object-value": "sr_hktGDS201"},
    #         {
    #             "name": "sysLocation.0",
    #             "object-value": "TH-HK2/floor_1B-002/rack_KHK1104",
    #         },
    #         {"name": "sysServices.0", "object-value": "6"},
    #     ]
    # }
    # }

    snmp_information = Dq(out).get_values('snmp-object')
    return snmp_information
