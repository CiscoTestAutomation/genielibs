"""Utility type functions for Platform"""

# Python
import re
import time
import logging

# Genie
from genie.harness.utils import connect_device

# Unicon
from unicon import Connection
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import (
    SubCommandFailure,
    StateMachineError,
    TimeoutError,
    ConnectionError,
)
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def write_erase_reload_device_without_reconfig(
    device,
    via_console,
    reload_timeout,
    username=None,
    password=None,
    reload_creds=None,
    reload_hostname='Router',
    sleep_after_reload=15
):
    """Execute 'write erase' on device and reload without reconfiguring.

        Args:
            device(`obj`): Device object
            via_console(`str`): Via to use to reach the device console.
            reload_timeout(`int`): Maximum time to wait for reload to complete
            reload_creds(`str or list`): Creds to apply if reloading device asks
            sleep_after_reload (int, optional): Amount of time to sleep after reload.
                Defaults to 15 seconds.
    """


    # Set 'write erase' dialog
    wr_dialog = Dialog(
        [
            Statement(
                pattern=r"Erasing the nvram filesystem will "
                        r"remove all configuration files! "
                        r"Continue? \[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )

    # Execute 'write erase' command
    log.info("\n\nExecuting 'write erase' on device '{}'".format(device.name))
    try:
        device.execute("write erase", reply=wr_dialog)
    except Exception as e:
        raise Exception(
            "Error while executing 'write erase' on device '{}'".format(
                device.name
            )
        ) from e
    else:
        log.info(
            "Successfully executed 'write erase' command on device '{}'".format(
                device.name
            )
        )

    # Collect device base information before reload
    os = device.os
    hostname = device.name

    username, password =  device.api.get_username_password(
        device = device,
        username = username,
        password = password,
        creds = reload_creds)

    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])

    # Set 'reload' dialog
    r_dialog = Dialog(
        [
            Statement(
                pattern=r".*System configuration has been modified.*",
                action="sendline(no)",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*Do you want to proceed?\[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*Proceed with reload? *\[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*Would you like to enter the initial configuration.*",
                action="sendline(no)",
                loop_continue=True,
                continue_timer=False,
            ),
        ]
    )

    # Execute 'reload' command
    log.info("\n\nExecuting 'reload' on device '{}'".format(device.name))
    try:
        device.reload(
            prompt_recovery=True, dialog=r_dialog, reload_creds=reload_creds,
            timeout = reload_timeout)
        device.disconnect()
    except SubCommandFailure:
        # Disconnect and destroy the connection
        log.info(
            "Sucessfully executed 'reload' command on device {}".format(
                device.name
            )
        )
        log.info(
            "Disconnecting and destroying handle to device {}".format(
                device.name
            )
        )
        device.destroy()
    except Exception as e:
        raise Exception(
            "Error while reloading device '{}'".format(device.name)
        ) from e

    # Wait until reload has completed and device can be reachable
    log.info(
        "\n\nWaiting '{}' seconds for device to reboot after reload...".format(
            sleep_after_reload
        )
    )
    time.sleep(sleep_after_reload)

    # Reconnect to device
    log.info(
        "\n\nReconnecting to device '{}' after reload...".format(hostname)
    )

    try:
        device.connect()
    except (ConnectionError, TimeoutError) as e:
        # Connection or Timeout Error but 'no' has been sent
        # simply destroy handle at this point
        device.disconnect()
        log.info(
            "Reconnected to device '{}' after 'write erase' and reload'".format(
                hostname
            )
        )
    except Exception as e:
        raise Exception(
            "Error reconnecting to device '{}' after 'write erase'"
            " and reload".format(hostname)
        ) from e
    else:
        device.disconnect()
        log.info(
            "Successully reconnected to device '{}' after 'write erase' "
            "and reload'".format(hostname)
        )


def write_erase_reload_device(
    device,
    via_console,
    reload_timeout,
    static_route,
    static_route_netmask,
    static_route_nexthop,
    priv,
    vty_start,
    vty_end,
    mgmt_interface,
    mgmt_netmask,
    config_sleep,
    vrf,
    via_mgmt,
    post_reconnect_time,
    username=None,
    password=None,
    reload_creds=None,
    reload_hostname='Router',
):
    """Execute 'write erase' on device, reload and apply basic configuration.

        Args:
            device(`obj`): Device object
            via_console(`str`): Via to use to reach the device console.
            reload_timeout(`int`): Maximum time to wait for reload to complete
            reload_creds(`str or list`): Creds to apply if reloading device asks
            static_route_ip (`str`): IP address for static route configuration
            config_sleep (`int`): Time to wait after applying mgmt IP configuration
            vrf (`str`): VRF to use for management IP operations
            via_mgmt(`str`): Via to use to reach the device mgt IP.
            post_reconnect_time(`int`): Maximum time to wait after reload before configuring


        Returns:
            None
    """

    device.api.write_erase_reload_device_without_reconfig(
        device = device,
        via_console = via_console,
        reload_timeout = reload_timeout,
        username = username,
        password = password,
        reload_creds = reload_creds,
        reload_hostname = reload_hostname,
    )
    os = device.os
    hostname = device.name
    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])

    username, password =  device.api.get_username_password(
        device = device,
        username = username,
        password = password,
        creds = reload_creds)

    # Wait before reconnecting
    log.info(
        "\n\nWaiting '{}' seconds after reload ...".format(
            post_reconnect_time
        )
    )
    time.sleep(post_reconnect_time)

    # Configure hostname
    log.info("\n\nConfigure hostname on device '{}'".format(hostname))
    try:
        device.connect()
        device.configure("hostname {}".format(hostname))
        device.disconnect()
    except StateMachineError:
        device.disconnect()
        log.info(
            "Successfully configured hostname on device '{}'".format(hostname)
        )
    except Exception as e:
        raise Exception(
            "Error while trying to configure hostname on device '{}'".format(
                hostname
            )
        ) from e

    # Configure mgmt IP configuration
    mgmt_ip = str(device.connections[via_mgmt]["ip"])
    log.info(
        "\n\nConfigure mgmt IP configuration on device '{}'".format(hostname)
    )

    # Build config string
    cfg_str = (
        "ip route vrf {vrf} {static_route} {static_route_netmask} {static_route_nexthop}\n"
        "username {username} priv {priv} password {password}\n"
        "line vty {vty_start} {vty_end}\n"
        "login local\n"
        "interface {mgmt_interface}\n"
        " vrf forwarding {vrf}\n"
        " ip address {mgmt_ip} {mgmt_netmask}\n"
        " no shutdown\n"
        " negotiation auto".format(
            vrf=vrf,
            static_route=static_route,
            username=username,
            static_route_netmask=static_route_netmask,
            password=password,
            static_route_nexthop=static_route_nexthop,
            priv=priv,
            vty_start=vty_start,
            vty_end=vty_end,
            mgmt_ip=mgmt_ip,
            mgmt_netmask=mgmt_netmask,
            mgmt_interface=mgmt_interface,
        )
    )
    try:
        # Connect and configure
        device.connect()
        device.configure(cfg_str)
    except Exception as e:
        # Disconnect
        device.disconnect()
        log.error(e)
        raise Exception(
            "Unable to configure mgmt IP configuration on '{}'".format(
                hostname
            )
        ) from e
    else:
        device.disconnect()
        log.info(
            "Sucessfully configured mgmt IP configuration on '{}'".format(
                hostname
            )
        )

    # Waiting for configuration apply to take effect before reconnecting to device
    log.info(
        "\n\nWaiting for '{}' seconds for applied configuration to "
        "take effect...".format(config_sleep)
    )
    time.sleep(config_sleep)

    # Reconnect to device using vty
    log.info(
        "\n\nReconnect to device '{}' using management IP".format(hostname)
    )
    try:
        connect_device(device=device)
    except Exception as e:
        raise Exception(
            "'write erase' and 'reload' did not complete successfully"
        ) from e
    else:
        log.info(
            "Successfully erased all device configurations with "
            "'write erase' and 'reload' on device '{}'".format(hostname)
        )


def is_connected_via_vty(device, alias=None):
    ''' Check if we are connected via VTY
    '''
    if alias:
        conn = getattr(device, alias)
    else:
        conn = device
    show_users = conn.execute(r'show users | inc \*')
    if re.search(' vty', show_users):
        return True
    return False

def fp_switchover(device,timeout=420):
    """Perform FP switchover on device.
        Args:
            device(`obj`): Device object
            timeout ('int'): timeout in seconds for FP switchover
                            if not provided default is 420 seconds,
        Returns:
            True if FP switchover is success else False
        Raises:
            None
    """

    # Capture the parsed output of "show platform"
    output = device.parse("show platform", abstract=dict(revision=None))

    # Check if FP data is available in parsed output
    if 'F0' in output['slot'] and 'F1' in output['slot']:

        log.info("Dual FP exists... Checking if both FP are in OK state")

        # Fetch both FP type info from parsed output to fetch FP state
        fp0_type = list(output['slot']['F0']['other'].keys())[0]
        fp1_type = list(output['slot']['F1']['other'].keys())[0]

        # Fetch both FP state before FP switchover
        fp0_state_before_sso = output['slot']['F0']['other'][fp0_type]['state']
        fp1_state_before_sso = output['slot']['F1']['other'][fp1_type]['state']

        # check which is Active FP and Which is standby FP before swithcover
        if fp0_state_before_sso == "ok, active" and fp1_state_before_sso == "ok, standby":
            log.info("F0 is in Active state")
            log.info("F1 is in Standby state")
            log.info("Proceeding with FP Switchover")
        elif fp1_state_before_sso == "ok, active" and fp0_state_before_sso == "ok, standby":
            log.info("F0 is in Standby state")
            log.info("F1 is in Active state")
            log.info("Proceeding with FP Switchover")
        else:
            log.info("FP's are not in active and standby state... Cannot perform FP SSO")
            return False

        dialog = Dialog([
                 Statement(pattern=r'.*Proceed with switchover to standby FP? [confirm]',
                 action='sendline(\r)',
                 loop_continue=True,
                 continue_timer=False)])

        # execute write operation before FP Switchover
        device.execute("write")
        # Perform FP switchover
        device.execute("redundancy force-switchover fp", reply=dialog)

        # declare wait_time as 0 to capture the total wait time to compare it with given timeout
        wait_time = 0
        while wait_time < timeout:
            # Fetch both FP state during FP switchover
            try:
                output = device.parse("show platform", abstract=dict(revision=None))
            except SchemaEmptyParserError as e:
                log.error("Failed to parse 'show platform', Error: {}".format(str(e)))
                return False
            fp0_state_after_sso = output['slot']['F0']['other'][fp0_type]['state']
            fp1_state_after_sso = output['slot']['F1']['other'][fp1_type]['state']

            # check if FP states are swapped after FP switchover
            if fp0_state_after_sso == fp1_state_before_sso and fp1_state_after_sso == fp0_state_before_sso:
                log.info("FP switchover is Successful")
                return True
            else:
                log.info(f"FP0 State is {fp0_state_after_sso}")
                log.info(f"FP1 State is {fp1_state_after_sso}")
                log.info("Wait for 10 seconds... FP switchover is in progress...")
                time.sleep(10)
                wait_time += 10
        if wait_time >= timeout:
            log.info("Maximum wait time reached after Switchover.....")
            log.info(f"FP0 State is {fp0_state_after_sso}")
            log.info(f"FP1 State is {fp1_state_after_sso}")
            log.info("FP Switchover failed")
            return False
    else:
        log.info("No Dual FP present in the device...Cannot perform FP SSO")
        return True

def clear_logging_onboard_switch(device, switch_number):
    """ clears logging onboard switch
        Example: clear logging onboard switch 1

        Args:
            device ('obj'): Device object
            switch_number('int'): Switch number (Range: 1-16)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
        Statement(
            pattern=r'.*Clear logging onboard buffer\[y\/n\]',
            action='sendline(y)',
            loop_continue=False
        )
    ])
    config = f"clear logging onboard switch {switch_number}"
    try:
        device.execute(config, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear logging onboard switch {switch_number} on {device.name}. Error:\n{e}")

def upgrade_hw_programmable(device, programmable_type, file_system, package_name, slot):
    """ FPGA/CPLD upgrade
        Example: upgrade hw-programmable cpld filename bootflash:<pkg> R0

        Args:
            device ('obj'): Device object
            programmable_type ('str'): programmable type. Ex: cpld, fpga.
            file_system ('str'): file system type. Ex: bootflash:, harddisk:, usb0:
            package_name ('str'): programmable package name.
            slot ('str'): slot name. Ex: F0, R0, 0.

        Returns:
            CLI output

        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
        Statement(
            pattern=r'\d+\s+\(Y\)es\/\(N\)o\/\(C\)ontinue\? \[Y\]',
            action='sendline(y)',
            loop_continue=True
        ),
        Statement(
            pattern=r'power-cycled\.\s+\(Y\)es\/\(N\)o\/\(C\)ontinue\? \[Y\]',
            action='sendline(y)',
            loop_continue=False
        )
    ])
    cmd = f"upgrade hw-programmable {programmable_type} filename {file_system}{package_name} {slot}"
    try:
        cmd_output = device.execute(cmd, reply=dialog)
        return cmd_output
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute upgrade hw-programmable on {device.name}. Error:\n{e}")

def clear_controllers_ethernet_controller(device):
    """ clear controllers ethernet-controller
        Args:
            device ('obj'): device to execute on
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear controllers ethernet-controller {device}".format(device=device.name))
    try:
        device.execute("clear controllers ethernet-controller")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not clear controllers ethernet controller {device}. Error:\n{e}')

def erase_startup_config(device):
    """ erase startup_config
        Args:
            device ('obj'): device to execute on
        Return:
            None
        Raises:
            SubCommandFailure
    """
    # Set 'erase startup-config' dialog
    erase_dialog = Dialog(
        [
            Statement(
                pattern=r"Erasing the nvram filesystem will "
                        r"Continue? \[confirm\].*",
                action="sendline()",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    log.info(f"erase startup config on {device}")
    try:
        device.execute("erase startup-config", reply=erase_dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'could not erase startup config on  {device}. Error:\n{e}')

def clear_logging_onboard_rp_active_standby(device, rp_active_standby, log_name=None):
    """ clears logging onboard rp active/standby
        Example: clear logging onboard rp active/standby
        Args:
            device ('obj'): Device object
            rp_active_standby('str'): Rp active/standby
            log_name('str'): Log name. Ex: environment, temperature. Default is None.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
        Statement(
            pattern=r'.*Clear logging onboard buffer\[y\/n\]',
            action='sendline(y)',
            loop_continue=False
        )
    ])
    config = f"clear logging onboard rp {rp_active_standby} {log_name if log_name else ''}"
    try:
        device.execute(config, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear logging onboard rp {rp_active_standby} on {device.name}. Error:\n{e}"
        )
