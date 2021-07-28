'''IOSXE configure functions for meraki'''

# Python
import re
import time

# Genie
from genie.utils.timeout import Timeout

# Banner
from pyats.log.utils import banner

# Logger
import logging
log = logging.getLogger(__name__)

# Unicon
from unicon import Connection
from unicon.core.errors import (
    SubCommandFailure,
    TimeoutError,
    ConnectionError,
)
from unicon.eal.dialogs import Statement, Dialog



def configure_meraki_register(device, token, mac_address):
    """
    This method is used to register the device to meraki dashboard
    It uses token, mac-address
        Args:
            device ("obj"): Device object
            token ("str"): Token used for registration eg: Q2ZZ-2RT8-9D9P
            mac_address: MAC Address of the device eg: 00:18:0a:00:58:ef
        Raises:
            Exception

        Returns:
            True if succeeded else False
    """

    dialog = Dialog([
        Statement(
            pattern=r"Enter token for switch +(\d+):",
            action="sendline({})".format(token),
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r"Check if token is entered correctly? \[confirm\].*",
            action="sendline()",
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=r"Enter Mac addr or just Return to use switch's Base Mac Addr. Enter Mac Addr for switch +(\d+) in hh:hh:hh:hh:hh:hh:",
            action="sendline({})".format(mac_address),
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(pattern=r"Check if mac address is entered correctly? \[confirm\].*",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False
                  ),
        Statement(pattern=r"Mac address is .*",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False)
    ])

    cmd = 'service meraki register token {}'.format(token)
    try:
        device.execute(cmd, reply=dialog)
    except Exception as err:
        log.error("Failed to register the device correctly: {err}".format(err=err))
        raise Exception(err)


def configure_conversion_reversion(device, via_console, mode='conversion', reload_timeout=5000,
                                   username=None,
                                   password=None,
                                   reload_hostname='Switch',
                                   m_user="miles",
                                   m_pwd="ikarem",
                                   m_enable="Meraki12345",
                                   reload_creds=None,
                                   device_online_status_timeout=1000,
                                   retry=30,
                                   interval=10,
                                   api_key='0',
                                   serial='0',
                                   organization_id='0'):
    """
    This method verifies if the device is ready for conversion from CAT9K Classic mode
    to Meraki Mode.
    It verifies the device is ready by using 'show meraki' command.
    Once the device is ready, it execute 'service meraki start'
    which will reload the device and come up in Meraki mode.
    This will also calculates the time taken to connect to the dashboard.
        Args:
                device ("obj"): Device object
                via_console(`str`): Via to use to reach the device console.
                mode ("str"): Type of mode to be executed : 'conversion' or 'reversion'
                reload_timeout ("int"): How long to wait after the reload starts
                username ("str"): Username after conversion
                password ("str"): Password after conversion
                reload_hostname ("str"): reload_hostname after conversion will be 'Switch'
                m_user ("str"): Meraki Default Username
                m_pwd ("str"): Meraki Default Password
                m_enable ("str"): Meraki Default Enable Password
                reload_creds ("str"): Reload Credentials like device, hostname etc..
                device_online_status_timeout ("int"): Retry secs for the device to come online after conversion
                retry ("int"):  Number of retries to be handled to check the device state
                interval ("int"): Sleep time between the retries
                api_key ('str"): API Key to connect to the dashboard
                serial ("str"): Serial / Token number of the device used to connect to dashboard
                organization_id ("str"): Org Id where the device is connected in dashboard

        Raises:
            Exception

        Returns:
            True if succeeded else False
    """

    if mode == 'conversion':
        mode_check = 'C9K-C'
        dialog = Dialog([
            Statement(
                pattern=r"Proceeding with conversion will permanently erase all data "
                        r"and the device can only be managed by Cisco Meraki dashboard. "
                        r"Continue\?  \[Y\/N\]\[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"Continue \[Y\/N\]\[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(pattern=r"^.*RETURN to get started",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])
        log.info('Verify if the device is ready for conversion')
    else:
        mode_check = 'C9K-M'
        dialog = Dialog([
            Statement(
                pattern=r"proceeding with conversion is destructive to the current IOS configuration "
                        r"and will render the device to regular Cat9K "
                        r"Continue? \[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Enter host name \[Switch\]\:",
                action="sendline()",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Enter enable secret\: ",
                action="sendline(Meraki12345)",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Confirm enable secret\: ",
                action="sendline(Meraki12345)",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Enter enable password\:",
                action="sendline(Meraki12345)",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Enter virtual terminal password\:",
                action="sendline(Meraki12345)",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Community string \[public\]\:",
                action="sendline()",  # Temp password will be removed later
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*management network from the above interface summary\:",
                action="sendline(GigabitEthernet0/0)",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*IP address for this interface \[+\S+\]\:",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Subnet mask for this interface \[+\S+\] \:",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*Enter your selection \[2\]\:",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r"^.*OK to enter CLI now\.\.\.",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(pattern=r"^.*RETURN to get started",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])
        log.info('Verify if the device is ready for reversion')

    os = device.os
    hostname = device.name

    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])

    # Execute 'show meraki' and check the status of registration and the mode.
    # Switch#show meraki
    # Switch              Serial                                   Conversion
    # Num PID             Number      Meraki SN     Mac Address    Status          Mode
    # 5  C9300-24T       FJC2328U02M Q2ZZ-8FAF-954B 0018.0a00.50b7 Registered      C9K-C
    cmd = 'show meraki'
    output = device.parse(cmd)
    if output is not None:
        for sw in output['meraki']['switch']:
            current_mode = output['meraki']['switch'][sw]['current_mode']
            conversion_status = output['meraki']['switch'][sw]['conversion_status']
            if current_mode != mode_check:
                log.error("Device is not ready, device is NOT in '{}' "
                          "mode".format(mode_check))
                return False
            if mode == 'conversion':
                if conversion_status != 'Registered':
                    log.error("Device is not ready, device is NOT Registered")
                    return False

    log.info('Device is ready for Conversion from C9K - '
             'Classic Mode to C9K - Meraki Mode')

    # Start the Conversion or Reversion according to the
    # mode specified by the user.
    log.info('Recording the time before the Conversion/Reversion')
    T00 = device.parse('show clock')
    log.info('@@#@ T00 is {}'.format(T00))
    conv_start_time = time.time()
    if mode == 'conversion':
        log.info('Execute service meraki start command')
        cmd = 'service meraki start'
    else:
        log.info('Execute service meraki stop command')
        cmd = 'service meraki stop'

    try:
        device.execute(cmd, reply=dialog, timeout=reload_timeout)
        device.disconnect()
    except SubCommandFailure:
        # Disconnect and destroy the connection
        log.info(
            "Successfully executed {} command on device {}".format(
                device.name, cmd
            )
        )
        log.info(
            "Disconnecting and destroying handle to device {}".format(
                device.name
            )
        )
        device.disconnect()
        device.destroy()
    except Exception as e:
        raise Exception(
            "Error while reloading device '{}'".format(device.name)
        ) from e

    # Reconnect to device which will be in Meraki Mode after
    # conversion or in Classic mode after reversion
    log.info(
        "\n\nReconnecting to device '{}' after conversion/reversion "
        "and reload...".format(hostname)
    )

    # Device coming up in Meraki mode has the below default startup config applied
    # Uses the default static Username "miles" and Password "ikarem" to connect to the script after conversion
    new_device = Connection(
        credentials=dict(default=dict(username=m_user, password=m_pwd),
                         enable=dict(password=m_enable)),
        os=os,
        hostname=reload_hostname,
        start=["telnet {ip} {port}".format(ip=ip, port=port)],
        prompt_recovery=True,
    )

    # Try to reconnect with iteration
    device_connected = 0
    for i in range(int(retry)):
        if device_connected:
            break
        con = new_device.connect()
        if 'Connected to' in con:
            log.info('Recording the time After the Conversion/Reversion')
            device_prompt_time = time.time()
            device_connected = 1
        else:
            time.sleep(interval)
            if i == int(retry) - 1:
                log.error('Retry connection failed')
                new_device.disconnect()  # Disconnect anyways before return
                return False

    log.info(
        "Successfully reconnected to device '{}' after 'Conversion/Reversion' "
        "and reload'".format(hostname)
    )

    new_device.configure('no enable password')  # Remove the temp password created
    new_device.configure('username {} privilege 15 password {}'
                         .format(username, password))  # Configure the original username and password
    new_device.execute('wr mem')  # Save the Config before disconnecting.
    new_device.disconnect()  # Disconnect the device

    if mode == 'conversion':
        log.info('Device from C9K-C to C9K-M Conversion happened Successfully')
        status_state = 'online'
    else:
        log.info('Device from C9K-M to C9K-C Reversion happened Successfully')
        status_state = 'offline'

    # Check the dashboard to find the status of the device

    if serial != '0' and api_key != '0' and organization_id != '0':
        try:
            import meraki  # import meraki api
        except Exception:
            log.error("Couldn't import Meraki will skip running this api")
            return True

        log.info('Connect to the Dashboard')
        dashboard = meraki.DashboardAPI(api_key)

        # Check the device status, retry until it comes online
        log.info('Check the device status, retry until it comes to the desired state')
        device_online = 0
        for i in range(int(device_online_status_timeout)):
            if device_online:
                break
            response = dashboard.organizations.getOrganizationDevicesStatuses \
                (organization_id, total_pages='all')
            for dev in response:
                if dev['serial'] == serial:
                    log.info('DEVICE Status: {}'.format(dev))
                    if dev['status'] == status_state:
                        device_status_time = time.time()
                        log.info('Device Status: {}'.format(dev))
                        log.info('---------------------------------')
                        log.info("--- %s seconds ---" % (time.time() - device_status_time))
                        log.info('---------------------------------')
                        device_online = 1
            if i == (int(device_online_status_timeout) - 1):
                log.error('Device is not Online within {} secs after '
                          'Conversion: ABORT'.format(device_online_status_timeout))
                return 0
            else:
                continue

        log.info('CALCULATE THE TIME TAKEN FOR CONVERSION OR REVERSION')
        log.info(banner('START TIME          : {}'.format(conv_start_time)))
        log.info(banner('END TIME            : {}'.format(device_prompt_time)))
        log.info(banner('DASHBOARD STATUS    : {}'.format(device_status_time)))
        conv_time = (int(device_prompt_time) - int(conv_start_time)) / 60
        dev_online = (int(device_status_time) - int(device_prompt_time)) / 60
        total_time = (int(device_status_time) - int(conv_start_time)) / 60
        log.info(banner('CONVERSION TIME             : {}'.format(conv_time)))
        log.info(banner('DEV ONLINE/OFFLINE TIME     : {}'.format(dev_online)))
        log.info(banner('TOTAL TIME                  : {}'.format(total_time)))

    return True


def _convert_seconds_to_minutes(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def _show_clock_seconds(device):
    output = device.execute('show clock')
    match_value = re.search('[0-9]+:[0-9]+:[0-9]+(\.[0-9]+)*', output)
    current_time = match_value.group(0)
    log.info('@@#@ time is %s' % time)
    tmp = current_time.split(':')
    current_time_in_sec = float(tmp[2]) + (float(tmp[1]) * 60) + (float(tmp[0]) * 60 * 60)
    output = int(current_time_in_sec)
    return output


def c9k_m_reload_with_boot_measurement(device, api_key, organization_id, serial, intf_name, reload_type='api',
                                       routable_ip='192.168.1.1', timeout=1000, intfuptimeout=200):
    """
    This method is for the reboot and boot time measurements.
    This method has to 2 options for reboot one via Dashboard Meraki API and another via CLI
    With this it measures the below steps
    Step1: Time taken for the device to go offline after reload is given
    Step2: Time taken for the device to come online after reload
    Step3: Time taken for getting the boot prompt
    Args:
        device ("obj")      : Device object
        api_key             : Dashboard API Key for connecting to Dashboard
        organization_id     : Organization Id where the device is claimed
        serial              : Serial Number/ Token of the Device
        intf_name           : Interface where the client is connected, used to verify the data after boot.
        reload_type         : Type of Reload via 'api' or via 'cli'
        routable_ip         : To Ping after the device is Up
        timeout             : Reload Timeout used at both CLI and API
        intfuptimeout       : Timeout Used for Interface to come up, used in CLI.

        Raises:
            Exception

        Returns:
            1 if succeeded else 0
    """

    try:
        import meraki  # import meraki api
    except Exception:
        log.error('Couldnt import meraki will skip running this api')
        return 0

    log.info('Connect to the Dashboard')
    dashboard = meraki.DashboardAPI(api_key)

    log.info(banner('Check the status of the device'))

    device_online = 0
    for i in range(timeout):
        if device_online:
            break
        response = dashboard.organizations.getOrganizationDevicesStatuses \
            (organization_id, total_pages='all')
        for dev in response:
            if dev['serial'] == serial:
                log.info('DEVICE Status: {}'.format(dev))
                if dev['status'] == 'online':
                    device_online = 1
        if i == (timeout - 1):
            log.error('Device is not Online within {} secs after '
                      'reload: ABORT'.format(timeout))
            return 0
        else:
            continue
    log.info('Device is Online, continue with Reload')
    log.info('Disconnect and Reconnect the device if there is a disconnect happens in previous runs.')
    device.disconnect()
    device.connect()
    log.info('Recording the time before the reload')
    T00 = device.parse('show clock')
    log.info('@@#@ T00 is {}'.format(T00))

    log.info(banner('Reloading the device'))
    device.execute('wr mem')
    if reload_type != 'api':  # Reload using the Dashboard API
        device.reload(timeout=timeout)
    else:
        # Reload the device using the API
        log.info('---------------------------------')
        log.info('Reload API Start time')
        api_start_time = time.time()
        log.info("--- %s seconds ---" % (time.time() - api_start_time))
        log.info('---------------------------------')

        response = dashboard.devices.rebootDevice(serial)
        log.info('Status of the Reload API: {}'.format(response))
        if response['success'] == True:
            log.info('Reboot request sent to device successfully')
        else:
            log.error('API did not send the Reboot Successfully: Abort')

        # Check the time taken for the device to go offline
        log.info('############################################################')
        log.info('Check the time taken for the device to go offline for reboot')
        log.info('############################################################')
        device_offline = 0
        for i in range(timeout):
            if device_offline:
                break
            response = dashboard.organizations.getOrganizationDevicesStatuses \
                (organization_id, total_pages='all')
            for dev in response:
                if dev['serial'] == serial:
                    log.info(time.time())
                    if dev['status'] == 'offline':
                        device_offline_time = time.time()
                        log.info('Device Status: {}'.format(dev))
                        log.info('---------------------------------')
                        log.info("--- %s seconds ---" % (time.time() - device_offline_time))
                        log.info('---------------------------------')
                        device_offline = 1
            if i == (timeout - 1):
                log.error('Device has not gone Offline within {} secs after '
                          'reload sent from dashboard: ABORT'.format(timeout))
                return 0
            else:
                continue

        log.info('Wait for the device to come back online after reload')
        log.info(banner('Check the time taken for the device to come Online after reboot'))
        device_online = 0
        for i in range(timeout):
            if device_online:
                break
            response = dashboard.organizations.getOrganizationDevicesStatuses \
                (organization_id, total_pages='all')
            for dev in response:
                if dev['serial'] == serial:
                    log.info('DEVICE Status: {}'.format(dev))
                    if dev['status'] == 'online':
                        device_online_time = time.time()
                        log.info('Device Status: {}'.format(dev))
                        log.info('---------------------------------')
                        log.info("--- %s seconds ---" % (time.time() - device_online_time))
                        log.info('---------------------------------')
                        device_online = 1
            if i == (timeout - 1):
                log.error('Device is not Online within {} secs after '
                          'reload: ABORT'.format(timeout))
                return 0
            else:
                continue

        log.info(banner('Check the time taken for the port to be connected after online'))
        port_online = 0
        for i in range(timeout):
            if port_online:
                break
            response = dashboard.switch.getDeviceSwitchPortsStatuses(serial)
            for dev in response:
                if dev['portId'] == '12':
                    log.info('Port Status: {}'.format(dev))
                    if dev['status'] == 'Connected':
                        port_connected_time = time.time()
                        log.info('Port Connected Time: {}'.format(dev))
                        log.info('---------------------------------')
                        log.info("--- %s seconds ---" % (time.time() - port_connected_time))
                        log.info('---------------------------------')
                        port_online = 1
            if i == (timeout - 1):
                log.error('Port is not Online within {} secs after '
                          'reload: ABORT'.format(timeout))
                return 0
            else:
                continue

    log.info(banner('Time to get the prompt after reboot'))

    prompt_time = time.time()
    try:
        device.disconnect()
        device.connect()
    except Exception:
        log.error('Not able to reconnect after reload')
        return 0
    T01 = device.parse('show clock')
    log.info('@@#@ T01 : Time to get prompt after reboot is {}'.format(T01))

    device.execute("terminal length 0")
    device.execute("terminal width 0")

    log.info('IOS bootup time')
    output = device.execute("show logg | in reboot")
    boot_time = re.search('.*:\s+Time taken to reboot after reload =\s+(\d+)\s+seconds$', output)
    boot_time_seconds = boot_time.group(1)
    log.info('@@#@ boot_time_seconds is {}'.format(boot_time_seconds))
    T0_sec = int(boot_time.group(1))
    log.info('@@#@ T0_sec is {}'.format(T0_sec))

    T0 = int(T0_sec / 60)
    log.info('@@#@ Initial boot time (power up to switch prompt) T0 is {}'.format(T0))

    log.info('---------------------------------')
    log.info("--- %s minutes ---" % T0)
    log.info('---------------------------------')

    log.info('Recording the time after the reload')
    T10_sec = _show_clock_seconds(device)
    log.info('@@#@ T10_sec is {}'.format(T10_sec))
    T10 = _convert_seconds_to_minutes(T10_sec)
    log.info('@@#@ T10 is {}'.format(T10))

    log.info('Disable Logging Console')
    device.configure('no logging console')

    log.info('Checking interface status')
    # checking interface state in a loop of 1500 sec
    timer = 0
    int_state = 0
    while int_state != 1 and timer <= intfuptimeout:
        output = device.execute("show ip interface brief {} | in down".format(intf_name))
        if not 'administratively' in output:
            log.info('@@#@ PASS: Interface %s is changed from admin down to down ' % intf_name)
            log.info('Time to bring-up interface')

            T11_sec = _show_clock_seconds(device)
            log.info('@@#@ T11_sec is {}'.format(T11_sec))
            T11 = _convert_seconds_to_minutes(T11_sec)
            log.info('@@#@ T11 is {}'.format(T11))

            break
        else:
            log.info('@@#@ Interface %s is not changed from admin down to down and retry' % intf_name)
            time.sleep(10)
            timer += 1

    output = device.execute("show ip interface brief {} | in down".format(intf_name))
    if not 'administratively' in output:
        log.info('@@#@ PASS: Interface %s is changed from admin down to down ' % intf_name)
    else:
        log.error("@@@@ FAIL: Interface %s is not changed from admin down to down after 1500sec" % intf_name)
        device.execute("show ip int br | i up")
        device.execute("show ip int br")

    log.info('Checking ping and Mtunnel status')

    device.transmit('app-hosting connect appid meraki session\r')
    device.receive('/ #', timeout=2)

    device.transmit('cat MERAKI_BUILD \r')
    device.receive('/ #', timeout=2)
    output = device.receive_buffer()
    log.info('@@#@ MERAKI BUILD is: %s' % output)
    device.transmit('cat /IOS_XE_BUILD \r')
    device.receive('/ #', timeout=2)
    output = device.receive_buffer()
    log.info('@@#@ IOS_XE_BUILD is: %s' % output)

    # checking ping status in a loop of 900 sec
    timer = 0
    ping_status = 0
    while ping_status != 1 and timer <= 90:
        device.transmit('ping -c 1 %s\r' % routable_ip)
        # device.receive('/ #',timeout = 20)
        device.receive(r'^.*packets received.*')
        output = device.receive_buffer()
        time.sleep(10)
        log.info('@@#@ Ping output is {}'.format(output))
        # import pdb;pdb.set_trace()

        if '1 packets received' in output:
            log.info('@@#@ Ping to %s passed' % routable_ip)
            device.transmit('dohost "show clock" > /storage/time\r')
            device.receive('/ #', timeout=2)
            device.transmit('more /storage/time\r')
            device.receive('/ #', timeout=2)
            T112 = device.receive_buffer()
            time.sleep(10)
            log.info('@@#@ Testing T112 is {}'.format(T112))

            break
        else:
            log.info('@@#@ Ping to %s failed and retry' % routable_ip)
            time.sleep(10)
            timer += 1

    device.transmit('ping -c 1 %s\r' % routable_ip)
    device.receive(r'^.*packets received.*')
    output = device.receive_buffer()
    time.sleep(10)
    log.info('@@#@ Ping output is {}'.format(output))

    if '1 packets received' in output:
        log.info('@@#@ Ping to %s passed' % routable_ip)
    else:
        log.error("@@@@ FAIL: Ping is failed after 15 minutes once the interface state is changed ")

    device.transmit('cat /tmp/connection_state\r')
    device.receive('/ #', timeout=2)
    output = device.receive_buffer()
    device.transmit('cat /click/ios/dump_pending_config_reqs\r')
    device.receive('/ #', timeout=5)
    output = device.receive_buffer()
    device.transmit('cat /click/uplinkstate/dhcp_state\r')
    device.receive('/ #', timeout=5)
    device.transmit('head -3 /click/uplinkstate/dhcp_state\r')
    device.receive('/ #', timeout=5)
    output = device.receive_buffer()
    device.transmit('cat /click/mtun/server1/state/debug_dump\r')
    device.receive('/ #', timeout=5)
    output = device.receive_buffer()
    device.transmit('cat /click/mtun/server2/state/debug_dump\r')
    device.receive('/ #', timeout=5)
    output = device.receive_buffer()
    device.transmit('cat /click/mtun/server3/state/debug_dump\r')
    device.receive('/ #', timeout=5)
    output = device.receive_buffer()

    device.transmit('exit\r')
    device.receive('#', timeout=2)
    device.transmit('\r')

    output = device.execute('more flash:/meraki/storage/time')
    match_value = re.search('[0-9]+:[0-9]+:[0-9]+(\.[0-9]+)*', output)
    current_time = match_value.group(0)
    log.info('@@#@ time is %s' % current_time)
    # return current_time
    tmp = current_time.split(':')
    current_time_in_sec = float(tmp[2]) + (float(tmp[1]) * 60) + (float(tmp[0]) * 60 * 60)
    T12_sec = int(current_time_in_sec)
    # return output

    log.info('@@#@ T12_sec is {}'.format(T12_sec))
    T12 = _convert_seconds_to_minutes(T12_sec)
    log.info('@@#@ T12 is {}'.format(T12))

    log.info('Collecting DMI and NDB Logs')

    device.execute('show logging process dmiauthd internal start last boot to-file flash:dmiauthd')
    device.execute('show logging process ndbmand internal start last boot to-file flash:ndbmand')

    log.info('Printing the performance numbers')
    log.info(banner('@@#@ T00 is {}'.format(T00)))
    log.info(banner('@@#@ T0 is {}'.format(T0)))
    log.info(banner('@@#@ T10 is {}'.format(T10)))
    log.info(banner('@@#@ T11 is {}'.format(T11)))
    log.info(banner('@@#@ T12 is {}'.format(T12)))

    T1_sec = T11_sec - T10_sec
    T2_sec = T12_sec - T11_sec
    T3_sec = T0_sec + T1_sec + T2_sec

    log.info('@@#@ Initial boot time (power up to switch prompt) T0 is {}'.format(T0))
    T1 = _convert_seconds_to_minutes(T1_sec)
    log.info('@@#@ Incremental time for Meraki app to configure all interfaces T1 is {}'.format(T1))

    T2 = _convert_seconds_to_minutes(T2_sec)
    log.info('@@#@ Incremental time for Ping Success and Mtunnel UP T2 is {}'.format(T2))

    T3 = _convert_seconds_to_minutes(T3_sec)
    log.info('@@#@ Total time T3 is {}'.format(T3))

    if reload_type == 'api':
        log.info(banner('Calculate the time taken at each step'))
        log.info('Reload API Start            : {}'.format(api_start_time))
        log.info('Device Offline              : {}'.format(device_offline_time))
        log.info('Device Online after reboot  : {}'.format(device_online_time))
        log.info('Device Port Connected Time  : {}'.format(port_connected_time))
        log.info('Device Prompt Time          : {}'.format(T0))

        reboot_req_time = (device_offline_time - api_start_time) / 60
        dev_online_time = (device_online_time - device_offline_time) / 60
        port_up_time = (device_online_time - port_connected_time) / 60
        total_time_from_reboot_req = (port_connected_time - api_start_time) / 60

        log.info(banner('RESULTS'))
        log.info('REBOOT REQ TIME TAKEN            : {}'.format(reboot_req_time))
        log.info('DEVICE ONLINE AFTER REBOOT       : {}'.format(dev_online_time))
        log.info('PORT CONNECTED TIME              : {}'.format(port_up_time))
        log.info('DEVICE PROMPT TIME               : {}'.format(T0))
        log.info('TOTAL TIME TAKEN                 : {}'.format(total_time_from_reboot_req))

    log.info('Reload Performed Successfully')
    return 1
