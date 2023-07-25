import re
import logging
import ipaddress
from unicon.eal.dialogs import Dialog
from genie.utils.timeout import Timeout
from unicon.core.errors import SubCommandFailure
from pyats.utils.secret_strings import to_plaintext

log = logging.getLogger(__name__)


def configure_management_credentials(device, credentials='default', username=None, password=None):
    ''' Configure management credentials.

    Configures aaa new model with login and exec default to local authentication.
    Adds username and password based on the credentials specified in the testbed.

    Args:
        device ('obj'): device object
        credentials ('str'): name of the credentials from the testbed. Default: 'default'
        username ('str'): username to configure, overrides username from credentials
        password ('str'): password to configure, overrides password from credentials
    '''
    try:
        creds = device.credentials
    except AttributeError:
        creds = {}

    username = username or creds.get(credentials, {}).get('username')
    password = password or to_plaintext(creds.get(credentials, {}).get('password', ''))

    config = []
    if username and password:
        config.extend([
            'aaa new-model',
            'aaa authentication login default local',
            'aaa authorization exec default local',
            f'username {username} password {password}'
        ])

    if config:
        device.configure(config)


def configure_management_vrf(device, vrf=None, protocols=None):
    ''' Configure management VRF on the device if it does not exist.

    Executes 'show vrf' to check if the VRF exits, if it does not exist,
    configures the VRF. Configures both ipv4 and ipv6 protocols by default.

    Args:
        device ('obj'): device object
        vrf ('str'): VRF name
        protocols ('list'): List of protocols, default: ['ipv4', 'ipv6']

    Returns:
        None

    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    vrf = vrf or management.get('vrf')

    if not vrf:
        return

    protocols = protocols or ['ipv4', 'ipv6']

    try:
        vrfs = device.parse('show vrf')
    except Exception:
        vrfs = {}

    vrf_config = []

    if vrf not in vrfs.get('vrf', {}):
        vrf_config.append(f'vrf definition {vrf}')

    for p in protocols:
        if p not in vrfs.get('vrf', {}).get(vrf, {}).get('protocols', []):
            vrf_config.extend([
                f'address-family {p}',
                'exit-address-family'
            ])

    if vrf_config:
        device.configure(vrf_config)


def configure_management_ip(device,
                            address=None,
                            interface=None,
                            vrf=None,
                            dhcp_timeout=30):
    '''
    Configure management ip on the device.

    Args:
        device ('obj'):  device object
        address ('dict'):  Address(es) to configure on the device (syntax: address/mask) (optional)
             ipv4 ('str') or ('list'): ipv4 address
             ipv6 ('str') or ('list'): ipv6 address
        interface ('str'): management interface (optional)
        vrf ('str'): interface VRF (optional)
        dchp_timeout ('int'): DHCP timeout in seconds (default: 30)

    Returns:
        None

    Examples:

        # Configure IP on interface
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv4': '1.1.1.1/24'})

        # Use config details from device in testbed
        #
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv4: '1.1.1.1/24'
        #        ipv6: '2001::123/64'

        # api picks up ip from testbed
        device.api.configure_management_ip()

        # IPv6 management address in a VRF
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv6': '2001::123/64'}, vrf='Mgmt-vrf')

        # Multiple addresses
        device.api.configure_management_ip(interface='GigabitEthernet0', address={'ipv4': ['1.1.1.1/24'], 'ipv6': ['2001::123/64']})

        # The api also supports the ipv4/ipv6 dhcp and ipv6/autoconfig.
        # Use config details from device in testbed
        # Example 1: (ipv4/ipv6 dhcp)
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv4: 'ipv4/dhcp'
        #        ipv6: 'ipv6/dhcp'
        #
        # Example 2: (ipv6 autoconfig)
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv6: 'ipv6/autoconfig'

        # api picks up ip from testbed
        device.api.configure_management_ip()
    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    address_dict = address or management.get('address')
    address = []

    # To process ipv4 and ipv6 address
    if address_dict:

        ipv4 = address_dict.get('ipv4')
        if ipv4 and not isinstance(ipv4, list):
            ipv4 = [ipv4]
            address += ipv4
        elif ipv4:
            address += ipv4

        ipv6 = address_dict.get('ipv6')
        if ipv6 and not isinstance(ipv6, list):
            ipv6 = [ipv6]
            address += ipv6
        elif ipv6:
            address += ipv6

    interface = interface or management.get('interface')
    vrf = vrf or management.get('vrf')

    device.api.configure_management_vrf(vrf)

    if interface:
        interface_config = [f'interface {interface}']
        if vrf:
            interface_config.append(f'vrf forwarding {vrf}')
    else:
        interface_config = []

    wait_ipv4_dhcp = False

    if interface and address:
        seq = 0
        for addr in address:

            if addr == 'ipv4/dhcp':
                interface_config.append('ip address dhcp')
                wait_ipv4_dhcp = True
                continue
            elif addr == 'ipv6/dhcp':
                interface_config.append('ipv6 address dhcp')
                continue
            elif addr == 'ipv6/autoconfig':
                interface_config.append('ipv6 address autoconfig')
                interface_config.append('ipv6 enable')
                continue

            ip_address = ipaddress.ip_interface(addr)

            if isinstance(ip_address, ipaddress.IPv6Interface):
                interface_config.append(f'ipv6 address {ip_address}')
                interface_config.append('ipv6 enable')
            else:
                seq += 1
                if seq > 1:
                    interface_config.append(f'ip address {ip_address.ip} {ip_address.netmask} secondary')
                else:
                    interface_config.append(f'ip address {ip_address.ip} {ip_address.netmask}')

    if interface_config:
        interface_config.append('no shutdown')
        device.configure(interface_config)

        if wait_ipv4_dhcp:
            timeout = Timeout(dhcp_timeout, 10)
            while timeout.iterate():
                interface_info = device.parse(f'show ip interface {interface}')
                if interface_info.q.contains('dhcp_negotiated'):
                    timeout.sleep()
                else:
                    assigned_ip = interface_info.q.get_values('ipv4')[0]
                    log.info(f'IP address assigned via DHCP: {assigned_ip}')
                    break
            else:
                log.error('No IP address was assigned via DHCP')


def configure_management_gateway(device,
                                 gateway=None,
                                 vrf=None):

    '''
    Configure management gateway on the device.

    Args:
        device ('obj'):  device object
        gateway: (dict, optional) Gateway address(es) for default route
             ipv4 ('str') or ('list'): ipv4 gateway address
             ipv6 ('str') or ('list'): ipv6 gateway address
        vrf ('str'): interface VRF (optional)

    Returns:
        None

    Examples:

        # Use config details from device in testbed
        #
        # R1:
        #   management:
        #     interface: GigabitEthernet0
        #     address:
        #        ipv4: '1.1.1.1/24'
        #        ipv6: '2001::123/64'
        #     gateway:
        #        ipv4: '1.1.1.1'
        #        ipv6: '2001::123/64'


        # Address and gateway
        device.api.configure_management_gateway(gateway={'ipv4': '1.1.1.254'})
    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    gateway_dict = gateway or management.get('gateway')
    gateway = []

    # To process ipv4 and ipv6 address
    if gateway_dict:

        ipv4 = gateway_dict.get('ipv4')
        if ipv4 and not isinstance(ipv4, list):
            ipv4 = [ipv4]
            gateway += ipv4
        elif ipv4:
            gateway += ipv4

        ipv6 = gateway_dict.get('ipv6')
        if ipv6 and not isinstance(ipv6, list):
            ipv6 = [ipv6]
            gateway += ipv6
        elif ipv6:
            gateway +=ipv6

    if gateway:
        # capture existing default routes for IPv4
        if vrf:
            default_route_show_cmd = f'show running-config | include ip route vrf {vrf} 0.0.0.0 0.0.0.0'
        else:
            default_route_show_cmd = 'show running-config | include ip route 0.0.0.0 0.0.0.0'
        existing_config = device.execute(default_route_show_cmd).splitlines()

        if not isinstance(gateway, list):
            gateway = [gateway]
        default_route_config = []
        for gw in gateway:
            gateway_address = ipaddress.ip_address(gw)
            if isinstance(gateway_address, ipaddress.IPv6Address):
                default_route_cmd = f'ipv6 route'
                if vrf:
                    default_route_cmd += f' vrf {vrf}'
                default_route_cmd += f' ::/0 {gw}'
            else:
                default_route_cmd = f'ip route'
                if vrf:
                    default_route_cmd += f' vrf {vrf}'
                default_route_cmd += f' 0.0.0.0 0.0.0.0 {gw}'

            if default_route_cmd in existing_config:
                existing_config.remove(default_route_cmd)
            else:
                default_route_config.append(default_route_cmd)

        if existing_config:
            remove_existing_config = [f'no {line}' for line in existing_config]
            device.configure(remove_existing_config)

        if default_route_config:
            device.configure(default_route_config)


def configure_management_routes(device,
                                routes=None,
                                vrf=None):
    '''
    Configure management routes on the device.

    Args:
        device ('obj'):  device object
        routes: ('dict', optional)
             ipv4 (list of 'dict'): ipv4 routes
                - subnet: (str) subnet including mask
                  next_hop: (str) next_hop for this subnet
             ipv6 (list of 'dict'): ipv6 routes
                - subnet: (str) subnet including mask
                  next_hop: (str) next_hop for this subnet
        vrf ('str'): interface VRF (optional)

    Returns:
        None

    Examples:
        # Routes
        device.api.configure_management(routes={
        'ipv4': [{
            'subnet': '192.168.1.0 255.255.255.0',
            'next_hop': '172.16.1.1'
        }],
         'ipv6': [{
            'subnet': '2001::123/64',
            'next_hop': '2002::123/64'
        }]
        })
    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    routes_dict = routes or management.get('routes')
    if routes_dict is None:
        return

    routes = []
    # To process ipv4 and ipv6 routes
    ipv4 = routes_dict.get('ipv4')
    if ipv4 and not isinstance(ipv4, list):
        ipv4 = [ipv4]
        routes += ipv4
    elif ipv4:
        routes += ipv4

    ipv6 = routes_dict.get('ipv6')
    if ipv6 and not isinstance(ipv6, list):
        ipv6 = [ipv6]
        routes += ipv6
    elif ipv6:
        routes += ipv6

    if routes:
        route_cmds = []
        for route in routes:
            # By default protocol is ip
            protocol = 'ip'
            subnet = route.get('subnet')
            next_hop = route.get('next_hop')
            if subnet and next_hop:
                if vrf:
                    cmd = f'{protocol} route vrf {vrf} {subnet} {next_hop}'
                else:
                    cmd = f'{protocol} route {subnet} {next_hop}'
                route_cmds.append(cmd)
        if route_cmds:
            device.configure(route_cmds)


def configure_management_tftp(device,
                              source_interface=None):
    '''
    Configure device for management via tftp.

    Args:
        device ('obj'):  device object
        source_interface ('str'): management interface (optional)

    Returns:
        None
    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    source_interface = source_interface or management.get('interface')

    tftp_config = []

    if source_interface:
        tftp_config.append(f'ip tftp source-interface {source_interface}')

    if tftp_config:
        device.configure(tftp_config)


def configure_management_http(device,
                              source_interface=None):

    '''
    Configure device for management via http.

    Args:
        device ('obj'):  device object
        source_interface ('str'): management interface (optional)

    Returns:
        None
    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    source_interface = source_interface or management.get('interface')

    http_config = []

    if source_interface:
        http_config.append(f'ip http source-interface {source_interface}')

    if http_config:
        device.configure(http_config)


def configure_management_ssh(device,
                             credentials='default',
                             username=None,
                             password=None,
                             domain_name='cisco.com'):
    '''
    Configure device for management via ssh.

    Args:
        device ('obj'):  device object
        credentials ('str'): credentials to authenticate
        username ('str', optional): username to ssh
        password ('str', optional): password to ssh
        domain_name ('str'): domain name to ssh

    Returns:
        None
    '''
    ssh_config = []

    device.api.configure_management_credentials(credentials,
        username=username, password=password)

    if domain_name:
        ssh_config.append(f'ip domain name {domain_name}')

    ssh_config.extend([
        'crypto key generate rsa',
    ])

    dialog = Dialog([
        [r'How many bits in the modulus \[\d+\]:\s*$', 'sendline()', None, True, False],
        [r'Do you really want to replace them\? \[yes/no\]:\s*$', 'sendline(yes)', None, True, False]
        ])
    device.configure(ssh_config, reply=dialog)

    device.api.configure_management_vty_lines(
        authentication='default',
        transport='ssh')


def configure_management_telnet(device,
                                credentials='default',
                                username=None,
                                password=None):
    '''
    Configure device for management via telnet.

    Args:
        device ('obj'):  device object
        credentials ('str'): credentials to authenticate
        username ('str', optional): username to ssh
        password ('str', optional): password to ssh

    Returns:
        None
    '''
    device.api.configure_management_credentials(credentials,
        username=username, password=password)

    device.api.configure_management_vty_lines(
        authentication='default',
        transport='telnet')


def configure_management_vty_lines(device,
                                   authentication=None,
                                   transport=None):
    '''
    Configure device for management via vty lines.

    Args:
        device ('obj'):  device object
        authentication ('str'): authentication details
        transport ('str'): transport details

    Returns:
        None
    '''
    if not isinstance(transport, list):
        transport = [transport]

    vty_config = []

    output = device.execute('show running-config | section line vty')

    # get all virtual terminal lines
    lines = re.findall(r'line vty (\d+) (\d+)', output)
    lines_start = lines[0][0]
    lines_end = lines[-1][1]
    vty_config.append(f'line vty {lines_start} {lines_end}')

    if authentication and f'login authentication {authentication}' not in output:
        vty_config.append(f'login authentication {authentication}')

    # find all transports
    all_transports = re.findall(r'transport input (.*)', output)
    transports = []
    for t in all_transports:
        transports.extend(t.strip().split(' '))
    # remove duplicates and ignore "all"
    transports = [t for t in set(transports) if t != 'all']
    for t in transport:
        if t not in transports:
            transports.append(t)

    transport_config = 'transport input {}'.format(' '.join(transports))
    vty_config.append(transport_config)

    device.configure(vty_config)


def configure_management_netconf(device,
                                 credentials='default',
                                 username=None,
                                 password=None,
                                 domain_name='cisco.com'):
    '''
    Configure device for management via netconf.

    Args:
        device ('obj'):  device object
        credentials ('str'): credentials to authenticate
        username ('str'): username to ssh
        password ('str'): password to ssh
        domain_name ('str'): domain name to do netconf

    Returns:
        None
    '''
    device.api.configure_management_ssh(
        credentials=credentials,
        username=username,
        password=password,
        domain_name=domain_name)

    netconf_config = ['netconf-yang']
    device.configure(netconf_config)


def configure_management_protocols(device,
                                   protocols=None):
    '''
    Configure the device management protocols.

    Args:
        device ('obj'):  device object
        protocols ('list', optional): [list of protocols]

    Returns:
        None

    device:
        R1:
            management:
                protocols:
                - http
                - tftp
                - telnet
                - ssh
                - netconf

    '''

    try:
        management = device.management
    except AttributeError:
        management = {}

    protocols = protocols or management.get('protocols', [])

    for proto in protocols:
        if hasattr(device.api, f'configure_management_{proto}'):
            func = getattr(device.api, f'configure_management_{proto}')
            func()
        else:
            log.warning(f'Protocol {proto} does not have a configure API, ignoring')


def configure_management(device,
                         address=None,
                         gateway=None,
                         vrf=None,
                         interface=None,
                         routes=None,
                         dhcp_timeout=30,
                         protocols=None,
                         set_hostname=False):
    ''' Configure management connectivity on the device.

    Arguments can be provided with the management connectivity information. By default,
    information is taken from the testbed device.management section.

    Testbed schema:

        device:
            management:
                interface: (str) Management interface to use
                vrf: (str) VRF to use for management interface
                protocols: [list of protocols]
                address ('dict'):  Address(es) to configure on the device (syntax: address/mask) (optional)
                   ipv4 ('str') or ('list'): ipv4 address
                   ipv6 ('str') or ('list'): ipv6 address
                gateway: (dict) Gateway address(es) for default route
                   ipv4 ('str') or ('list'): ipv4 gateway address
                   ipv6 ('str') or ('list'): ipv6 gateway address
                routes: ('dict')
                   ipv4 (list of 'dict'): ipv4 routes
                      - subnet: (str) subnet including mask
                        next_hop: (str) next_hop for this subnet
                   ipv6 (list of 'dict'): ipv6 routes
                      - subnet: (str) subnet including mask
                        next_hop: (str) next_hop for this subnet

    Args:
        device ('obj'):  device object
        address ('dict', optional):  Address(es) to configure on the device (syntax: address/mask) (optional)
            ipv4 ('str') or ('list'): ipv4 address
            ipv6 ('str') or ('list'): ipv6 address
        gateway: (dict, optional) Gateway address(es) for default route
            ipv4 ('str') or ('list'): ipv4 gateway address
            ipv6 ('str') or ('list'): ipv6 gateway address
        vrf: (str, optional) VRF to use for management interface
        interface: (str, optional) Management interface to use
        routes: ('dict', optional)
           ipv4 (list of 'dict'): ipv4 routes
              - subnet: (str) subnet including mask
                next_hop: (str) next_hop for this subnet
           ipv6 (list of 'dict'): ipv6 routes
              - subnet: (str) subnet including mask
                next_hop: (str) next_hop for this subnet
        dhcp_timeout ('int', optional): DHCP timeout in seconds (default: 30)
        protocols ('list', optional): [list of protocols]
        set_hostname (bool): Configure hostname on the device (default: False)
    '''
    try:
        management = device.management
    except AttributeError:
        management = {}

    address = address or management.get('address')
    gateway = gateway or management.get('gateway')
    interface = interface or management.get('interface')
    routes = routes or management.get('routes')
    vrf = vrf or management.get('vrf')

    if set_hostname:
        device.configure(f'hostname {device.name}')

    device.api.configure_management_vrf(vrf)

    device.api.configure_management_ip(
        interface=interface,
        address=address,
        vrf=vrf,
        dhcp_timeout=dhcp_timeout)

    device.api.configure_management_gateway(
        gateway=gateway,
        vrf=vrf)

    device.api.configure_management_routes(
        routes=routes,
        vrf=vrf)

    device.api.configure_management_protocols(
        protocols=protocols
    )

def unconfigure_netconf_yang_polling(device):
    """ configure unconfigure netconf_yang cisco-odm parameters polling enable
    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure unconfigure netconf_yang cisco-odm parameters polling enable
    """
    config = [f"no netconf-yang cisco-odm polling-enable"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure unconfigure netconf_yang cisco-odm parameters polling enable. Error:\n{e}")
    
def configure_mtc(device, version, interface=None, protocol=None, address=None):
    """ Configure parameters for mtc 
    Args:
        device ('obj'): device object
        version ('str'): protocol version ipv4 or ipv6
        interface ('str') or ('list'): interface of mtc
        protocol ('str') or ('list'): protocols of mtc
        address ('str'): mtc ipv4 or ipv6 address
    
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f'mgmt-traffic control {version}']

    if interface:
        if isinstance(interface,str):
            cmd.append(f'interface {interface}')
        else:
            for intf in interface:
                cmd.append(f'interface {intf}')

    if protocol:
        if isinstance(protocol,str):
            cmd.append(f'protocol {protocol}')
        else:
            for proto in protocol:
                cmd.append(f'protocol {proto}')

    if address:
        cmd.append(f'address {address}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure the parameter under mtc. Error:\n{e}')
    
def unconfigure_mtc_parameters(device, version, interface=None, protocol=None):
    """ Unconfigure parameters for mtc 
    Args:
        device ('obj'): device object
        version ('str'): protocol version ipv4 or ipv6
        interface ('str') or ('list'): interface under mtc
        protocol ('str') or ('list'): protocols of mtc
    
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f'mgmt-traffic control {version}']

    if interface:
        if isinstance(interface,str):
            cmd.append(f'no interface {interface}')
        else:
            for intf in interface:
                cmd.append(f'no interface {intf}')

    if protocol:
        if isinstance(protocol,str):
            cmd.append(f'no protocol {protocol}')
        else:
            for proto in protocol:
                cmd.append(f'no protocol {proto}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure the parameter under mtc. Error:\n{e}')
    
def unconfigure_mtc(device, version):
    """ Unconfigure mtc 
    Args:
        device ('obj'): device object
        version ('str'): protocol version ipv4 or ipv6
    
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f'no mgmt-traffic control {version}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure mtc. Error:\n{e}')
            
def configure_netconf_yang_intelligent_sync(device):
    """ Configure netconf-yang cisco-ia intelligent-sync
    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure netconf-yang cisco-ia intelligent-sync
    """
    cmd = "netconf-yang cisco-ia intelligent-sync"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure netconf-yang cisco-ia intelligent-sync. Error:\n{e}")

def unconfigure_netconf_yang_intelligent_sync(device):
    """ Unconfigure netconf-yang cisco-ia intelligent-sync
    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure netconf-yang cisco-ia intelligent-sync
    """
    cmd = "no netconf-yang cisco-ia intelligent-sync"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure netconf-yang cisco-ia intelligent-sync. Error:\n{e}")

def configure_ip_ssh_version(device, version):
    
    """ Configure ip ssh version
        Args:
            device ('obj'): Device object
            version('str'): ssh version
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip ssh version {version}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip ssh version on device {device}. Error:\n{e}")

def unconfigure_ip_ssh_version(device, version):
    
    """ Unconfigure ip ssh version
        Args:
            device ('obj'): Device object
            version('str'): ssh version
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no ip ssh version {version}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip ssh version on device {device}. Error:\n{e}")

def configure_line_vty_needs_enhancement(device,firstline_id,lastline_id,min,sec):
    """ configure_line_vty_needs_enhancement 
        Args:
            device ('obj'): device to execute on
            firstline_id ('int') : firstline identifier
            lastline_id ('int') :  lastline identifier   
            min ('int') : timeout in minutes
            sec ('int') : timeout in seconds    

        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = ["line vty {firstline_id} {lastline_id}".format(firstline_id=firstline_id,lastline_id=lastline_id),
           "transport preferred ssh",
           "exec-timeout {min} {sec}".format(min=min,sec=sec),
           "transport input all",
           "transport output all"]   
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure_line_vty_needs_enhancement Error {e}".format(e=e))