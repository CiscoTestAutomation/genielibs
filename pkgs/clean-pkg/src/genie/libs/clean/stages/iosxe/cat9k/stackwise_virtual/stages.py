import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog
from unicon.plugins.iosxe.stack.utils import StackUtils
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.metaparser.util.schemaengine import Optional, Any
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.libs.clean import BaseStage
from genie.utils.timeout import Timeout

# Logger
log = logging.getLogger(__name__)


class ConfigureStackwiseVirtual(BaseStage):
    """This stage configures StackWise Virtual on Cat9k devices and verifies
the configuration after device reload.

Stage Schema
------------
configure_stackwise_virtual:

    wait_time (int, optional): Wait time in seconds before accessing device
        after svl configuration. Defaults to 60.

    reload_time (int, optional): Reload time in seconds for device reload
        after svl configuration. Defaults to 300.

    svl_link_interfaces (dict, optional): Dictionary of StackWise Virtual
        link interfaces. Keys are domain numbers, values are lists of
        interface names. Defaults to empty dict.

Example
-------
configure_stackwise_virtual:
    wait_time: 120
    reload_time: 400
    svl_link_interfaces:
        1:
          - TenGigabitEthernet1/0/1
          - TenGigabitEthernet1/0/2
"""
    # =================
    # Argument Defaults
    # =================
    # Argument Defaults
    WAIT_TIME = 180
    RELOAD_TIME = 300
    TIMEOUT_FOR_STANDBY_READY = 300
    INTERVAL_CHECK = 30
    SVL_LINK_INTERFACES = {}
    RELOAD_ERRORS_PATTERNS = []

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('wait_time',
                 description="Wait time in seconds before accessing device after svl configuration. Default to 60 seconds"):
        int,
        Optional('reload_time',
                 description="Reload time in seconds for device reload after svl configuration. Default to 300 seconds"):
        int,
        Optional('timeout_for_standby_ready',
                 description="Waiting time in seconds for standby RP to be ready after device reload. Default to 300 seconds"):
        int,
        Optional('interval_check',
                 description="Interval time in seconds to check standby RP status. Default to 30 seconds"):
        int,
        Optional('svl_link_interfaces',
                 description="Dictionary of StackWise Virtual link interfaces. Defaults to empty dict"):
        dict,
        Optional('reload_errors_patterns',
                 description="List of error patterns to check during reload. Defaults to empty list"):
        list,
    }

    exec_order = [
        'check_stackwise_virtual_config',
        'configure_stackwise_virtual',
        'boot_stack',
        'verify_stack_wise_virtual_config'
    ]

    def check_stackwise_virtual_config(self, steps, device):
        """ Check if StackWise Virtual configuration exists

            Args:
                steps (obj): Steps object
                device (obj): Device object
        """
        with steps.start(
                "Checking for existing StackWise Virtual configuration"
        ) as step:
            try:
                device.parse("show stackwise-virtual link")
            except SchemaEmptyParserError:
                step.passed(
                    f"No StackWise Virtual link on {device.name}. Continue with configuration."
                )

            self.skipped(
                f"StackWise Virtual configuration exists on {device.name}.")

    def configure_stackwise_virtual(self,
                                    device,
                                    steps,
                                    link_interfaces=SVL_LINK_INTERFACES):
        """ Configure StackWise Virtual on the device

            Args:
                device (obj): Device object
                steps (obj): Steps object
                link_interfaces (dict): Dictionary of StackWise Virtual link interfaces
        """
        with steps.start(
                "Configuring StackWise Virtual on the device") as step:
            if not link_interfaces:
                if hasattr(device, 'interfaces'):
                    for intf, intf_value in device.interfaces.items():
                        if hasattr(intf_value, 'stackwise_virtual_link'):
                            link_interfaces.setdefault(
                                intf_value.stackwise_virtual_link,
                                []).append(intf)
            if not link_interfaces:
                step.failed(
                    f"No StackWise Virtual link interfaces provided and device {device.name} has no interfaces."
                    )
            # Configure StackWise Virtual domain
            for subconnection in device.subconnections:
                try:
                    output = subconnection.execute('show stackwise-virtual')
                    parsed_output = device.parse('show stackwise-virtual',
                                                 output=output)
                except SchemaEmptyParserError as e:
                    log.info(
                        "No StackWise Virtual configuration found, proceeding with configuration."
                    )
                    parsed_output = {}
                #check for current domain on the device if they are the same as the one to be configured
                # use that domain instead of configuring a new one
                domain = parsed_output.get('domain', '')
                if str(domain) in link_interfaces:
                    log.info(
                        f"StackWise Virtual domain {domain} already configured on {subconnection.via}, skipping domain configuration."
                    )
                    continue
                # if not found a domain configured, configure from the provided link_interfaces
                else:
                    for link_number in link_interfaces:
                        try:
                            subconnection.configure(
                                ['stackwise-virtual', f'domain {link_number}'])
                        except SubCommandFailure as e:
                            log.exception(
                                f"Failed to configure StackWise Virtual domain {link_number} on {subconnection.via}")
                            steps.failed(
                                f"Failed to configure StackWise Virtual domain on {subconnection.via}: {e}")
                            
            # Unicon Dialogs for handling prompts during copy running-config startup-config we are not using the api because we 
            # want to handle each subconnection separately
            copy_run_to_start_dialog = Dialog([
                Statement(
                    pattern=r'^.*Destination +(filename|file +name)(\s\(control\-c +to +(cancel|abort)\)\:)? +\[(\S+\/)?startup\-config]\?\s*$',
                    action='sendline()',
                    loop_continue=True,
                    continue_timer=False),
                Statement(
                    pattern=r'.*proceed anyway\?.*$',
                    action='sendline(y)',
                    loop_continue=True,
                    continue_timer=False),
                Statement(
                    pattern=r'Continue\? \[no\]:\s*$',
                    action='sendline(y)',
                    loop_continue=True,
                    continue_timer=False),
            ])

            # configure stackwise virtual links
            for subconnection in device.subconnections:
                try:
                    # get the interfaces on the subconnection
                    subcon_interfaces = subconnection.execute(
                        "show ip interface brief")
                    parsed_subcon_interfaces = device.parse(
                        "show ip interface brief",
                        output=subcon_interfaces).get('interface', {}).keys()
                    # check and configure stackwise virtual links
                    for link_number, intf_names in link_interfaces.items():
                        for intf_name in intf_names:
                            if intf_name in parsed_subcon_interfaces:
                                stackwise_virtual_link_config = [
                                    f'interface {intf_name}',
                                    f'stackwise-virtual link {link_number}'
                                ]
                                subconnection.configure(stackwise_virtual_link_config)
                except SubCommandFailure as e:
                    log.exception(
                        f"Failed to configure StackWise Virtual link on {subconnection.via}")
                    steps.failed(
                        f"Failed to configure StackWise Virtual link on {subconnection.via}: {e}"
                    )
                # Save configuration
                subconnection.execute("copy running-config startup-config", reply=copy_run_to_start_dialog )

    def boot_stack(self,
                       device,
                       steps,
                       wait_time=WAIT_TIME,
                       reload_time=RELOAD_TIME,
                       timeout=TIMEOUT_FOR_STANDBY_READY,
                       interval=INTERVAL_CHECK,
                       error_pattern=RELOAD_ERRORS_PATTERNS):
        """ Boot the device

            Args:
                device (obj): Device object
                steps (obj): Steps object
                wait_time (int): Wait time in seconds before accessing device after boot, defaults to 180 seconds.
                reload_time (int): Reload time in seconds for device reload,defaults to 300 seconds.
                timeout (int): Timeout in seconds for standby RP to be ready, defaults to 300 seconds.
                interval (int): Interval in seconds to check standby RP status, defaults to 10 seconds.
                error_patterns (list): List of error patterns to check during reload, defaults to empty list.
        """
        utils = StackUtils()
        with steps.start("Power cycle device") as step:
            try:
                device.api.execute_power_cycle_device()
            except Exception as e:
                log.error(f"Power cycle failed: {e}")
                with step.start(f"Connecting to device {device.name} after power cycle failure") as connect_attempt:
                    try:
                        device.connect()
                    except Exception as e:
                        log.exception(f"Failed to connect to device {device.name}")
                        connect_attempt.failed(
                            f"Failed to connect to device {device.name} after power cycle: {e}"
                        )
                    connect_attempt.passed('Successfully connected to device.')
                log.info("Attempting to reload device!")
                with step.start(f"Attempting to reload device {device.name}") as reload_step:
                    device.connect()
                    for subconnection in device.subconnections:
                        subconnection.sendline('reload')
                    try:
                        device.reload(reload_command='', error_pattern=error_pattern, timeout=reload_time)
                    except Exception as e:
                        step.failed(
                            f"Failed to boot device {device.name} using reload: {e}"
                        )
                    else:
                        reload_step.passed(
                            f"Device {device.name} reloaded successfully."
                        )
                        step.passx(f"Device {device.name}  successfully booted.")
            else:
                device.api.device_recovery_boot()

            log.info(f"Waiting for {wait_time} seconds before reconnecting to the device.")
            time.sleep(wait_time)  # Wait for a while to allow the device to stabilize
            # Reconnect to the device
            try:
                _disconnect_reconnect(device)
            except Exception as e:
                log.exception(f"Failed to reconnect to device {device.name}")
                step.failed(
                    f"Failed to reconnect to device {device.name}: {e}")
            # check active and standby
            log.info('Wait for Standby RP to be ready.')
            if utils.is_active_standby_ready(device, timeout=timeout, interval=interval):
                step.passed(f"Device {device.name} booted successfully.")
            else:
                step.failed(f"Standby RP is not ready on device {device.name} after boot.")

    def verify_stack_wise_virtual_config(self, device, steps):
        """ Verify StackWise Virtual configuration on the device

            Args:
                device (obj): Device object
            Returns:
                None
        """
        with steps.start(
                "Verifying StackWise Virtual configuration on the device"
        ) as step:
            try:
                link_output = device.parse("show stackwise-virtual link")
            except SchemaEmptyParserError as e:
                step.failed(
                    f"Failed to verify StackWise Virtual configuration on {device.name}: {e}"
                )
            # make sure all svl links are up
            for switch , switch_info in link_output.get('switch', {}).items():
                for link_num, link_info in switch_info.get('svl', {}).items():
                    for intf, intf_info in link_info.get('ports', {}).items():
                        # check link status is UP and protocol status is READY
                        if intf_info.get('link_status') != 'U' or intf_info.get('protocol_status') != 'R':
                            step.failed(
                                f"StackWise Virtual link interface {intf} on switch {switch} with link number {link_num} is not up.")
                        log.info(f"StackWise Virtual link interface {intf} on switch {switch} with link number {link_num} is up.")
            step.passed(
                f"StackWise Virtual configuration verified on {device.name}.")
