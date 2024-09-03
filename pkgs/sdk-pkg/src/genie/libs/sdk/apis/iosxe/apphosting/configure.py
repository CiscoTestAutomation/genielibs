''' Common Config functions for IOX / app-hosting '''

import logging
import time
import inspect

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.utils.timeout import Timeout


def enable_usb_ssd(device, timeout=30):
    '''
    Configure - no platform usb disable
    Enables connected SSDs on c9300
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI
    Returns:
        None
    '''

    try:
        output = device.configure("no platform usb disable" , timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable USB SSD - Error:\n{error}".format(error=e)
        )

def disable_usb_ssd(device, timeout=30):
    '''
    Configure - platform usb disable
    Disables connected SSDs on c9300
    Args:
        device ('obj') : Device object
        timeout ('int'): timeout arg for Unicon configure for this CLI
    Returns:
        None
    '''

    try:
        output = device.configure("platform usb disable" , timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable USB SSD - Error:\n{error}".format(error=e)
        )

def clear_iox(device, max_time=120, interval=10, disable_iox_then_clear=False,wait_timer=30,timeout=30):
    '''
    Execute clear iox
    Uses disable_iox
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
        disable_iox_then_clear ('boolean') : Disable IOX then clear
        wait_timer ('int') : wait timer after disable IOX if disable_iox_then_clear
        timeout ('int'): timeout arg for Unicon execute for this CLI
    Returns:
        True
        False
    Raises:
        None
    '''

    time_out = Timeout(max_time=max_time, interval=interval)
    while time_out.iterate():
        try:
            output = device.execute("clear iox" , timeout=timeout)
            if 'IOX cleanup successfully completed' in output:
                return True
            elif 'IOX is configured/UP. IOX must be disabled before invoking this command' in output:
                if disable_iox_then_clear:
                    log.info("User requested unconfigure IOX then clear IOX")
                    device.api.disable_iox()
                    log.info('Wait %s seconds after Disable IOX' % wait_timer)
                    time.sleep(wait_timer)
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not clear IOX - Error:\n{error}".format(error=e)
            )
    return False

def enable_iox(device):
    '''
    Configure iox
    Args:
        device ('obj') : Device object
    Returns:
        None
    '''
    try:
        device.configure("iox")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable IOX - Error:\n{error}".format(error=e)
        )

def disable_iox(device):
    '''
    Configure no iox
    Args:
        device ('obj') : Device object
    Returns:
        None
    '''
    try:
        device.configure("no iox")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable IOX - Error:\n{error}".format(error=e)
        )


def configure_thousand_eyes_application(device, vlan_id, app_ip, app_gateway_ip,
                app_netmask, thousand_eye_token, app_proxy, app_dns):
    '''
    Configure Thousand Eye Application
    Args:
        device ('obj'): Device object
        vlan_id ('str'): Vlan information App installation
        app_ip ('str'):  Public IP for Thousand Eye Application
        app_gateway_ip ('str'): gateway IP for Application
        app_netmask ('str'):  Subnet mask for the Public IP used to configure Thousand Eye application
        thousand_eye_token ('str'): Thousand Eye Application Token
        app_proxy ('str'): Proxy details for application
        app_dns ('str'): Domain name server Ip address
    Returns:
        None
    Raises:
        SubCommandFailure

    '''

    log.info("User requested Configure Thousand Eye Application")

    cmd = [
            "no app-hosting appid 1keyes",
            "app-hosting appid 1keyes",
            "app-vnic AppGigabitEthernet trunk",
            "vlan {vlan_id} guest-interface 0".format(vlan_id=vlan_id),
            "guest-ipaddress {app_ip} netmask {app_netmask}".format(app_ip=app_ip,app_netmask=app_netmask),
            "app-default-gateway {app_gateway_ip} guest-interface 0".format(app_gateway_ip=app_gateway_ip),
            "app-resource docker",
            "prepend-pkg-opts",
            "run-opts 1 \"-e TEAGENT_ACCOUNT_TOKEN={thousand_eye_token}\"".format(thousand_eye_token=thousand_eye_token),
            "run-opts 3 \"-e TEAGENT_PROXY_TYPE=STATIC\"",
            "run-opts 4 \"-e TEAGENT_PROXY_LOCATION={app_proxy}\"".format(app_proxy=app_proxy),
            "name-server0 {app_dns}".format(app_dns=app_dns),
            "start"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configure Thousand Eye Application Config. Error {e}".format(e=e)
        )


def configure_app_hosting_appid_iperf_from_vlan(device,port_id,vlan_id):
    """ configure_app_hosting_appid_iperf_from_vlan
        Args:
            device ('obj'): device to execute on
            port_id(int): port identifier
            vlan_id('str'): vlan identifier

        Return:
            None
        Raises:
            SubCommandFailure
    """
    cmd = ["app-hosting appid iperf",
           "app-vnic AppGigabitEthernet port {port_id} trunk".format(port_id=port_id),
           "Vlan {vlan_id} guest-interface 0".format(vlan_id=vlan_id),
           "start"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure_app_hosting_appid_iperf_from_vlan Error {e}".format(e=e))


def configure_app_hosting_appid_trunk_port(device, appid, app_vnic, app_vnic_port=None,
                app_vnic_port_mode=None, app_vnic_guest_interface=None, vlan_id=None,
                app_ip=None, app_netmask=None, app_gateway_ip=None, start=False):
    """
        Configure app-hosting appid
        Args:
            device ('obj'): Device object
            appid ('str'): app-hosting appid
            app_vnic ('str'): app-hosting app-vnic type
            app_vnic_port ('int', optional): app-vnic port number of interface. Default is None
            app_vnic_port_mode ('str', optional): access or trunk port mode. Default is None
            app_vnic_guest_interface ('str', optional): guest-interface name. Default is None
            vlan_id ('str', optional): Vlan information App installation. Default is None
            app_ip ('str', optional):  Public IP for Thousand Eye Application. Default is None
            app_netmask ('str', optional):  Subnet mask for the Public IP. Default is None
            app_gateway_ip ('str', optional): gateway IP for Application. Default is None
            start ('bool', optional): True to start the Application. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure

    """

    config = [f'app-hosting appid {appid}', f'app-vnic {app_vnic}']

    # cmd = f'app-vnic {app_vnic}'
    if app_vnic_port:
        config[1] += f' port {app_vnic_port} {app_vnic_port_mode}'
    if app_vnic_guest_interface != None:
        config[1] += f' guest-interface {app_vnic_guest_interface}'

    if vlan_id:
        config.append(f'vlan {vlan_id} guest-interface 0')
    if app_ip and app_netmask:
        config.append(f'guest-ipaddress {app_ip} netmask {app_netmask}')
    if app_gateway_ip:
        config.append(f'app-default-gateway {app_gateway_ip} guest-interface 0')
    if start:
        config.append('start')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure app-hosting appid. Error {e}")


def configure_app_hosting_appid_docker(device, appid, prepend_pkg_opts=True, run_opts=[]):
    """
        Configure app-hosting appid resource docker
        Args:
            device ('obj'): Device object
            appid ('str'): app-hosting appid
            prepend_pkg_opts ('bool', optional): configure prepend-pkg-opts. Default is True
            run_opts ('list', optional): list of dictinaries.
            For ex:
                [
                    {'index': 1, 'string': '-e TEAGENT_PROXY_LOCATION=proxy-wsa.esl.cisco.com:80'},
                    {'index': 3, 'string': '-e TEAGENT_PROXY_TYPE=STATIC'},
                ]
        Returns:
            None
        Raises:
            SubCommandFailure

    """

    config = [f'app-hosting appid {appid}', 'app-resource docker']

    if prepend_pkg_opts:
        config.append('prepend-pkg-opts')

    for run_opt in run_opts:
        config.append(f'run-opts {run_opt["index"]} "{run_opt["string"]}"')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure app-hosting appid resource docker. Error {e}")


def configure_app_hosting_resource_profile(device, appid, profile_name, cpu=None, cpu_percent=None,
                                           memory=None, vcpu=None, start=False):
    """
        Configure app-hosting appid resource custom profile
        Args:
            device ('obj'): Device object
            appid ('str'): app-hosting appid
            profile_name ('srt'): app-resource profile name
            cpu ('int', optional): application CPU units/share quota. Default is None
            cpu_percent ('int', optional): application cpu percent. Default is None
            memory ('int', optional): memory reservation MB units. Default is None
            vcpu ('int', optional): application VCPU count. Default is None
            start ('bool', optional): True to start the Application. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure

    """

    config = [f'app-hosting appid {appid}', f'app-resource profile {profile_name}']

    if cpu:
        config.append(f'cpu {cpu}')
    if cpu_percent:
        config.append(f'cpu-percent {cpu_percent}')
    if memory:
        config.append(f'memory {memory}')
    if vcpu:
        config.append(f'vcpu {vcpu}')
    if start:
        config.append(f'start')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure app-hosting appid resource custom profile. Error {e}")


def unconfigure_app_hosting_appid(device, appid=''):
    """ Unconfigure app-hosting appid
        Args:
            device ('obj'): device to use
            appid ('str'): app-hosting appid
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"no app-hosting appid {appid}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure app-hosting appid. Error: {e}')

def confirm_iox_enabled_requested_storage_media(device, storage='ssd'):
    """Confirm iox enabled requested storage media
    Args:
        device('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    log.debug("Entering " + inspect.currentframe().f_code.co_name)
    local_args = locals()
    log.debug("Passed in arguments are")
    log.debug(local_args)
    log.debug("Called by function name " + inspect.currentframe().f_back.f_code.co_name)

    if storage not in ["ssd", "alt_hdd"]:
        log.error("Passed in value of storage not supported!")
        return False
    storage_map = {
        "ssd": {
            "req_storage_string": "/vol/usb1",
            "mod_storage_string": "/flash1/",
            "sso_storage_string": "/vol/disk0",
            "other_storage": "/mnt/sd3"
        },
        "alt_hdd": {
            "req_storage_string": "/mnt/sd3",
            "mod_storage_string": "/flash1/",
            "sso_storage_string": "/vol/disk0",
            "other_storage": "/vol/usb1"
        }
    }
    
    storage_strings = storage_map[storage]
    result = False
    output = []
    for attempt in range(1, 10):
        try:
            output = device.parse('show app-hosting infra')
            log.debug(output)
            break
        except Exception as e:
            log.info("Wait 10 seconds and try again! With message \n {error}".format(error=e))
            time.sleep(10)
            continue
        except:
            log.error("Problem with parsing show app-hosting infra CLI")
            return False

    if not output:
        log.error("Failed to parse show app-hosting infra!")
        return False
    internal_storage = output['internal_working_directory']

    for key, storage_string in storage_strings.items():
        if storage_string in internal_storage:
            if key == "other_storage":
                log.error('IOX brought up on the other Storage Media Instead! - Error!')
                return False
            log.info(f'IOX brought up on Requested Storage {storage} \n with location {storage_string} successfully!')
            return True
    log.error('IOX not brought up properly! - Error!')
    return False

def enable_usb_ssd_verify_exists(device, storage_name="usbflash1:.",timeout=30):
    """ configure app-hosting appid
        Args:
            device ('obj'): device to use
            storage_name('str'): storage name eg:flash or bootflash
            timeout('int'): time
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        out = device.api.get_show_output_include(command='show running-config', filter='platform usb disable')
        if out[0]: # if we get True
            device.api.enable_usb_ssd()
            time.sleep(timeout)
        output = device.parse("show version")

        try:
            if output['version']['disks'][storage_name]:
                log.info(output['version']['disks'])
                return True
            else:
                log.info(output['version'])
                return False
        except SubCommandFailure as e:
            log.error("Problem with parsing show version CLI")
            return False
    except SubCommandFailure as e:
        log.error(f"Problem with parsing show version CLI. Error:\n{e}")
        return False


def configure_app_management_networking(device, app_name="guestshell", auto_start=None):
    '''
    Args:
            device ('obj'): device to use
            app_name('str'): WORD  no description
            auto_start('str'): Application start
        Returns:
            True/False
        Raises:
            SubCommandFailure
    '''

    log.info("Configuring APP %s with basic Mgmt Interface config - app-vnic management guest-interface 0" % app_name)
    config = [f'app-hosting appid {app_name}',f'app-vnic management guest-interface 0']

    if auto_start:
        config.append('start')

    try:
        device.configure(config)
        return True 
    except SubCommandFailure as e:
        log.error(f"Couldn't configure app management networking. Error:\n{e}")
        return False 