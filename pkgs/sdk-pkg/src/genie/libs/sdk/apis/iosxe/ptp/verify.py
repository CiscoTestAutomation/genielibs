"""Common verify functions for ptp"""

# Python
import logging
from netaddr import IPNetwork
# pyats
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_ptp_states(
    device, interfaces,states, max_time=15, check_interval=5
):
    """ Verify ptp state convergence in show ptp port interface 
        Args:
            device ('obj'): Device object
            interface ('list'): PTP interface
            states ('list'): Expected states
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        for intf in interfaces:
            try:
                out = device.parse("show ptp port {intf}".format(intf=intf))
            except SchemaEmptyParserError:
                pass
            if out:
                port_state = out['ptp_port_dataset']['port_info']['state']
                log.info("PTP value fetched from output {port_state}".format(port_state=port_state))
                if port_state:
                    if port_state in states:
                        result = True
                    else:
                        result = False

        if result:
            return True
        timeout.sleep()            
    return False

def verify_ptp_platform_fed_results(
    device, interfaces, states, clock_mode, delay_mech, domain, profile, max_time=15, check_interval=5
):

    """ Verify ptp fed values in show ptp fed command
        Args:
            device ('obj'): Device object
            interfaces ('list'): PTP interfaces
            states ('list'): Expected states
            clock_mode ('str'): Clock mode
            delay_mech ('str'): PTP delay mechanism
            domain ('int'): PTP domain
            profile ('str'): PTP profile
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval ('int'): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        result = False
        for intf in interfaces:
            try:
                out = device.parse("show platform software fed switch active ptp interface {intf}".format(intf=intf))
            except SchemaEmptyParserError:
                pass
            if out:
                port_state = out['interface']['port_info']['state']
                dom = out['interface']['domain_value']
                clock = out['interface']['clock_mode']
                prof = out['interface']['profile_type']
                delay = out['interface']['delay_mechanism']
                if (port_state in states) and (int(dom) == int(domain)) and (clock == clock_mode) and \
                    (prof == profile) and (delay == delay_mech):
                    result = True
                else:
                    result = False

        if result:
            return True
        timeout.sleep()            
    return False

def verify_ptp_clock(
    device, device_type, domain, priority1, priority2, offset, dscp_event=59, 
    dscp_general=47, max_time=15, check_interval=5
):

    """ Verify ptp clock values in show ptp clock command
        Args:
            device ('obj'): Device object
            device_type ('str'): Clock type
            domain ('int'): PTP domain
            priority1 ('str'): PTP priority1
            priority2 ('str'): PTP priority2
            offset ('list'): PTP offset from master
            dscp_event ('int'): PTP ip dscp event message (default value is 59)
            dscp_general ('int'): PTP ip dscp general message ( default value is 47)
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval ('int'): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ptp clock")
        except SchemaEmptyParserError:
            pass
        if out:
            dev_type = out['ptp_clock_info']['device_type']
            dom = out['ptp_clock_info']['clock_domain']
            prio1 = out['ptp_clock_info']['priority1']
            prio2 = out['ptp_clock_info']['priority2']
            off = out['ptp_clock_info']['offset_from_master']
            eve = out['ptp_clock_info']['message_event_ip_dscp']
            gen = out['ptp_clock_info']['message_general_ip_dscp']
            if (dev_type.lower() == device_type.lower()) and (int(dom) == int(domain)) and \
                    (int(prio1) == int(priority1)) and (int(prio2) == int(priority2)) and \
                    (int(off) <= int(offset)) and (int(eve) == int(dscp_event)) and \
                    (int(gen) == int(dscp_general)):
                result = True
            else:
                result = False

        if result:
            return True
        timeout.sleep()            
    return False

def verify_ptp_counters(
    device, interfaces, sync_trans, follow_trans, sync_recv, follow_recv, max_time=15, check_interval=5
):

    """ Verify ptp fed counter values in show ptp fed command
        Args:
            device ('obj'): Device object
            interfaces ('list'): PTP interfaces
            sync_trans ('list'): Sync messages transmitted
            follow_trans ('int'): Follow up messages transmitted
            sync_recv ('list'): Sync messages received
            follow_recv ('str'): Follow up messages received
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        result = False
        for intf in interfaces:
            try:
                out = device.parse("show platform software fed switch active ptp interface {intf}".format(intf=intf))
            except SchemaEmptyParserError:
                pass
            if out:
                sync_t = out['interface']['num_info']['num_sync_messages_transmitted']
                follow_t = out['interface']['num_info']['num_followup_messages_transmitted']
                sync_r = out['interface']['num_info']['num_sync_messages_received']
                follow_r = out['interface']['num_info']['num_followup_messages_received']
                if (int(sync_t) <= int(sync_trans)) and (int(follow_t) <= int(follow_trans)) and (int(sync_r) <= int(sync_recv)) and \
                    (int(follow_r) <= int(follow_recv)):
                    result = True
                else:
                    result = False

        if result:
            return True
        timeout.sleep()            
    return False

def verify_ptp_parent(
    device, priority1, priority2, max_time=15, check_interval=5
):

    """ Verify ptp parent values in show ptp parent command
        Args:
            device (`obj`): Device object
            priority1 ('str'): PTP priority1
            priority2 ('str'): PTP priority2
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ptp parent")
        except SchemaEmptyParserError:
            pass
        if out:
            parent_id = out['ptp_parent_property']['parent_clock']['identity']
            gm_id = out['ptp_parent_property']['grandmaster_clock']['identity']
            prio1 = out['ptp_parent_property']['grandmaster_clock']['priority1']
            prio2 = out['ptp_parent_property']['grandmaster_clock']['priority2']
            if (parent_id[0] != None) and (gm_id[0] != None):
                result = True
            else:
                result = False

        if result:
            return True
        timeout.sleep()            
    return False

def verify_ptp_calibration_states(
    device, states, domain, max_time=15, check_interval=5
):

    """ Verify ptp parent values in show ptp parent command
        Args:
            device (`obj`): Device object
            states ('str): PTP calibration state
            domain ('str): PTP domain
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ptp brief | ex FA")
        except SchemaEmptyParserError:
            pass
        if out:
            result = True
        else:
            result = False

        if result:
            return True
        timeout.sleep()
    return False
