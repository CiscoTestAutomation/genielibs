# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def get_boot_variables(device, boot_var, output=None):
    '''Get current or next-reload boot variables on the device
        Args:
            device (`obj`): Device object
            boot_var (`str`): Type of boot variable to return to caller
            output (`str`): output from show boot
        Returns:
            List of boot images or []
    '''

    # Check type
    assert boot_var in ['current', 'next']

    boot_images = []
    try:
        boot_out = device.parse("show boot", output=output)
    except SchemaEmptyParserError as e:
        log.error("Command 'show boot' did not return any output\n{}".\
                  format(str(e)))
    else:
        # Get current or next
        if boot_var == 'current':
            if boot_out.get("active", {}):
                boot_variables = boot_out.get("active", {}).get("boot_variable")
                log.info(f"Boot images set using boot_variable on active device: {boot_variables}")
            else:
                for each in ["current_boot_variable", "boot_variable"]:
                    if boot_out.get(each):
                        boot_variables = boot_out.get(each)
                        log.info(f"Boot images set using {each} -> {boot_variables}")
                        break
                
        else:
            if boot_out.get("active", {}):
                boot_variables = boot_out.get("active", {}).get("boot_variable")
                log.info(f"Boot images set using boot_variable on active device: {boot_variables}")
            else:
                for each in ["next_reload_boot_variable", "boot_variable"]:
                    if boot_out.get(each):
                        boot_variables = boot_out.get(each)
                        log.info(f"Boot images set using {each} -> {boot_variables}")
                        break

            if boot_variables is None:
                boot_variables = boot_out.get("next_reload_boot_variable")
                log.info(f"Boot images set using next_reload_boot_variable -> {boot_variables}")

        # Trim
        if boot_variables:
            for item in boot_variables.split(';'):
                if not item:
                    continue
                if ',' in item:
                    item, num = item.split(',')
                if " " in item:
                    item, discard = item.split(" ")
                boot_images.append(item)

    return boot_images


def get_fabric_ap_state(device, ap_name):
    """Get fabric ap state
    Args:
        device (obj): Device object
        ap_name (str): accesspoint name
    Returns:
        ap state (str) if success else empty string
    Raises:
        N/A        
    """
    ap_state = ""
    try:
        fabric_ap_summary = device.parse('show fabric ap summary')
        if fabric_ap_summary.get('ap_name').get(ap_name):
            ap_state = fabric_ap_summary.get('ap_name').get(ap_name).get('state')

    except (SchemaEmptyParserError) as e:
        log.error("Failed to get ap state from 'show fabric ap summary': Error: {e}".format(e=str(e)))
        return ""
    return ap_state


def get_lisp_session_state(device,peer_ip):
    """Get lisp session state
    Args:
        device (obj): Device object
        peer_ip(str): Peer IP
    Returns:
        Peer state (str) if success else empty string
    Raises:
        N/A
    """
    lisp_session_state = []
    ip_lst = []
    try:
        show_lisp_session = device.parse('show lisp session established')
        if show_lisp_session.get('vrf').get('default'):
            lisp_peer = show_lisp_session.get('vrf').get('default').get('peers')
    except (SchemaEmptyParserError) as e:
        log.error("Failed to get lisp session peers from 'show lisp session established': Error: {e}".format(e=str(e)))
        return ""

    keys = lisp_peer.keys()

    for i in keys:
        if peer_ip in i:
            ip_lst.append(i)
    if peer_ip in ip_lst:
        for j in range(len(lisp_peer[peer_ip])):
            state = lisp_peer[peer_ip][j]['state']
            lisp_session_state.append(state)

        return lisp_session_state

def get_ap_ip(device,ap_name):
    """Get Access Point IP
    Args:
        device (obj): Device object
        ap_name(str): AP Name       
    Returns:
        ap ip (str) if success else empty string
    Raises:
        N/A        
    """
    ap_ip = ""
    try:
        show_tunnel = device.parse('show access-tunnel summary')
        if show_tunnel.get('name').get(ap_name):
            ap_ip = show_tunnel.get('name').get(ap_name).get('ap_ip')
    except (SchemaEmptyParserError) as e:
        log.error("Failed to get assess point IP from 'show access-tunnel summary': Error: {e}".format(e=str(e)))
        return ""
    return ap_ip


def get_rloc_ip(device,ap_name):
    """Get rloc IP
    Args:
        device (obj): Device object
        ap_name(str): AP Name
    Returns:
        aloc ip (str) if success else empty string
    Raises:
        N/A        
    """
    rloc_ip = ""
    try:
        show_tunnel = device.parse('show access-tunnel summary')
        if show_tunnel.get('name').get(ap_name):
            rloc_ip = show_tunnel.get('name').get(ap_name).get('rloc_ip')
    except (SchemaEmptyParserError) as e:
        log.error("Failed to get rloc ip from 'show access-tunnel summary': Error: {e}".format(e=str(e)))
        return ""
    return rloc_ip


def get_matching_line_processes_platform(device,process):
    """Get matching lines from show processes platform
    Args:
        device (obj): Device object
        process(str): Name of process
        
    Returns:
        matching lines (str) if success else empty string
    Raises:
        N/A        
    """
    matching_line = ""
    try:
        no_of_matching_line = device.parse('show processes platform | count {}'.format(process))
        if no_of_matching_line:
            matching_line = no_of_matching_line.get('number_of_matching_lines')

    except (SchemaEmptyParserError) as e:
        log.error("Failed to get matching lines from 'show processes platform': Error: {e}".format(e=str(e)))
        return ""
    return matching_line


def get_matching_line_platform_software(device,process):
    """Get matching lines from show platform software process
    Args:
        device (obj): Device object
        process(str): Name of process
        
    Returns:
        matching lines (str) if success else empty string
    Raises:
        N/A        
    """
    matching_line = ""
    try:
        no_of_matching_line = device.parse('show platform software process slot sw standby r0 monitor | count {}'.format(process))
        if no_of_matching_line:
            matching_line = no_of_matching_line.get('number_of_matching_lines')

    except (SchemaEmptyParserError) as e:
        log.error("Failed to get matching lines from 'show platform software process slot sw standby r0 monitor': Error: {e}".format(e=str(e)))
        return ""
    return matching_line


def get_processes_platform_dict(device,process):
    """Get processes platform dict
    Args:
        device (obj): Device object
        process(str): Name of process

    Returns:
        processes_platform_dict(str) if success else empty string
    Raises:
        N/A        
    """
    processes_platform_dict = ""
    try:
        processes_platform_dict = device.parse('show processes platform | include {}'.format(process))
        if processes_platform_dict:
            return processes_platform_dict 

    except (SchemaEmptyParserError) as e:
        log.error("Failed to parse from 'show processes platform': Error: {e}".format(e=str(e)))
        return ""


def get_platform_software_dict(device,process):
    """Get platform software dict
    Args:
        device (obj): Device object
        process(str): Name of process

    Returns:
        platform_software_dict(str) if success else empty string
    Raises:
        N/A        
    """
    platform_software_dict = ""
    try:
        platform_software_dict = device.parse('show platform software process slot sw standby r0 monitor | include {}'.format(process))
        if platform_software_dict:
            return platform_software_dict

    except (SchemaEmptyParserError) as e:
        log.error("Failed to get matching lines from 'show platform software process slot sw standby r0 monitor': Error: {e}".format(e=str(e)))
        return ""
