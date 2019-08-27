"""Utility type functions for Platform"""

# Python
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

# Logger
log = logging.getLogger(__name__)


def write_erase_reload_device(
    device,
    via_console,
    via_mgmt,
    vrf,
    reload_timeout,
    static_route,
    static_route_netmask,
    priv,
    static_route_nexthop,
    vty_start,
    vty_end,
    mgmt_interface,
    mgmt_netmask,
    config_sleep,
    post_reconnect_time,
):
    """Execute 'write erase' on device

        Args:
            device(`obj`): Device object
            reload_timeout(`int`): Maximum time to wait for reload to complete
            static_route_ip (`str`): IP address for static route configuration
            config_sleep (`int`): Time to wait after applying mgmt IP configuration

        Returns:
            None
    """

    # Set 'write erase' dialog
    wr_dialog = Dialog(
        [
            Statement(
                pattern=r"Erasing the nvram filesystem will "
                "remove all configuration files! "
                "Continue? \[confirm\].*",
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
        )
    else:
        log.info(
            "Successfully executed 'write erase' command on device '{}'".format(
                device.name
            )
        )

    # Collect device base information before reload
    os = device.os
    hostname = device.name
    username = device.tacacs["username"]
    password = device.passwords["enable"]
    ip = str(device.connections[via_console]["ip"])
    port = str(device.connections[via_console]["port"])
    mgmt_ip = str(device.connections[via_mgmt]["ip"])

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
        device.reload(prompt_recovery=True, dialog=r_dialog)
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
    except:
        raise Exception(
            "Error while reloading device '{}'".format(device.name)
        )

    # Wait until reload has completed and device can be reachable
    log.info(
        "\n\nWaiting '{}' seconds for device to reboot after reload...".format(
            reload_timeout
        )
    )
    time.sleep(reload_timeout)

    # Reconnect to device
    log.info(
        "\n\nReconnecting to device '{}' after reload...".format(hostname)
    )
    new_device = Connection(
        username=username,
        password=password,
        os=os,
        hostname="Router",
        start=["telnet {ip} {port}".format(ip=ip, port=port)],
        prompt_recovery=True,
    )
    try:
        new_device.connect()
    except (ConnectionError, TimeoutError) as e:
        # Connection or Timeout Error but 'no' has been sent
        # simply destroy handle at this point
        new_device.disconnect()
        log.info(
            "Reconnected to device '{}' after 'write erase' and reload'".format(
                hostname
            )
        )
    except:
        raise Exception(
            "Error reconnecting to device '{}' after 'write erase'"
            " and reload".format(hostname)
        )
    else:
        new_device.disconnect()
        log.info(
            "Successully reconnected to device '{}' after 'write erase' "
            "and reload'".format(hostname)
        )

    # Wait before reconnecting to configure hostname
    log.info(
        "\n\nWaiting '{}' seconds before configuring hostname on device...".format(
            post_reconnect_time
        )
    )
    time.sleep(post_reconnect_time)

    # Configure hostname
    log.info("\n\nConfigure hostname on device '{}'".format(hostname))
    try:
        new_device.connect()
        new_device.configure("hostname {}".format(hostname))
    except StateMachineError:
        new_device.disconnect()
        log.info(
            "Successfully configured hostname on device '{}'".format(hostname)
        )
    except:
        raise Exception(
            "Error while trying to configure hostname on device '{}'".format(
                hostname
            )
        )

    # Configure mgmt IP configuration
    log.info(
        "\n\nConfigure mgmt IP configuration on device '{}'".format(hostname)
    )
    new_device2 = Connection(
        username=username,
        password=password,
        os=os,
        hostname="{}".format(hostname),
        prompt_recovery=True,
        start=["telnet {ip} {port}".format(ip=ip, port=port)],
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
        new_device2.connect()
        new_device2.configure(cfg_str)
    except Exception as e:
        # Disconnect
        new_device2.disconnect()
        log.error(e)
        raise Exception(
            "Unable to configure mgmt IP configuration on '{}'".format(
                hostname
            )
        )
    else:
        new_device2.disconnect()
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
    except:
        raise Exception(
            "'write erase' and 'reload' did not complete successfully"
        )
    else:
        log.info(
            "Successfully erased all device configurations with "
            "'write erase' and 'reload' on device '{}'".format(hostname)
        )
