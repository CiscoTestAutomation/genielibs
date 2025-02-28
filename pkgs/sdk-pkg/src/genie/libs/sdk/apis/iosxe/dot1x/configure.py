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

def configure_dot1x_cred_profile(device, profile_name, user_name, passwd, passwd_type=None):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
            username (`str`): username for dot1x user
            passwd (`str`): password in plain text
            passwd_type('str',optional): password type (HIDDEN/UNENCRYPTED),defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = ''
    cmd += 'dot1x credentials {}\n'.format(profile_name)
    cmd += 'username {}\n'.format(user_name)
    if passwd_type == 'HIDDEN':
        cmd += 'password 7 {}\n'.format(passwd)
    elif passwd_type == 'UNENCRYPTED':
        cmd += 'password 0 {}\n'.format(passwd)
    else:
        cmd += 'password {}\n'.format(passwd)
    #cmd += 'password {}\n'.format(passwd)
    log.info("configure dot1x credential")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile {}.Error: {}".format(profile_name, str(e))
        )

def configure_eap_profile(device, profile_name,method='md5',ciphersuite=None):
    """Configure EAP Md5 profile
        Args:
            device ('obj'): device to use
            profile_name (`str`): eap profile name
            method ('str',optional). Method to use for eap authentication. Default is md5
            ciphersuite ('str', optional): Ciphersuite to use for eap profile
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure eap md5 profile
    """
    cmd = ''
    cmd += 'eap profile {}\n'.format(profile_name)
    cmd += 'method {}\n'.format(method)
    if ciphersuite:
        cmd += 'ciphersuite {}\n'.format(ciphersuite)
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

def clear_access_session(device, interface=None):
    """ executes clear access-sesssion CLI
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to execute clear access-sesssion.
    """
    cmd = "clear access-session"

    if interface:
        converted_interface = Common.convert_intf_name(interface)
        cmd += " interface {intf}".format(intf=converted_interface)
        
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute clear access-sesssion.Error: {}".format(str(e))
        )

def config_identity_ibns(device, policy_map=None, interface=None, access=True, port_control='auto', template_name=None, dot1x_pae=None, **kwargs):
    """ Configure 802.1x port based authentication for
        IBNS2.0 with service policy under interface/template
    Mandatory args:
            device ('obj'): device to use
            access ('bol'): Set to True, False to configure in Trunk mode
    Optional args:
        policy_map('str'): Name of policy map to be attached.
        interface (`str`,optional): Interface name
        data_vlan(`int`): vlan_id for data traffic
        voice_vlan(`int`): vlan_id for voice traffic
        max_req:(`int`) Max No. of Retries
        max_reauth_req(`int`): Max No. of Reauthentication Attempts
        authmod('str'): default(multi-auth), mult-host peer, multi-domain etc
        open('bol'): {False: closed | True: open (default) }
        reauth('str'):  server or numberic range is 1 to 65535 seconds
        ctr('str'): {both | in}
        txp(`int`):The range is 1 to 65535 seconds
        port_control ('str'): {auto|force-authorized|force-unauthorized}. Default = 'auto'
        template_name ('str'): Template name to be configured
        txp_sup ('int'): The range is 1 to 65535 seconds
        dot1x_pae ('Str'): auth mothod 
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

    cmd = ""
    if interface is not None:
        converted_interface = Common.convert_intf_name(interface)
        cmd += 'interface {}\n'.format(converted_interface)
    else:
        cmd += f'template {template_name}\n'

    if access:
        if template_name is None:
            cmd += "switchport\n"
            cmd += "switchport mode access\n"
        else:
            cmd += "switchport mode access\n"
    else:
        if template_name is None:
            cmd += "switchport\n"
            cmd += "switchport mode trunk\n"
        else:
            cmd += "switchport mode trunk\n"

    cmd += "access-session port-control {port_control}\n".format(port_control=port_control)
    cmd += "authentication periodic\n"
    cmd += "mab\n"
    if dot1x_pae is not None:
        cmd += "dot1x pae {}\n".format(dot1x_pae)
    else:
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

    if 'txp_sup' in dict1 :
        cmd += f"dot1x timeout supp-timeout {dict1['txp_sup']}\n"

    if dict1['authmod'] != 'multi-auth':
        cmd += "access-session host-mode {}\n".format(dict1['authmod'])
    
    if dict1['open'] != True:
        cmd += "access-session closed\n"

    if 'ctr' in dict1:
        cmd += "access-session control-direction {}\n".format(dict1['ctr'])

    if 'reauth' in dict1:
        cmd += "authentication timer reauthenticate {}\n".format(dict1['reauth'])

    if policy_map:
        cmd += "service-policy type control subscriber {}\n".format(policy_map)

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 802.1x port based Authentication"
            "Error: {}".format(str(e))
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

def configure_dot1x_cred_pki(device, profile_name, user_name, pki_trustpoint):
    """Configure EAP Md5 profile with PKI
        Args:
            device ('obj'): device to use
            profile_name (`str`): dot1x credential profile name
            username (`str`): username for dot1x user
            pki_trustpoint (`str`): PKI trustpoint name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure dot1x credential
    """
    cmd = ''
    cmd += f'dot1x credentials {profile_name}\n'
    cmd += f'username {user_name}\n'
    cmd += f'pki-trustpoint {pki_trustpoint}\n'

    log.info("Configure dot1x credential with PKI")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure dot1x credential profile with PKI{}.Error: {}".format(profile_name, str(e))
        )

def configure_dot1x_pae(device, intf, mode='both'):

    """Configure
    dot1x pae {mode}

    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
        mode ('str', optional): Mode to configure, defaults to 'both'

    Return:
        None

    Raise:
        SubCommandFailure: Failed configuring dot1x pae on interface
    """

    try:
        device.configure([
            f"interface {intf}",
            f"dot1x pae {mode}"
        ])

    except SubCommandFailure:
        log.error('Failed configuring dot1x pae command on interface')


def unconfigure_dot1x_pae(device, intf, mode='both'):

    """Unconfigure
    no dot1x pae {mode}

    Args:
        device (`obj`): Device object
        intf (`str`): Interface to configure
        mode ('str', optional): Mode to unconfigure, defaults to 'both'

    Return:
        None

    Raise:
        SubCommandFailure: Failed unconfiguring dot1x pae on interface
    """

    try:
        device.configure([
            f"interface {intf}",
            f"no dot1x pae {mode}"
        ])

    except SubCommandFailure:
        log.error('Failed configuring dot1x pae command on interface')


def configure_service_template_linksec(device, template, session_type):
    """Configure Service template with link security
        Args:
            device ('obj'): device to use
            template (`str`): template name
            session_type (`str`): session type to be configured

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service template with link security
    """

    cmd = [
        f'service-template {template}',
        f'linksec policy {session_type}',
    ]

    log.debug("Configure Service template with link security")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service template with link security")


def unconfigure_service_template(device, template):
    """Unconfigure Service template
        Args:
            device ('obj'): device to use
            template (`str`): template name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Service template
    """
    cmd = f'no service-template {template}'

    log.debug("Unconfigure Service template")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Service template")


def configure_service_template_voice(device, template):
    """Configure Service template with voice
        Args:
            device ('obj'): device to use
            template (`str`): template name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service template with voice
    """

    cmd = [
        f'service-template {template}',
        'voice vlan'
          ]

    log.debug("Configure Service template with voice")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service template with voice")


def configure_class_map_subscriber(device,
                                   map_name,
                                   match_type,
                                   result_type=None,
                                   auth_status=None,
                                   method_type=None,
                                   dot1x_type=None,
                                   priority_type=None,
                                   priority=None):
    """Configure Class Map Subscriber
        Args:
            device ('obj'): device to use
            map_name ('str'): map name
            match_type ('str'): Match type
            result_type ('str', optional): Result type, defaults to None
            auth_status ('str', optional): Authorization status, defaults to None
            method_type ('str', optional): Method type, defaults to None
            dot1x_type ('str', optional): Dot1x type, defaults to None
            priority_type('str', optional): Priority type, defaults to None
            priority ('str', optional): Priorit value, defaults to None

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Class map Subscriber
    """
    log.debug("Configure Class map Subscriber")

    cmd = [f'class-map type control subscriber match-all {map_name}']
    if result_type and method_type and dot1x_type:
       cmd.append (f'match {match_type} {result_type} {method_type} {dot1x_type}')
    elif result_type:
       cmd.append (f'match {match_type} {result_type}')
    elif auth_status:
       cmd.append (f'match {match_type} {auth_status}')
    elif method_type:
       cmd.append (f'match {match_type} {method_type}')
    elif priority_type:
       cmd.append (f'match {match_type} {priority_type} {priority}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
         "Could not configure Class map Subscriber")
    return

def unconfigure_class_map_subscriber(device, map_name):
    """Unconfigure Class Map Subscriber
        Args:
            device ('obj'): device to use
            map_name (`str`): map name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Class Map Subscriber
    """
    cmd = f'no class-map type control subscriber match-all {map_name}'

    log.debug("Unconfigure Class Map Subscriber")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure Class Map Subscriber")


def configure_dot1x_cred_int(device, interface, cred_profile_name=None, eap_profile=None, auth_profile=None):
    """Configure Dot1x credential on interface
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str', optional): dot1x credential profile name
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_profile (`str`, optional): Auth profile name(Default is None)

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to configure Dot1x credential on interface
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = []
    cmd.append(f'interface {converted_interface}')

    if cred_profile_name:
        cmd.append(f'dot1x credentials {cred_profile_name}')

    if eap_profile is not None:
        cmd.append(f'dot1x supplicant eap profile {eap_profile}')

    if auth_profile is not None:
       cmd.append(f'dot1x authenticator eap profile {auth_profile}')


    log.debug("Configure dot1x credential on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure credential on interface on {}.Error: {}".format(converted_interface, str(e))
        )


def unconfigure_dot1x_cred_int(device, interface, cred_profile_name=None, eap_profile=None, auth_profile=None):
    """Unconfigure Dot1x credential on interface
    Args:
        device ('obj'): device to use
        interface (`str`): Interface name
        cred_profile_name (`str', optional): dot1x credential profile name (Default is None)
        eap_profile (`str`, optional): eap profile name (Default is None)
        auth_profile (`str`, optional): Auth profile name (Default is None)

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to unconfigure Dot1x credential on interface
    """
    converted_interface = Common.convert_intf_name(interface)
    cmd = []
    cmd.append(f'interface {converted_interface}')

    if cred_profile_name:
        cmd.append(f'no dot1x credentials {cred_profile_name}')

    if eap_profile is not None:
        cmd.append(f'no dot1x supplicant eap profile {eap_profile}')

    if auth_profile is not None:
       cmd.append(f'no dot1x authenticator eap profile {auth_profile}')


    log.debug("Unconfigure dot1x credential on interface")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure credential on interface on {}.Error: {}".format(converted_interface, str(e))
        )

def configure_radius_server_accounting_system(device,minutes,seconds,privilege_level,auth_list):
    """ configure radius-server accounting system host-config
    Args:
        device ('obj'): Device object
        minutes ('int): Specify timeout in minutes
        seconds ('int'): Specify timeout in seconds
        privilege_level ('int'): Specify privilege level for line
        auth_list ('str') : Specify authentication list
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring radius-server accounting system host-config
    """
    log.info(f"Configuring radius-server accounting system host-config")

    configs=[
        "radius-server accounting system host-config",
        "line console 0",
        f"exec-timeout {minutes} {seconds}",
        f"privilege level {privilege_level}",
        f"login authentication {auth_list}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure radius-server accounting system host-config. Error:\n{e}")

def configure_service_template_with_inactivity_timer(device,template_name,timer):
    """ configure service template with inactivity timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): inactivity timer value
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with inactivity timer
    """
    log.info(f"Configuring service template with inactivity timer")

    configs=[
	    f"service-template {template_name}",
	    f"inactivity-timer {timer}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with inactivity timer. Error:\n{e}")

def configure_service_template_with_vlan(device,template_name,vlan_id):
    """ configure service template with vlan
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        vlan_id ('int'): Vlan ID to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with vlan
    """
    log.info(f"Configuring service template with vlan")

    configs=[
	    f"service-template {template_name}",
	    f"vlan {vlan_id}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with vlan. Error:\n{e}")

def configure_service_template_with_access_group(device,template_name,access_grp):
    """ configure service template with access group
    Args:
        device ('obj'): Device object
        template_name ('str): Specify a template name
        access_grp ('str'): Access-Group
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring service template with access group
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"service-template {template_name}",
	    f"access-group {access_grp}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with access group. Error:\n{e}")

def configure_class_map_type_match_any(device,class_map_name,service_temp_name):
    """ configure class-map type control subscriber match-any
    Args:
        device ('obj'): Device object
        class_map_name ('str): Specify a class map name
        service_temp_name ('str'): Specify service template name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring class-map type control subscriber match-any
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"class-map type control subscriber match-any {class_map_name}",
	    f"match activated-service-template {service_temp_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure class-map type control subscriber match-any. Error:\n{e}")

def configure_class_map_type_match_none(device,class_map_name,service_temp_name):
    """ configure class-map type control subscriber match-none
    Args:
        device ('obj'): Device object
        class_map_name ('str): Specify a class map name
        service_temp_name ('str'): Specify service template name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring class-map type control subscriber match-none
    """
    log.info(f"Configuring service template with access group")

    configs=[
	    f"class-map type control subscriber match-none {class_map_name}",
	    f"match activated-service-template {service_temp_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure class-map type control subscriber match-none. Error:\n{e}")

def configure_template_methods_for_dot1x(device,template_name,vlan_id,voice_vlan_id,policy_map_name):
    """ configure template methods for dot1x
    Args:
        device ('obj'): Device object
        template_name ('str): Specify template name
        vlan_id ('str'): Specify VLAN ID of the VLAN when this port is in access mode
        voice_vlan_id ('str'): Specify Vlan for voice traffic
        policy_map_name ('str'): Policy-map name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring template methods for dot1x
    """
    log.info(f"Configuring template methods for dot1x")

    configs=[
        f"template {template_name}",
        "dot1x pae authenticator",
        f"switchport access vlan {vlan_id}",
        "switchport mode access",
        f"switchport voice vlan {voice_vlan_id}",
        "mab",
        "access-session closed",
        "access-session port-control auto",
        "authentication periodic",
        "authentication timer reauthenticate server",
	    f"service-policy type control subscriber {policy_map_name}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure template methods for dot1x. Error:\n{e}")

def configure_template_methods_using_max_reauth(device,template_name,timeout_period,max_reauth):
    """ configure template methods using max reauth and timeout
    Args:
        device ('obj'): Device object
        template_name ('str): Specify template name
        timeout_period ('int'): Specify VLAN ID of the VLAN when this port is in access mode
        max_reauth ('int'): Specify max-reauth-req value <1-10>
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring template methods using max reauth and timeout
    """
    log.info(f"Configuring template methods for dot1x")

    configs=[
        f"template {template_name}",
        f"dot1x timeout tx-period {timeout_period}",
        f"dot1x max-reauth-req {max_reauth}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure template methods using max reauth and timeout. Error:\n{e}")

def clear_access_session_mac(device, mac):
    """Clear Access Session MAC
    Args:
        device ('obj'): device to use
        mac (`str`): MAC to be cleared

    Returns:
        None

    Raises:
        SubCommandFailure: Failed to clear access session mac
    """
    log.debug("Clearing Access session MAC")
    try:
        device.execute(f'clear access-session mac {mac}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to clear Access session MAC.Error: {}".format(str(e))
        )

def unconfigure_source_template(device, interface, template_name):
    """Unconfigure Source template config
        Args:
            device ('obj'): device to use
            interface (`str`): Interface name
            template (`str`): Built-in/User defined template Name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove the source template
    """

    converted_interface = Common.convert_intf_name(interface)
    cmd = [
                f"interface {interface}",
                f"no source template {template_name}"
          ]
    log.info("Unconfigure source template {tmp} on {intf}".format(tmp=template_name, intf=converted_interface))

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure the source template {}.Error: {}".format(template_name, str(e))
        )


def configure_service_policy(device, policy_name):
    """Configure Service policy
        Args:
            device ('obj'): device to use
            policy_name (`str`): Policy_name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Service policy
    """

    cmd = [f'service-policy type control subscriber {policy_name}']

    log.debug("Configure Service policy")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Service policy")


def unconfigure_service_policy(device):
    """Unconfigure Service policy
        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Service policy
    """

    cmd = ['no service-policy type control subscriber']

    log.debug("Unconfigure Service policy")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Service policy")


def configure_access_session_limit(device, session_limit, event_limit):
    """Configure Access session and event limit
        Args:
            device ('obj'): device to use
            session_limit (`int`): Session Limit or max sessions to be logged
            event_limit ('int'): Event Limit per session

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure Access session and event limit
    """

    cmd = [f'access-session event-logging enable session-limit {session_limit} event-limit {event_limit}']

    log.debug("Configure Access session and event limit")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Access session and event limit")


def unconfigure_access_session_limit(device):
    """Unconfigure Access session and event limit
        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure Access session and event limit
    """

    cmd = ['no access-session event-logging enable session-limit']

    log.debug("Unconfigure Access session and event limit")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Access session and event limit")


def unconfigure_dot1x_template(device, template_name):
    """template unconfig
        Args:
            device ('obj'): device to use
            template (`str`): Built-in/User defined template Name

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to unconfigure template
    """
    cmd = ''
    cmd += f'no template {template_name}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure template {}.Error: {}".format(template_name, str(e))
        )


def configure_parameter_map_subscriber(device, parameter_map_name, map_num,
    filter_type, parameter_type, parameter_name, action_num, template_type,
    template_name):
    """Configure parameter map subscriber
        Args:
            device ('obj'): device to use
            parameter_map_name (`str`): Parameter Map name to be configured
            map_num ('int'): Map number to be configured
            filter_type ('str'): Filter type to be configured
            parameter_type ('str'): parameter type to be configured
            parameter_name ('str'): Parameter name to be configured
            action_num ('int'): Action number to be configure
            template_type ('str'): Template type to be configured
            template_name ('str'): Template name to be configured

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to configure parameter map subscriber
    """
    cmd = ''
    cmd += f'parameter-map type subscriber attribute-to-service {parameter_map_name}\n'
    cmd = [  f'parameter-map type subscriber attribute-to-service {parameter_map_name}\n',
                   f'{map_num} map {parameter_type} {filter_type} {parameter_name}\n',
                   f'{action_num} {template_type} {template_name}' ]


    log.debug("Configure parameter map subscriber")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure parameter map subscriber")


def configure_service_template_with_absolute_timer(device, template_name, timer):
    """ configure service template with absolute timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): timer
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with absolute timer")

    configs=[
	    f"service-template {template_name}",
	    f"absolute-timer {timer}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with absolute timer. Error:\n{e}")

def configure_service_template_with_description(device, template_name, desc_line):
    """ configure service template with description
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        desc_line ('str'): description line
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with description")

    configs=[
	    f"service-template {template_name}",
	    f"description {desc_line}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with description. Error:\n{e}")

def configure_service_template_with_inactivity_timer(device, template_name, timer, probe=None):
    """ configure service template with inactivity timer
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        timer ('int'): timer
        probe('str',optional): probe
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with inactivity timer")

    cmd = []
    cmd.append(f"service-template {template_name}")
    if probe:
        cmd.append(f"inactivity-timer {timer} probe")
    else:
        cmd.append(f"inactivity-timer {timer}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with inactivity timer. Error:\n{e}")

def configure_service_template_with_redirect_url(device, template_name, url_link, acl_name="", redirect_option=""):
    """ configure service template with redirect url
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        url_link ('str'): url link
        acl_name('str'): acl name
        redirect_option('str'): redirect option
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with redirect url")

    cmd = []
    cmd.append(f"service-template {template_name}")
    if acl_name:
        if redirect_option:
            cmd.append(f"redirect url {url_link} match {acl_name} {redirect_option}")
        else:
            cmd.append(f"redirect url {url_link} match {acl_name}")
    else:
        cmd.append(f"redirect url {url_link}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with redirect url. Error:\n{e}")

def configure_service_template_with_sgt(device, template_name, sgt_range):
    """ configure service template with sgt
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        sgt_range ('int'): sgt range
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with sgt")

    configs=[
	    f"service-template {template_name}",
	    f"sgt {sgt_range}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with sgt. Error:\n{e}")

def configure_service_template_with_tag(device, template_name, tag):
    """ configure service template with sgt range
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        tag ('str'): tag name
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with tag")

    configs=[
	    f"service-template {template_name}",
	    f"tag {tag}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with tag. Error:\n{e}")

def unconfigure_autoconf(device):
    """ Unconfigure autoconf enable

    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = 'no autoconf enable'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to  Unconfigure autoconf enable on this device. Error:\n{e}")

def configure_service_template_with_command_line(device, template_name, command):
    """ configure service template with command
    Args:
        device ('obj'): Device object
        template_name ('str'): Specify a template name
        command ('str'): command to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Configuring service template with command")

    configs=[
	    f"service-template {template_name}",
	    f"{command}"
	]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure service template with command. Error:\n{e}")

def configure_authentication_control_direction(device, interface, direction):

    """Configure authentication control-direction
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        direction ('str'): Control traffic direction (both/in)
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        f'authentication control-direction {direction}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authentication control-direction. Error:\n{e}")

def unconfigure_authentication_control_direction(device, interface, direction):

    """Unconfigure authentication control-direction
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        direction ('str'): Control traffic direction (both/in)
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        f'no authentication control-direction {direction}'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authentication control-direction. Error:\n{e}")

def configure_authentication_open(device, interface):

    """Configure authentication open
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        'authentication open'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure authentication open. Error:\n{e}")

def unconfigure_authentication_open(device, interface):

    """Unconfigure authentication open
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
    Return:
        None
    Raise:
        SubCommandFailure
    """

    cmd = [
        f'interface {interface}',
        'no authentication open'
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure authentication open. Error:\n{e}")

def configure_authentication_event_server(device, interface, action, action_type, vlan_id=None):
    """Configure authentication event server
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        action ('str'): alive  Configure AAA server alive actions
                        dead   Configure AAA server dead actions 
        action_type ('str', optional): authorize     Authorize the port
                                       reinitialize  Reinitialize all client on the port
        vlan_id ('int'): <1-4094>  Enter a VlanId                        
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if action_type=="reinitialize": 
        cmd.append("authentication event server {action} action {action_type} vlan {vlan_id}".format(action=action, action_type=action_type, vlan_id=vlan_id))
    if action_type=="authorize" and action!="alive":
        cmd.append("authentication event server {action} action {action_type} voice".format(action=action, action_type=action_type))
    else:
         raise Exception("Unable to process the request.Please provide correct options")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure authentication {action}. Error:\n{error}"
            .format(action=action, error=e)
        )  

def unconfigure_authentication_event_server(device, interface, action, action_type, vlan_id=None):
    """Unconfigure authentication event server
    Args:
        device ('obj'): Device object
        interface ('str'): Interface to configure
        action ('str'): alive  Configure AAA server alive actions
                        dead   Configure AAA server dead actions 
        action_type ('str', optional): authorize     Authorize the port
                                       reinitialize  Reinitialize all client on the port
        vlan_id ('int'): <1-4094>  Enter a VlanId                        
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f"interface {interface}"]
    if action_type=="reinitialize": 
        cmd.append("no authentication event server {action} action {action_type} vlan {vlan_id}".format(action=action, action_type=action_type, vlan_id=vlan_id))
    if action_type=="authorize" and action!="alive":
        cmd.append("no authentication event server {action} action {action_type} voice".format(action=action, action_type=action_type))
    else:
        raise Exception("Unable to process the request.Please provide correct options")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure authentication {action}. Error:\n{error}"
            .format(action=action, error=e)
        )  

def configure_enable_cisp(device):
    """ Configure cisp on device
     Args:
            device ('obj'): Device object
     Returns:
            None
     Raises:
            SubCommandFailure
    """
    cmd = [f"cisp enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not configure cisp on device Error: {error}".format(error=e))

def unconfigure_enable_cisp(device):
    """ Unconfigure cisp on device
     Args:
            device ('obj'): Device object
     Returns:
            None
     Raises:
            SubCommandFailure
    """
    cmd = [f"no cisp enable"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not unconfigure cisp on device Error: {error}".format(error=e))

def configure_access_session_acl_default_passthrough(device):
    """ Configure access-session acl deafult passthrough
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure access-session acl default passthrough on device
    """

    cmd = ["access-session acl default passthrough"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-session acl default passthrough on device. Error:\n{e}"
        )

def unconfigure_access_session_acl_default_passthrough(device):
    """ Unconfigures access-session acl default passthrough
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to unconfigure access-session acl default passthrough on device
    """

    cmd = ["no access-session acl default passthrough"]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure access-session acl default passthrough on device. Error:\n{e}"
        )

def configure_access_session_macmove_deny(device):
    """Configure access-session mac-move deny
    Args:
        device ('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f'access-session mac-move deny']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure access-session. Error:\n{e}")

def unconfigure_access_session_macmove_deny(device):
    """unconfigure access-session mac-move deny
    Args:
        device ('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f'no access-session mac-move deny']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure access-session. Error:\n{e}")

def configure_access_session_macmove_deny_uncontrolled(device):
    """Configure access-session mac-move deny-uncontrolled
    Args:
        device ('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Do you wish to continue\? \[yes\]:",
                action='sendline(yes)',
                loop_continue=False,
                continue_timer=False
            )
        ]
    )
    cmd = [f'access-session mac-move deny-uncontrolled']
    try:
        device.configure(cmd, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure access-session. Error:\n{e}")

def unconfigure_access_session_macmove_deny_uncontrolled(device):
    """unconfigure access-session mac-move deny-uncontrolled
    Args:
        device ('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f'no access-session mac-move deny-uncontrolled']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure access-session. Error:\n{e}")

def configure_default_spanning_tree(device, mode_type):
    """Configure default spanning-tree
    Args:
        device ('obj'): Device object
        mode_type('str'):  backbonefast  Enable BackboneFast Feature
                           bridge        STP Bridge Assurance parameters
                           cca           enable/disable CCA routine
                           dispute       Enable STP dispute mechanism
                           etherchannel  Spanning tree etherchannel specific configuration
                           extend        Spanning Tree 802.1t extensions
                           logging       Enable Spanning tree logging
                           loopguard     Spanning tree loopguard options
                           mode          Spanning tree operating mode
                           mst           Multiple spanning tree configuration
                           pathcost      Spanning tree pathcost options
                           portfast      Spanning tree portfast options
                           sso           Stateful Switchover
                           transmit      STP transmit parameters
                           uplinkfast    Enable UplinkFast Feature
                           vlan          VLAN Switch Spanning Tree
    Return:
        None
    Raise:
        SubCommandFailure 
    """
    cmd = f"default spanning-tree {mode_type}"
    if mode_type == "backbonefast":
        cmd+= f" {mode_type}"
    elif mode_type == "bridge":
        cmd+= f" {mode_type} assurance"
    elif mode_type == "dispute":
        cmd+= f" {mode_type}"
    elif mode_type == "etherchannel":
        cmd+= f" {mode_type} guard"
    elif mode_type == "logging":
        cmd+= f" {mode_type}"
    elif mode_type == "loopguard":
        cmd+= f" {mode_type} default"
    elif mode_type == "mode":
        cmd+= f" {mode_type}"
    elif mode_type == "pathcost":
        cmd+= f" {mode_type} method"
    elif mode_type == "portfast":
        cmd+= f" {mode_type} default"
    elif mode_type == "sso":
        cmd+= f" {mode_type} block-tcn"
    elif mode_type == "transmit":
        cmd+= f" {mode_type} hold-count"
    elif mode_type == "uplinkfast":
        cmd+= f" {mode_type} max-update-rate"
    else:
        cmd+= f" {mode_type} 10"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure default spanning-tree. Error:\n{e}")

def configure_access_session_mac_move(device, access_type, deny_type):
    """Configure access-session mac-move
    Args:
        device ('obj'): Device object
        access_type('str'): accounting             Accounting Filter List Configuration
                            acl                    Application of ACLs on access-session
                            attributes             Attributes Filter List Configuration
                            authentication         Authentication Filter List Configuration
                            bridge-mode            bridge-mode
                            cache                  Set cache configuration
                            event-logging          Event log Configuration
                            interface-template     Set the interface-template sticky globally
                            limit                  Set session limit parameter
                            mac-move               Set required action when a MAC move is detected
                            monitor                Apply template to monitor access sessions on the port
                            passthru-access-group  IP access-list map to FQDN ACL
                            single-policy          Replace all interface service-policies with single policy
                            tls-version            Set required TLS version
                            voice                  voice client auth options
                            wireless               Wireless
        deny_type('str'):   deny               DENY MAC moves (clears existing session)
                            deny-uncontrolled  Deny MAC move to uncontrolled port
    Return:   
        None
    Raise:
        SubCommandFailure  
    """
    cmd = f"access-session {access_type} {deny_type}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure access-session {access_type}. Error:\n{e}")
            
def unconfigure_access_session_mac_move(device, access_type, deny_type):
    """Unconfigure access-session mac-move
    Args:
        device ('obj'): Device object
        access_type('str'): accounting             Accounting Filter List Configuration
                            acl                    Application of ACLs on access-session
                            attributes             Attributes Filter List Configuration
                            authentication         Authentication Filter List Configuration
                            bridge-mode            bridge-mode
                            cache                  Set cache configuration
                            event-logging          Event log Configuration
                            interface-template     Set the interface-template sticky globally
                            limit                  Set session limit parameter
                            mac-move               Set required action when a MAC move is detected
                            monitor                Apply template to monitor access sessions on the port
                            passthru-access-group  IP access-list map to FQDN ACL
                            single-policy          Replace all interface service-policies with single policy
                            tls-version            Set required TLS version
                            voice                  voice client auth options
                            wireless               Wireless
        deny_type('str'):   deny               DENY MAC moves (clears existing session)
                            deny-uncontrolled  Deny MAC move to uncontrolled port
    Return:   
        None
    Raise:
        SubCommandFailure  
    """
    cmd = f"no access-session {access_type} {deny_type}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure access-session mac-move. Error:\n{e}")

def configure_parameter_map(device,
        parameter_map_name=False,
        enable_global=False,
        banner_file_name=None,
        banner_text=None,
        banner_title=None,
        captive_bypass_portal=False,
        cisco_logo_disable=False,
        consent_email=False,
        custom_page=False,
        device_failure_file_name=None,
        login_device_name=None,
        login_expired_device_name=None,
        custom_page_success_name=None,
        logout_window_disabled=False,
        max_http_conns=None,
        redirect_command=None,
        sleeping_client_timeout=None,
        success_window_disable=False,
        timeout_seconds=None,
        type_name=None,
        http_port=None,
        intercept_https_enable=False,
        secure_webauth_disable=False,
        trustpoint_name=None,
        virtual_ipv4=None,
        virtual_ipv6=None,
        watch_add_ipv4=None,
        watch_add_ipv6=None,
        dynamic_expiry_timeout=None,
        enabled_watch_list=False,
        webauth_bypass_intercept_name=None,
        webauth_bypass_intercept=None,
        webauth_http_enable=False
        ):

    """ Configuring paramter-map webauth <>
        Args:
            device (`obj`): Device object
            parameter_map_name ('str'): parameter-map name (max 99 char)
            enable_global('bool'): To enable global mode
            banner_file_name('str'): Specify name of the banner-file
            banner_text('str'): c banner-text c, where 'c' is a delimiting character (maximum 200 characters)
            banner_title('str'): c banner-title-text c, where 'c' is a delimiting character (maximum 127 characters)
            captive_bypass_portal('bool'): Turn on captive bypass
            cisco_logo_disable('bool'): Disable Cisco logo on internal html pages
            consent_email('bool'): Turn-on Consent with Email
            custom_page('bool'): custom-page - login, expired, success or failure page
            device_failure_file_name('str') : Specify name of the HTML file
            login_device_name('str'): Specify file on local storage media,Specify name of the HTML file
            login_expired_device_name('str'): Expired authentication proxy,Specify name of the HTML file
            custom_page_success_name('str'):Successful authentication proxy
            logout_window_disabled('bool'): Webauth logout window disable
            max_http_conns('int'): Maximum number of HTTP connections per client
            redirect_command('str'): Specify the redirect command 
            sleeping_client_timeout('int'): Sleep Timeout in Minute (10-43200)
            success_window_disable('bool'): Disable Success Window
            timeout_seconds('int'):timeout for the webauth session in Seconds
            type_name('str'): type - web-auth, consent or both
            http_port('int'): Set Webauth http server port (81-65535)
            intercept_https_enable('bool'): Enable intercept of https traffic
            secure_webauth_disable('bool'): Disable HTTP secure server for Webauth
            trustpoint_name('str') : Specify the trustpoint name
            virtual_ipv4('str'): Virtual IPv4 Address
            virtual_ipv6('str'): Virtual IPv6 Address
            watch_add_ipv4('str'): Watch List of webauth clients, IPv4 Watch List Entry
            watch_add_ipv6('str'): Watch List of webauth clients, IPv6 Watch List Entry
            dynamic_expiry_timeout('int'):Webauth watch-list expiry timeout in seconds
            enabled_watch_list('bool'): Enable Watchlist
            webauth_bypass_intercept_name('str'): Specify the webauth bypass ACL name
            webauth_http_enable('bool') : Enable HTTP server for Webauth

        Returns:
            None 
        Raises: 
            SubCommandFailure
    """
    log.debug(f"Configuring parameter-map type webauth {parameter_map_name}")
    cmd = []
    if parameter_map_name:
        cmd.append("parameter-map type webauth {parameter_map_name}".format(parameter_map_name=parameter_map_name))
    if enable_global:
        cmd.append("parameter-map type webauth global")
        if http_port:
            cmd.append("http port {http_port}".format(http_port=http_port))
        if intercept_https_enable:
            cmd.append("intercept-https-enable")
        if secure_webauth_disable:
            cmd.append("secure-webauth-disable")
        if trustpoint_name:
            cmd.append("trustpoint {trustpoint_name}".format(trustpoint_name=trustpoint_name))
        if virtual_ipv4:
            cmd.append("virtual-ip ipv4 {virtual_ipv4}".format(virtual_ipv4=virtual_ipv4))
        if virtual_ipv6:
            cmd.append("virtual-ip ipv6 {virtual_ipv6}".format(virtual_ipv6=virtual_ipv6))
        if watch_add_ipv4:
            cmd.append("watch-list add-item ipv4 {watch_add_ipv4}".format(watch_add_ipv4=watch_add_ipv4))
        if watch_add_ipv6:
            cmd.append("watch-list add-item ipv6 {watch_add_ipv6}".format(watch_add_ipv6=watch_add_ipv6))
        if dynamic_expiry_timeout:
            cmd.append("watch-list dynamic-expiry-timeout {dynamic_expiry_timeout}".format(dynamic_expiry_timeout=dynamic_expiry_timeout))
        if enabled_watch_list:
            cmd.append("watch-list enabled")
        if webauth_bypass_intercept_name:
            cmd.append("webauth-bypass-intercept {webauth_bypass_intercept}".format(webauth_bypass_intercept=webauth_bypass_intercept))
        if webauth_http_enable:
            cmd.append("webauth-http-enable")
    if banner_file_name:
        cmd.append("banner file {banner_file_name}".format(banner_file_name=banner_file_name))
    if banner_text:
        cmd.append("banner text {banner_text}".format(banner_text=banner_text))
    if banner_title:
        cmd.append("banner title {banner_title}".format(banner_title=banner_title))
    if captive_bypass_portal:
        cmd.append("captive-bypass-portal")
    if cisco_logo_disable:
        cmd.append("cisco-logo-disable")
    if consent_email:
        cmd.append("consent email")
    if custom_page:
        if device_failure_file_name:
            cmd.append("custom-page failure device {device_failure_file_name}".format(device_failure_file_name=device_failure_file_name))
        if login_device_name:
            cmd.append("custom-page login device {login_device_name}".format(login_device_name=login_device_name))
        if login_expired_device_name:
            cmd.append("custom-page login expired device {login_expired_device_name}".format(login_expired_device_name=login_expired_device_name))
        if custom_page_success_name:
            cmd.append("custom-page failure device {custom_page_success_name}".format(custom_page_success_name=custom_page_success_name))
    if logout_window_disabled:
        cmd.append("logout-window-disabled")
    if max_http_conns:
        cmd.append("max-http-conns {max_http_conns}".format(max_http_conns=max_http_conns))
    if redirect_command:
        cmd.append("redirect {redirect_command}".format(redirect_command=redirect_command))
    if sleeping_client_timeout:
        cmd.append("sleeping-client timeout {sleeping_client_timeout}".format(sleeping_client_timeout=sleeping_client_timeout))
    if success_window_disable:
        cmd.append("success-window-disable")
    if timeout_seconds:
        cmd.append("timeout init-state sec {timeout_seconds}".format(timeout_seconds=timeout_seconds))
    if type_name:
        cmd.append("type {type_name}".format(type_name=type_name))

    try:
        device.configure(cmd)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure class-map on device. Error:\n{error}"
        )

def unconfigure_parameter_map(device, parameter_map_name):
    """ unconfigure paramter map
        Args:
            device ('obj'): device to use
            parameter_map_name ('str'): parameter-map name (max 99 char)
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure interface-template sticky timer
    """
    cmd = f'no parameter-map type webauth {parameter_map_name}'
    log.debug("Unconfigure Parameter map")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure parameter map {parameter_map_name}.Error:\n{e}"
        )

def unconfigure_parameter_map_subscriber(device, parameter_map_name):
    """UnConfigure parameter map subscriber
        Args:
            device ('obj'): device to use
            parameter_map_name (`str`): Parameter Map name to be unconfigured
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure parameter map subscriber
    """
    cmd = f'no parameter-map type subscriber attribute-to-service {parameter_map_name}'

    log.debug("UnConfigure parameter map subscriber")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure parameter map subscriber")
    
def configure_access_session_tls_version(device, version):
    """Configure access-session tls-version
        Args:
            device ('obj'): device to use
            version (`str`): TLS version to configure ('1.0', '1.2', '1.3', 'all')
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure access-session tls-version
    """
    if version not in ['1.0', '1.2', '1.3', 'all']:
        raise ValueError("Invalid TLS version. Accepted values are '1.0', '1.2', '1.3', 'all'.")

    cmd = 'access-session tls-version {}'.format(version)
    log.info("Configuring access-session tls-version to {}".format(version))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure access-session tls-version {}.Error: {}".format(version, str(e))
        )

def unconfigure_access_session_tls_version(device):
    """Unconfigure access-session tls-version
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure access-session tls-version
    """
    cmd = 'no access-session tls-version'
    log.info("Unconfiguring access-session tls-version")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure access-session tls-version. Error: {}".format(str(e))
        )