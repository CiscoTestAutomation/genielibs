"""Common configure functions for interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_local_span_source(device, session_id, int_type, span_port, direction=''):
    """ configure locl span source interface
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            int_type('str'): SPAN source {VLAN|interface}
            span_port('str'): SPAN source interface/VLAN ID
            direction('str'): MONITOR (TRANSMIT/RECEIVE/BOTH) TRAFFIC, Default=both
                ex:)
                    both  Monitor received and transmitted traffic
                    rx    Monitor received traffic only
                    tx    Monitor transmitted traffic only
                    <cr>  <cr> 
    """
    if int_type in ('interface','vlan'):
        if direction:
            cmd = f"monitor session {session_id} source {int_type} {span_port} {direction}\n"
        else:
            cmd = f"monitor session {session_id} source {int_type} {span_port}"
    else:
         raise ValueError("Incorrect argument for int_type, Expected: vlan or Interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local_span_source. Error:\n{error}".format(error=e)
        )

def configure_local_span_destination(device, session_id, span_port, encapsulation=None,
                                     ingress=None, vlan_id=None):
    """ configure locl span destination interface
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            span_port ('str'): SPAN destination interface
            encapsulation ('str'): (dot1q|replicate|default=None)
            ingress ('str'): (dot1q|untagged|vlan|default=None)
            vlan_id ('int'): default=None
    """
    cmd = ""
    if encapsulation in ('dot1q','replicate'):
        if ingress in ('dot1q', 'untagged'):
            cmd = f"monitor session {session_id} destination interface {span_port} " \
                  f"encapsulation {encapsulation} ingress {ingress} vlan {vlan_id}\n"

        elif ingress == 'vlan':
            cmd = f"monitor session {session_id} destination interface {span_port} " \
                  f"encapsulation {encapsulation} ingress vlan {vlan_id}\n"
        else:
            cmd = f"monitor session {session_id} destination interface {span_port} " \
                  f"encapsulation {encapsulation}\n"
    else:
        if ingress in ('dot1q', 'untagged'):
            cmd = f"monitor session {session_id} destination interface {span_port} " \
                  f"ingress {ingress} vlan {vlan_id}\n"

        elif ingress == 'vlan':
            cmd = f"monitor session {session_id} destination interface {span_port} " \
                  f"ingress vlan {vlan_id}\n"
        else:
            cmd = f"monitor session {session_id} destination interface {span_port}\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local_span_destination. Error:\n{error}".format(error=e)
        )

def remove_all_span(device):
    """ Remove all SPAN sessions in the box
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no monitor session all")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove monitor session. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_local_span_source(device, session_id, int_type, span_port, direction=''):
    """ unconfigure locl span source interface
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            int_type('str'): SPAN source {VLAN|interface}
            span_port('str'): SPAN source interface/VLAN ID
            direction('str'): MONITOR (TRANSMIT/RECEIVE/BOTH) TRAFFIC, Default=both
                ex:)
                    both  Monitor received and transmitted traffic
                    rx    Monitor received traffic only
                    tx    Monitor transmitted traffic only
                    <cr>  <cr> 
    """
    if int_type in ('interface','vlan'):
        if direction:
            cmd = f"no monitor session {session_id} source {int_type} {span_port} {direction}\n"
        else:
            cmd = f"no monitor session {session_id} source {int_type} {span_port}"
    else:
         raise ValueError("Incorrect argument for int_type, Expected: vlan or Interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure local_span_source. Error:\n{error}".format(error=e)
        )

def unconfigure_local_span_destination_interface(device, session_id, int_type, span_port ):
    """ unconfigure locl span destination interface
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            int_type('str'): SPAN source {VLAN|interface}
            span_port('str'): SPAN source interface/VLAN ID
    """
    cmd = ""
    if int_type == 'interface':
        cmd = f"no monitor session {session_id} destination interface {span_port}\n"
    elif int_type== 'vlan':
        cmd = f"no monitor session {session_id} destination remote vlan {span_port}\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local_span_destination interface. Error:\n{error}".format(error=e)
        )

def configure_local_span_filter(device, session_id, access_control_rule, access_list='', vlan_id=''):
    """ Configure local span filter
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            access_control_rule('str'): SPAN filter access control rule (eg. ip,ipv6,mac,vlan)
            access_list('str',optional): The name of access control list
            vlan_id('int', optional): SPAN source vlan number (eg. 1-4094)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring local span filter.
    """
    if access_control_rule in ('ip', 'ipv6', 'mac', 'vlan'):
        if vlan_id:
            cmd = f"monitor session {session_id} filter {access_control_rule} {vlan_id}"
        elif access_list:
            cmd = f"monitor session {session_id} filter {access_control_rule} access-group {access_list}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure local span filter. Error:\n{e}"
        )

def unconfigure_local_span_filter(device, session_id, access_control_rule, access_list='', vlan_id=''):
    """ Unconfigure local span filter
        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            access_control_rule('str'): SPAN filter access control rule (eg. ip,ipv6,mac,vlan)
            access_list('str'): The name of access control list
            vlan_id('int', optional): SPAN source vlan number (eg. 1-4094)
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring local span filter
    """
    if access_control_rule in ('ip', 'ipv6', 'mac', 'vlan'):
        if vlan_id:
            cmd = f"no monitor session {session_id} filter {access_control_rule} {vlan_id}"
        elif access_list:
            cmd = f"no monitor session {session_id} filter {access_control_rule} access-group {access_list}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure local span filter. Error:\n{e}"
        )


def configure_interface_monitor_session_shutdown_erspan_dest(device, session_name):
    """ configure monitor session on device by doing shut of the erspan destination interface
        Args:
            device ('obj'): Device object
            session_name ('str'): Session name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"monitor session {session_name} type erspan-destination")
    configs.append(f"shutdown")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to shut on erspan destination monitor session  :\n{e}"
        )  

def configure_interface_monitor_session_mtu(device, session_name, mtu):
    """ configure monitor session on device by setting destination mtu
        Args:
            device ('obj'): Device object
            session_name ('str'): Session name
            mtu ('str'): mtu size, (196-9000)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"monitor session {session_name} type erspan-source")
    configs.append(f"destination")
    configs.append(f"mtu {mtu}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure mtu on erspan monitor session :\n{e}"
        ) 


def configure_interface_monitor_session_no_mtu(device, session_name, mtu):
    """ configure monitor session on device by setting destination no mtu
        Args:
            device ('obj'): Device object
            session_name ('str'): Session name
            mtu ('str'): mtu size, (196-9000)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append(f"monitor session {session_name} type erspan-source")
    configs.append(f"destination")
    configs.append(f"no mtu {mtu}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure no mtu on erspan monitor session :\n{e}"
        ) 


def config_erspan_monitor_session_shut_unshut(device, session_number, action):

     """ Configure erspan monitor session shutdown
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
             action ('str'): 'shutdown' or 'no shutdown'

         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"monitor session {session_number} type erspan-source")
     configs.append(f"{action}")


     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to shut/unshut erspan monitor session :\n{e}"
         )
       
        
def unconfig_erspan_monitor_session_no_source(device, session_number, interface='', vlan=''):

     """ Configure no source on erspan monitor session 
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
             interface ('str') :{optional} source interface name, either "interface" or "vlan" is mandatory
             vlan ('str'): {optional} source vlan number, either "interface" or "vlan" is mandatory         

         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"monitor session {session_number}  type erspan-source")
     if interface!='':
        configs.append(f"no source interface {interface}")
     if vlan!='':
        configs.append(f"no source vlan {vlan}")

     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure no source on erspan monitor session :\n{e}"
         )
    

def unconfig_erspan_monitor_session_no_filter(device, session_number, vlan):

     """ Configure no filter on erspan monitor session 
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
             vlan ('str'): sorce vlan number         

         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"monitor session {session_number} type erspan-source")
     configs.append(f"no filter vlan {vlan}")

     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure  no filter on erspan monitor session :\n{e}"
         )

def config_erspan_monitor_session_filter(device, session_number, vlan):

     """ Configure filter on erspan monitor session 
         Args:
             device ('obj'): Device object
             session_number ('int'): session number
             vlan ('str'): sorce vlan number         

         Returns:
             None
         Raises:
             SubCommandFailure
     """
     configs = []
     configs.append(f"monitor session {session_number} type erspan-source")
     configs.append(f"filter vlan {vlan}")

     try:
         device.configure(configs)
     except SubCommandFailure as e:
         raise SubCommandFailure(
             f"Failed to configure filter on erspan monitor session :\n{e}"
         )

def configure_remote_span_on_vlan(device, vlan):
    """ Configure RSPAN on vlan
        Args:
            device ('obj'): Device object
            vlan ('str'): vlan number
        Returns:
            None
        Raises:
            SubCommandFailure
        Description:
            configure RSPAN on vlan for remote monitor session configurations
    """
    configs = []
    configs.append(f"vlan {vlan}")
    configs.append(f"remote-span")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure RSPAN on vlan {vlan} :\n{e}"
        )

def configure_source_destination_remote_vlan(device, session_id, direction,vlan):
    """ configure source destination remote vlan
        Args:
            device (`obj`): Device object
            session_id ('int'): RSPAN session number
            direction('str'): RSPAN {source|destination}
            vlan('str'): SPAN source /destination remote VLAN ID
        Returns:
            None
        Raises:
            SubCommandFailure
        Description:
            configure source destination remote vlan
    """
    cmd = ""
    if direction == 'source':
        cmd = f"monitor session {session_id} source remote vlan {vlan}\n"
    elif direction == 'destination':
        cmd = f"monitor session {session_id} destination remote vlan {vlan}\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure source destination remote vlan. Error:\n{error}".format(error=e)
        )

def unconfigure_source_destination_remote_vlan(device, session_id, direction,vlan):
    """ unconfigure source destination remote vlan
        Args:
            device (`obj`): Device object
            session_id ('int'): RSPAN session number
            direction('str'): RSPAN {source|destination}
            vlan('str'): SPAN source /destination remote VLAN ID
        Returns:
            None
        Raises:
            SubCommandFailure
        Description:
            configure source destination remote vlan
    """
    cmd = ""
    if direction == 'source':
        cmd = f"no monitor session {session_id} source remote vlan {vlan}\n"
    elif direction == 'destination':
        cmd = f"no monitor session {session_id} destination remote vlan {vlan}\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure source destination remote vlan. Error:\n{error}".format(error=e)
        )


def configure_local_span_source_and_get_output(
        device, session_id, int_type, span_port, direction=''):
    """ Configure local span source interface and get output

        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            int_type ('str'): SPAN source {VLAN|interface}
            span_port ('str'): SPAN source interface/VLAN ID
            direction ('str'): MONITOR (TRANSMIT/RECEIVE/BOTH) TRAFFIC,
                Default=both
                ex:)
                    both  Monitor received and transmitted traffic
                    rx    Monitor received traffic only
                    tx    Monitor transmitted traffic only
                    <cr>  <cr>
        Returns:
            str: stripped output string of configure command
                ex:)
                    format1: Only NGIO switch is supported for Local SPAN.
                        SPAN Session Validation failed.
                    format2: % Interface(s) Gi0/1/5 already configured
                        as monitor destinations
        Raises:
            SubCommandFailure
            ValueError: when ``int_type`` is neither ``interface`` nor ``vlan``
    """
    if int_type in ('interface', 'vlan'):
        if direction:
            cmd = (f"monitor session {session_id} source {int_type} "
                   f"{span_port} {direction}\n")
        else:
            cmd = (f"monitor session {session_id} source {int_type} "
                   f"{span_port}")
    else:
        raise ValueError(
            "Incorrect argument for int_type, "
            "Expected: vlan or interface")
    try:
        output = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local span source. "
            "Error:\n{error}".format(error=e))
    return output.strip()


def configure_local_span_destination_and_get_output(
        device, session_id, span_port, encapsulation=None,
        ingress=None, vlan_id=None):
    """ Configure local span destination interface and get output

        Args:
            device (`obj`): Device object
            session_id ('int'): SPAN session number
            span_port ('str'): SPAN destination interface
            encapsulation ('str'): (dot1q|replicate|default=None)
            ingress ('str'): (dot1q|untagged|vlan|default=None)
            vlan_id ('int'): default=None
        Returns:
            str: stripped output string of configure command
                ex:)
                    format1: Only NGIO switch is supported for Local SPAN.
                        SPAN Session Validation failed.
                    format2: % Interface(s) Gi0/1/5 already configured
                        as monitor destinations
        Raises:
            SubCommandFailure
    """
    cmd = f"monitor session {session_id} destination interface {span_port}"
    if encapsulation in ('dot1q', 'replicate'):
        cmd += f" encapsulation {encapsulation}"
    if ingress in ('dot1q', 'untagged'):
        cmd += f" ingress {ingress} vlan {vlan_id}"
    elif ingress == 'vlan':
        cmd += f" ingress vlan {vlan_id}"
    try:
        output = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local span destination. "
            "Error:\n{error}".format(error=e))
    return output.strip()


def configure_local_span_and_verify_output(
        device, session_id, span_port, int_type='interface', direction='',
        encapsulation=None, ingress=None, vlan_id=None,
        role='source', validation_code=0):
    """ Config span session, and verify the session validation result

        Args:
            device ('obj'): Device object
            session_id ('int'): SPAN session number
            span_port ('str'): SPAN source interface/VLAN ID
            int_type ('str'): SPAN source {VLAN|interface}
            direction ('str'): MONITOR (TRANSMIT/RECEIVE/BOTH) TRAFFIC,
                Default=both
                ex:)
                    both  Monitor received and transmitted traffic
                    rx    Monitor received traffic only
                    tx    Monitor transmitted traffic only
                    <cr>  <cr>
            encapsulation ('str'): (dot1q|replicate|default=None)
            ingress ('str'): (dot1q|untagged|vlan|default=None)
            vlan_id ('int'): default=None
            role ('str'): Role of the span session,
                          'source' or 'destination'
            validation_code ('int'): Expected span session validation code:
                0:  Validation pass
                1:  Exceed the maximum source port number
                2:  Only one Dst port is supported
                3:  Port already configured as monitor sources
                4:  Port already configured as monitor destinations
                5:  Src port is already be used in session
                6:  Dst port is already be used in session
                7:  Exceed the maximum SPAN session number
                8:  Only NGIO switch is supported
                -1: Unknown reason
        Returns:
            True/False
    """
    if role == 'source':
        output = device.api.configure_local_span_source_and_get_output(
            session_id=session_id,
            int_type=int_type,
            span_port=span_port,
            direction=direction)
    elif role == 'destination':
        output = device.api.configure_local_span_destination_and_get_output(
            session_id=session_id,
            span_port=span_port,
            encapsulation=encapsulation,
            ingress=ingress,
            vlan_id=vlan_id)
    else:
        log.debug(f'Incorrect role {role}, expected source or destination')
        return False

    validation_msg_dict = {
        0: 'Validation pass',
        1: 'Exceed the maximum source port number',
        2: 'Only one Dst port is supported',
        3: 'Port already configured as monitor sources',
        4: 'Port already configured as monitor destinations',
        5: 'Src port is already be used in session',
        6: 'Dst port is already be used in session',
        7: 'Exceed the maximum SPAN session number',
        8: 'Only NGIO switch is supported',
        -1: 'Unknown reason',
    }
    output_lower = (output or '').strip().lower()

    if 'validation failed' not in output_lower and '%' not in output_lower:
        actual_reason_code = 0
    elif 'maximum source port' in output_lower:
        actual_reason_code = 1
    elif ('only' in output_lower
          and 'dst port is supported' in output_lower):
        actual_reason_code = 2
    elif 'already configured as monitor sources' in output_lower:
        actual_reason_code = 3
    elif 'already configured as monitor destinations' in output_lower:
        actual_reason_code = 4
    elif 'already be used in session' in output_lower:
        if 'src port' in output_lower:
            actual_reason_code = 5
        elif 'dst port' in output_lower:
            actual_reason_code = 6
        else:
            actual_reason_code = -1
    elif 'exceed the maximum span session number' in output_lower:
        actual_reason_code = 7
    elif 'only ngio switch is supported' in output_lower:
        actual_reason_code = 8
    else:
        actual_reason_code = -1

    log.debug(
        f'Parsed reason code: {actual_reason_code}, reason message: '
        f'({validation_msg_dict.get(actual_reason_code)})')
    if actual_reason_code != validation_code:
        log.debug(
            'Verify config local span session failed, '
            f'expected reason code: {validation_code} '
            f'actual reason code: {actual_reason_code}')
        return False
    return True
