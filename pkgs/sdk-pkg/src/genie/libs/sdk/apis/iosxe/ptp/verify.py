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
                port_state = out.q.get_values("Port_state")[0]
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
                port_state = out.q.get_values("Port_state")[0]
                dom = out.q.get_values("domain_value")[0]
                clock = out.q.get_values("Clock_Mode")[0]
                prof = out.q.get_values("Profile_Type")[0]
                delay = out.q.get_values("Delay_mechanism")[0]
                if (port_state in states) and (dom == domain) and (clock == clock_mode) and \
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
            dev_type = out.q.get_values("PTP_Device_Type")[0]
            dom = out.q.get_values("Clock_Domain")[0]
            prio1 = out.q.get_values("Priority1")[0]
            prio2 = out.q.get_values("Priority2")[0]
            off = out.q.get_values("Offset_From_Master")
            eve = out.q.get_values("Message_event_ip_dscp")[0]
            gen = out.q.get_values("Message_general_ip_dscp")[0]

            if (dev_type.lower() == device_type.lower()) and (dom == domain) and \
                    (prio1 == priority1) and (prio2 == priority2) and \
                    (off[0] <= offset) and (int(eve) == int(dscp_event)) and \
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
                sync_t = out.q.get_values("num_sync_messages_transmitted")[0]
                follow_t = out.q.get_values("num_followup_messages_transmitted")[0]
                sync_r = out.q.get_values("num_sync_messages_received")[0]
                follow_r = out.q.get_values("num_followup_messages_received")[0]
                if (sync_t <= sync_trans) and (follow_t <= follow_trans) and (sync_r <= sync_recv) and \
                    (follow_r <= follow_recv):
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
            parent_id = out.q.get_values("Parent_Clock_Identity")[0]
            gm_id = out.q.get_values("Grandmaster_Clock_Identity")[0]
            prio1 = out.q.get_values("Priority1")[0]
            prio2 = out.q.get_values("Priority2")[0]
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

