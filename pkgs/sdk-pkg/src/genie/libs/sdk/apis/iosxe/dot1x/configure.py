import logging
import re
from genie.libs.parser.utils.common import Common
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)

log = logging.getLogger(__name__)

def source_configured_template(device, interface, template_name):
    """Source template config
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            template (`str`): Built-in/User defined template Name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to source a configured template
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = ''
    cmd += 'interface {}\n'.format(converted_interface)
    cmd += 'source template {}'.format(template_name)
    log.info("Assign template {tmp} on {intf}".format(tmp=template_name, intf=converted_interface))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not source a configured template {}.Error: {}".format(template_name, str(e))
        )

def configure_dot1x_cred_profile(device, profile_name, user_name, passwd):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
            username (`str`): username for dot1x user
            passwd (`str`): password in plain text
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = ''
    cmd += 'dot1x credentials {}\n'.format(profile_name)
    cmd += 'username {}\n'.format(user_name)
    cmd += 'password {}\n'.format(passwd)
    log.info("configure dot1x credential")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile {}.Error: {}".format(profile_name, str(e))
        )

def configure_eap_profile(device, profile_name,method='md5'):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
            method ('str',optional). Method to use for eap authentication. Default is md5
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = ''
    cmd += 'eap profile {}\n'.format(profile_name)
    cmd += 'method {}\n'.format(method)
    log.debug("Configure eap profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure eap profile {}.Error: {}".format(profile_name, str(e))
        )

def unconfigure_eap_profile(device, profile_name):
    """Unconfigure EAP Profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = 'no eap profile {}\n'.format(profile_name)
    log.info("Unconfigure eap profile {}".format(profile_name))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure profile: {profile_name}".format(profile_name=profile_name)
        )

def configure_eap_profile_md5(device, profile_name):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = ''
    cmd += 'eap profile {}\n'.format(profile_name)
    cmd += 'method md5\n'
    log.info("configure eap md5 profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure eap md5 profile {}.Error: {}".format(profile_name, str(e))
        )

def configure_dot1x_supplicant(device, interface, cred_profile_name=None, eap_profile=None,auth_port_control=None):
    """Configure switch as dot1x supplicant/client
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str`,optional): dot1x credential profile name
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_port_control ('str',optional): Port control type (i.e auto, force-authorized)
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure eap md5 profile
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = ''
    cmd += 'interface {}\n'.format(converted_interface)
    cmd += 'dot1x pae supplicant\n'

    if cred_profile_name:
        cmd += 'dot1x credentials {cred_profile_name}\n'.format(cred_profile_name=cred_profile_name)

    if eap_profile is not None:
        cmd += 'dot1x supplicant eap profile {}\n'.format(eap_profile)

    if auth_port_control:
        cmd += 'authentication port-control {auth_port_control}\n'.format(auth_port_control=auth_port_control)

    log.info("configure dot1x supplicant")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure dot1x_supplicant on {}.Error: {}".format(converted_interface, str(e))
        )

def configure_mode_to_eEdge(device):
    """ Convert the configuration mode to eEdge
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to Convert the configuration mode to eEdge
    """
    cmd = 'authentication convert-to new-style forced'
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy',out)
    if matchout is not None:
        log.info("convert-to new-style")
        try:
             device.configure(cmd)
        except SubCommandFailure as e:
             raise SubCommandFailure(
                 "Failed to Convert the configuration mode to eEdge monitor.Error: {}".format(str(e))
            )
    else:
        log.info('switch is already configured in new-style')

def enable_autoconf(device):
    """ Enable autoconf
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable autoconf
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'autoconf enable\n'
    else:
        cmd = ''
        cmd += 'autoconf enable\n'

    log.info("Enable autoconf")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable autoconf.Error: {}".format(str(e))
        )

def configure_access_session_monitor(device):
    """ Enable access-session  monitor
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable access-session monitor
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'access-session monitor\n'
    else:
        cmd = ''
        cmd += 'access-session monitor\n'
        
    log.info("Configure access-session monitor")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable access-session monitor.Error: {}".format(str(e))
        )

def configure_access_session_sticky(device, timer):
    """ configure interface-template sticky timer
        Args:
            device ('obj'): device to use
            timer (int): <1-65535>  Enter a value between 1 and 65535
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure interface-template sticky timer
    """
    out = device.execute('authentication display config-mode')
    matchout = re.search('legacy', out)
    if matchout is not None:
        log.info('Switch is in legacy mode, converting to new-style')
        cmd = ''
        cmd += 'authentication convert-to new-style forced\n'
        cmd += 'access-session interface-template sticky timer {}\n'.format(timer)
    else:
        cmd = ''
        cmd += 'access-session interface-template sticky timer {}\n'.format(timer)
        
    log.info("Configure interface-template sticky timer")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure access-session sticky timer on {}.Error: {}".format(timer, str(e))
        )

def enable_dot1x_sysauthcontrol(device):
    """ Globally enables 802.1X port-based authentication.
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable 802.1X port-based authentication.
    """
    log.info("Enables 802.1X port-based authentication")
    cmd = ""
    cmd += "dot1x system-auth-control\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable dot1x system auth-control.Error: {}".format(str(e))
        )

def clear_access_session(device):
    """ executes clear access-sesssion CLI 
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to execute clear access-sesssion.
    """
    cmd = ""
    cmd += "clear access-session\n"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute clear access-sesssion.Error: {}".format(str(e))
        )

def config_identity_ibns(device, interface, policy_map, access=True, port_control='auto', **kwargs):
    """ Configured 802.1x port based authentication for
        IBNS2.0 with service policy
    Mandatory args:
            device ('obj'): device to use
            interface (`str`): Interface name
            access(bol): Set to True, False to configure in Trunk mode
            Policy_map: Name of policy map to be attached.
    Optional args:
        data_vlan(`int`): vlan_id for data traffic
        voice_vlan(`int`): vlan_id for voice traffic
        max_req:(`int`) Max No. of Retries
        max-reauth-req(`int`): Max No. of Reauthentication Attempts
        authmod('str'): default(multi-auth), mult-host peer, multi-domain etc
        closed('bol'):  {False: closed | True: open (default) }
        reauth('str'):  server or numberic range is 1 to 65535 seconds
        ctr('str'): {both | in}
        txp(`int`):The range is 1 to 65535 seconds
        port_control ('str'): {auto|force-authorized|force-unauthorized}. Default = 'auto'
    Returns:
            None
    Raises:
            SubCommandFailure: Failed to configure 802.1x port based authentication
    """
    dict1 = {}
    #For IBNS2.0  access-session is in Open mode (default)
    dict1['open'] = True
    #For IBNS2.0 default access-session host-mode is in multi-auth (default)
    dict1['authmod'] ='multi-auth'
    
    converted_interface = Common.convert_intf_name(interface)
    cmd = " "
    cmd += 'interface {}\n'.format(converted_interface)

    if access:
        cmd += "switchport\n"
        cmd += "switchport mode access\n"
    else:
        cmd += "switchport\n"
        cmd += "switchport mode trunk\n"
    cmd += "access-session port-control {port_control}\n".format(port_control=port_control)
    cmd += "authentication periodic\n"
    cmd += "mab\n"
    cmd += "dot1x pae authenticator\n"
    
    for key, value in kwargs.items():
        if type(value) == str:
            dict1[key] = value.lower()
        else:
            dict1[key] = value

    if 'data_vlan' in dict1:
       cmd += "switchport access vlan {}\n".format(dict1['data_vlan'])

    if 'voice_vlan' in dict1:
       cmd += "switchport voice vlan {}\n".format(dict1['voice_vlan'])

    if 'max_req'in dict1:
        cmd += "dot1x max-req {}\n".format(dict1['max_req'])

    if 'max_reauth_req'in dict1:
        cmd += "dot1x max-reauth-req {}\n".format(dict1['max_reauth_req'])

    if  'txp' in dict1:
        cmd += "dot1x timeout tx-period {}\n".format(dict1['txp'])

    if dict1['authmod'] != 'multi-auth':
        cmd += "access-session host-mode {}\n".format(dict1['authmod'])

    if dict1['open'] == False:
        cmd += "access-session closed\n"

    if 'ctr' in dict1:
        cmd += "access-session control-direction {}\n".format(dict1['ctr'])

    if  'reauth' in dict1:
        cmd += "authentication timer reauthenticate {}\n".format(dict1['reauth'])

    cmd += "service-policy type control subscriber {}\n".format(policy_map)

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 802.1x port based Authentication on {}"
            "Error: {}".format(converted_interface, str(e))
        )


def unconfigure_dot1x_cred_profile(device, profile_name):
    """Unconfigure dot1x credentials profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = 'no dot1x credentials {}\n'.format(profile_name)
    log.info("unconfigure dot1x credential")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile {}.Error: {}".format(profile_name, str(e))
        )


def unconfigure_eap_profile_md5(device, profile_name):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = 'no eap profile {}\n'.format(profile_name)
    log.info("unconfigure eap md5 profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure eap md5 profile {}.Error: {}".format(profile_name, str(e))
        )

def unconfigure_access_session_monitor(device):
    """ Enable access-session  monitor
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable access-session monitor
    """
    cmd = 'no access-session monitor\n'
    log.info("Unconfigure access-session monitor")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to disable access-session monitor.Error: {}".format(str(e))
        )


def unconfigure_access_session_sticky(device, timer):
    """ configure interface-template sticky timer
        Args:
            device ('obj'): device to use
            timer (int): <1-65535>  Enter a value between 1 and 65535
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure interface-template sticky timer
    """
    cmd = 'no access-session interface-template sticky timer {}\n'.format(timer)
    log.info("Unconfigure interface-template sticky timer")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure access-session sticky timer on {}.Error: {}".format(timer, str(e))
        )


def disable_dot1x_sysauthcontrol(device):
    """ Globally disables 802.1X port-based authentication.
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable 802.1X port-based authentication.
    """
    log.info("Disables 802.1X port-based authentication")
    cmd = "no dot1x system-auth-control\n"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to Disablele dot1x system auth-control.Error: {}".format(str(e))
        )


def unconfigure_dot1x_supplicant(device, profile_name, intf, eap_profile=None):

    """ UnConfigure on dot1x supplicant switch 
    Args:
        device (`obj`): Device object
        profile_name (`str`): dot1x Credential profile_name
        intf (`str`) : Supplicant Interface
        eap_profile (`str`, optional): eap profile name (Default is None)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append("no dot1x credentials {}".format(profile_name))
    config_list.append("interface {}".format(intf))
    config_list.append("no dot1x pae supplicant")

    if eap_profile is not None:
        config_list.append("no dot1x supplicant eap profile {}".format(eap_profile))

    try:
        device.configure(config_list)
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure dot1x supplicant username {profile_name}\
            on pagent interface {intf}'.format(profile_name=profile_name,intf=intf)
        )
        
def unconfigure_dot1x_system_auth_control(device):

    """UnConfigure dot1x system-auth-control
    Args: 
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring     
    """
    try:
        device.configure([
            "no dot1x system-auth-control"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure dot1x system-auth-control'
        )

def configure_authentication_host_mode(device, mode, intf, style='legacy'):

    """Configure legacy cli authentication host-mode multi-auth/multi-domain/multi-host/single-host
    Args:
        device (`obj`): Device object
        mode (`str`): Host mode
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd} host-mode {mode}".format(cmd=cmd,mode=mode)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure host-mode'
    )
        
def unconfigure_authentication_host_mode(device,mode,intf,style='legacy'):

    """UnConfigure legacy cli authentication host-mode multi-auth/multi-domain/multi-host/single-host
    Args:
        device (`obj`): Device object
        mode (`str`): Host mode
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"

    try:    
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd} host-mode {mode}".format(cmd=cmd,mode=mode)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure host-mode'
        )        

def configure_authentication_order(device,order,intf):

    """Configure legacy cli authentication order dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        order (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication order {order}".format(order=order)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication order'
        )        

def unconfigure_authentication_order(device,order,intf):

    """UnConfigure legacy cli authentication order dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        order (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication order {order}".format(order=order)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication order'
    )

def configure_authentication_priority(device,priority,intf):

    """Configure legacy cli authentication priority dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        priority (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication priority {priority}".format(priority=priority)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication priority'
        )

def unconfigure_authentication_priority(device,priority,intf):

    """Unconfigure legacy cli authentication priority dot1x/mab/webauth
    Args:
        device (`obj`): Device object
        priority (`str`): mab dot1x/dot1x/mab/dot1x mab
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication priority {priority}".format(priority=priority)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication priority'
        )        

def configure_authentication_port_control(device,control,intf,style='legacy'):

    """Configure legacy cli 
    authentication port-control auto/force-authorized/force-unauthorized
    Args:
        device (`obj`): Device object
        control (`str`): auto/force-authorized/force-unauthorized
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (Default is legacy)
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """

    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd} port-control {control}".format(cmd=cmd,control=control)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication port-control'
        )
        
def unconfigure_authentication_port_control(device,control,intf,style='legacy'):

    """UnConfigure legacy cli 
    authentication port-control auto/force-authorized/force-unauthorized
    Args:
        device (`obj`): Device object
        control (`str`): auto/force-authorized/force-unauthorized
        intf (`str`): Interface to configure
        style (`str`, optional): legacy or new (default is legacy)
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    cmd = ""
    if style == "new":
        cmd = "access-session"
    else:
        cmd = "authentication"
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd} port-control {control}".format(cmd=cmd,control=control)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication port-control'
        )

def configure_authentication_periodic(device,intf):

    """Configure legacy cli 
        authentication periodic
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication periodic"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to configure authentication periodic'
)        

def unconfigure_authentication_periodic(device,intf):

    """UnConfigure legacy cli 
    authentication periodic
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication periodic"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication periodic'
)        

def configure_authentication_timer_reauth(device,value,intf):

    """Configure legacy cli 
    authentication timer reauthenticate value/server
    Args:
        device (`obj`): Device object
        value (`str`): authentication timer reauthenticate value/server
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "authentication timer reauthenticate {value}".format(value=value)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication timer reauthenticate'
        )
        
def unconfigure_authentication_timer_reauth(device,intf):

    """UnConfigure legacy cli 
    authentication timer reauthenticate value/server
    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no authentication timer reauthenticate"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Unable to unconfigure authentication timer reauthenticate'
    )

def configure_auth_method(device,value,intf):

    """Configure cli 
    authentication method mab/dot1x pae authenticator
    Args:
        device (`obj`): Device object
        value (`str`): mab/dot1x
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    cmd = ""
    if value == "dot1x":
        cmd = "dot1x pae authenticator"
    elif value == "mab":
        cmd = "mab"
    else:
        cmd = value

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "{cmd}".format(cmd=cmd)
        ])
    except SubCommandFailure:
        log.error('Failed configuring authentication method')

def unconfigure_auth_method(device,value,intf):

    """unconfigure legacy cli 
    authentication method mab/dot1x pae authenticator
    Args:
        device (`obj`): Device object
        value (`str`): mab/dot1x
        intf (`str`): Interface to configure
    Return:   
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """
    cmd = ""
    if value == "dot1x":
        cmd = "dot1x pae authenticator"
    elif value == "mab":
        cmd = "mab"
    else:
        cmd = value

    try:
        device.configure([
            "interface {intf}".format(intf=intf),
            "no {cmd}".format(cmd=cmd)
        ])
    except SubCommandFailure:
        log.error('Failed unconfiguring authentication method')


