""" debug related APIs for N9K """

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def enable_backtrace(
    device,
    service,
    module=None,
    frame_count=6,
):
    """ analyze core by BingoPy
        # CISCO INTERNAL

        Args:
            device (`obj`): Device object
            service (`str`): service to enable backtrace
            module (`int`): module number for LCs
            frame_count (`int`): number of backtraces
        Returns:
            out (`str`): Output of command
    """

    # get sap_id
    try:
        out = device.parse(
            "show system internal sysmgr service name {service}".format(
                service=service))
        # example:
        # {
        #     "instance": {
        #         "bgp": {
        #             "tag": {
        #                 "65000": {
        #                     "internal_id": 87,
        #                     "last_restart_date": "Thu Aug 20 05:49:00 2020",
        #                     "last_terminate_reason": "SYSMGR_DEATH_REASON_FAILURE_SIGNAL",
        #                     "pid": 19262,
        #                     "plugin_id": "1",
        #                     "previous_pid": 18234,
        #                     "process_name": "bgp",
        #                     "restart_count": 12,
        #                     "sap": 308,
        #                     "state": "SRV_STATE_HANDSHAKED",
        #                     "state_start_date": "Thu Aug 20 05:49:00 2020",
        #                     "uuid": "0x11B"
        #                 }
        #             }
        #         }
        #     }
        # }
        sap_id = out.q.contains(service).get_values('sap', 0)
        if not sap_id:
            raise Exception("Couldn't get sap id")
    except SchemaEmptyParserError:
        return ''

    # enable backtrace
    # example:
    # R3_nx# debug service-core sap 308 frame-count 6
    # Setting setting frame count 6 for sap 308
    if module:
        out = device.execute(
            'debug service-core module {m} sap {sap} frame-count {fc}'.format(
                m=module, sap=sap_id, fc=frame_count))
    else:
        out = device.execute(
            'debug service-core sap {sap} frame-count {fc}'.format(
                sap=sap_id, fc=frame_count))

    return out
