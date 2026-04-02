"""IOSXE CAT9K specific clean stages"""

# Python
import logging
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, wait as wait_futures, ALL_COMPLETED


from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.utils.timeout import Timeout

# Genie
from genie.libs.clean.stages.iosxe.stages import (
    ChangeBootVariable as IOSXEChangeBootVariable)
from genie.libs.clean.stages.iosxe.stages import (
    TftpBoot as IOSXETftpBoot)
from genie.libs.clean.stages.iosxe.stages import (
    InstallImage as IOSXEInstallImage)
from genie.libs.clean.stages.stages import VerifyRunningImage as GenericVerifyRunningImage
from genie.libs.clean.exception import StackMemberConfigException

# MetaParser
from genie.metaparser.util.schemaengine import Optional, Any, Or
from genie.libs.clean import BaseStage
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

from unicon.plugins.iosxe.stack.utils import StackUtils
from unicon.plugins.generic.statements import buffer_settled
from unicon.plugins.generic.service_statements import reload_statement_list
from unicon.plugins.iosxe.statements import boot_from_rommon_stmt

# Logger
log = logging.getLogger(__name__)

class ChangeBootVariable(IOSXEChangeBootVariable):
    """This stage configures boot variables of the device using the following steps:

    - Delete existing boot variables.
    - Configure boot variables using the provided 'images'.
    - Write memory.
    - Verify the boot variables are as expected.

Stage Schema
------------
change_boot_variable:

    images (list): Image files to use when configuring the boot variables.

    timeout (int, optional): Execute timeout in seconds. Defaults to 300.

    current_running_image (bool, optional): Set the boot variable to the currently
        running image from the show version command instead of the image provided.
        Defaults to False.

Example
-------
change_boot_variable:
    images:
        - harddisk:/image.bin
    timeout: 150
"""

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 300
    CURRENT_RUNNING_IMAGE = False

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('timeout'): int,
        Optional('current_running_image'): bool,

        # Deprecated
        Optional('check_interval'): int,
        Optional('max_time'): int,
        Optional('write_memory'): bool,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'configure_boot_variable',
        'write_memory',
        'verify_boot_variable'
    ]


class TftpBoot(IOSXETftpBoot):
    """This stage boots a new image onto your device using the tftp booting
method.

Stage Schema
------------
tftp_boot:

    image (list): Image to boot with

    ip_address (list): Management ip address to configure to reach to the
        tftp server

    subnet_mask (str): Management subnet mask

    gateway (str): Management gateway

    tftp_server (str): Tftp server that is reachable with management interface

    recovery_password (str): Enable password for device
        required after bootup. Defaults to None.

    recovery_username (str): Enable username for device
        required after bootup. Defaults to None.

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time during which tftp boot must
        complete. Defaults to 1000 seconds.

    image_length_limit(int, optional): Maximum length of characters for image.
        Defaults to 110.

Example
-------
tftp_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    ip_address: [10.1.7.126, 10.1.7.127]
    gateway: 10.1.7.1
    subnet_mask: 255.255.255.0
    tftp_server: 11.1.7.251
    recovery_password: nbv_12345
    recovery_username: user_123
    save_system_config: False
    timeout: 1000
    image_length_limit: 90

There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 1000
    IMAGE_LENGTH_LIMIT = 110


    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        'ip_address': list,
        'subnet_mask': str,
        'gateway': str,
        'tftp_server': str,
        'recovery_password': str,
        'recovery_username': str,
        Optional('recovery_en_pasword'): str,
        Optional('save_system_config'): bool,
        Optional('timeout'): int,
        Optional('image_length_limit'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'check_image_length',
        'delete_boot_variables',
        'write_memory',
        'enable_boot_manual',
        'go_to_rommon',
        'tftp_boot',
        'reconnect',
    ]

    def delete_boot_variables(self, steps, device, timeout=30):

        # Delete any previously configured boot variables
        with steps.start("Delete any previously configured boot variables on {}".\
                        format(device.name)) as step:
            try:
                device.configure('no boot system', timeout=timeout)
            except Exception as e:
                step.failed("Failed to delete the boot variables because of {}".format(e))

    def enable_boot_manual(self, steps, device):
        # To enable the boot manual
        with steps.start("Enabling the boot manual on {}".\
                        format(device.name)) as step:
            try:
                device.api.configure_boot_manual()
            except Exception as e:
                step.failed("Failed to enable the boot manual {}".format(e))


class VerifyApFabricSummary(BaseStage):
    """ This stage checks the fabric summary.

    Stage Schema
    ------------
    verify_ap_fabric_summary:

        ap_list(str):access point list

    Examples:
        verify_ap_fabric_summary:
            ap_list: ["AP188B.4500.44C8", "AP188B.4500.55C8"]

    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        'ap_list': list
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_ap_fabric_summary'
    ]

    def verify_ap_fabric_summary(self, device, steps, ap_list, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):

        for ap_name in ap_list:
            with steps.start("Checking ap state from show fabric summary for {}".format(device.name)) as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    # Fetch fabric ap state from get_fabric_ap_state
                    try:
                        fabric_ap_state_fetch = device.api.get_fabric_ap_state(ap_name)
                    except Exception as e:
                        step.failed('Unable to fetch  AP state from Fabric summary',from_exception=e)

                    # Verify if the given AP is registered
                    if fabric_ap_state_fetch.lower() == "Registered".lower():
                        step.passed("Sucess: The given Accesspoint {} is successfully Registered".format(ap_name))
                    else:
                        log.warning("Accesspoint has not yet registered. Re-Try Checking for Accesspoint State after {} secs".format(timeout))
                        timeout.sleep()
                else:
                    step.failed("Accesspoints failed to register to the controller")


class VerifyLispSessionEstablished(BaseStage):
    """ This stage validates LISP session establishment.

    Stage Schema
    ------------
    show_lisp_session_established:

        peer_ip(str) : peer ip


    Examples:
        show_lisp_session_established:
            peer_ip: "112.1.1.1"

    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============

    schema = {
        'peer_ip': str

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_lisp_session_established'
    ]

    def verify_lisp_session_established(self, device, steps, peer_ip, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):

        with steps.start("Validate LISP session ESTAB for {}".format(device.name)) as step:
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                # Fetch peer state from get_lisp_session_state
                try:
                    peer_state_fetch = device.api.get_lisp_session_state(peer_ip)
                except (AttributeError, SubCommandFailure) as e:
                    step.failed("Failed to fetch peer state",from_exception=e)

                # Verify if the given peer is registered
                if peer_state_fetch:
                    step.passed("Sucess: peer ip {} is in UP state in lisp session output".format(peer_ip))
                else:
                    log.warning("Re-Try Checking for LISP session ESTAB after {} secs".format(timeout))
                    timeout.sleep()
            else:
                step.failed("peer ip failed to register to the controller")

class VerifyAccessTunnelSummary(BaseStage):
    """ This stage checks the wireless process.

    Stage Schema
    ------------
    verify_access_tunnel_summary:

        ap_name(str): accesspoint name
        ap_ip(str): accesspoint IP
        rloc_ip(str): rloc IP

    Examples:
        verify_access_tunnel_summary:
            ap_name: "Ac0"
            ap_ip: "70.201.2.152"
            rloc_ip: "70.1.1.1"
    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        'ap_name': str,
        'ap_ip': str,
        'rloc_ip': str
    }
    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_access_tunnel_summary'
    ]

    def verify_access_tunnel_summary(self, device, steps, ap_name, ap_ip, rloc_ip, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):
        with steps.start("Checking AP IP and RLOC IP for {}".format(device.name)) as step:
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                try:
                    # Fetch AP IP  from get_ap_ip api
                    ap_ip_fetch = device.api.get_ap_ip(ap_name)
                except (AttributeError, SubCommandFailure) as e:
                    step.failed("Failed to find AP IP",from_exception=e)
                try:
                    # Fetch RLOC IP  from get_rloc_ip api
                    get_rloc_ip_fetch = device.api.get_rloc_ip(ap_name)
                except (AttributeError, SubCommandFailure) as e:
                    step.failed("Failed to find RLOC IP",from_exception=e)

                # Verify the AP IP for the given device
                if ap_ip_fetch == ap_ip:
                    step.passed("Destination IP has successfully registered with the device")
                else:
                    log.warning("Destination IP has not registered with the device")
                    timeout.sleep()

                # Verify the RLOC IP for the given device
                if get_rloc_ip_fetch == rloc_ip:
                    step.passed("Source IP has successfully registered with the device")
                else:
                    log.warning("Source IP has not registered with the device")
                    timeout.sleep()
            else:
                step.failed("ap ip and rloc ip are ailed to register")


class VerifyWirelessProcess(BaseStage):
    """ This stage checks the wireless process.

    Stage Schema
    ------------
    verify_wireless_process:

        check_processes(str): check process

    Examples:
        verify_wireless_process:
            check_processes : ['wncd','wncmgrd','nmspd','rrm','rogue','fman','dbm']

    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        'check_processes': list
    }
    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_wireless_process'
    ]

    def verify_wireless_process(self, device, steps, check_processes, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):
        for process in check_processes:
            with steps.start("Checking wireless process for {}".format(device.name)) as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    try:
                        no_of_matching_line_platform_fetch = device.api.get_matching_line_processes_platform(process)
                        if no_of_matching_line_platform_fetch >= 1:
                            processes_platform_dict = device.api.get_processes_platform_dict(process)
                            if processes_platform_dict:
                                no_of_matching_line_software_fetch = device.api.get_matching_line_platform_software(process)

                                if no_of_matching_line_software_fetch >= 1:
                                    platform_software_dict = device.api.get_platform_software_dict(process)
                                    if platform_software_dict:
                                        step.passed("Process {} is UP on standby member".format(process))
                                    else:
                                        log.warning('Process {} is Not UP in Standby Member. Going for re-check'.format(process))
                                        timeout.sleep()
                                else:
                                    log.warning('processes platform is not UP for Process {}'.format(process))
                                    timeout.sleep()
                            else:
                                log.warning('platform software process slot sw standby r0 monitor is not UP for Process {}'.format(process))
                                timeout.sleep()
                        else:
                            log.warning('processes platform {} is Not UP for process'.format(process))
                            timeout.sleep()
                    except Exception as e:
                        step.failed('Unable to check wireless process',from_exception=e)



class VerifyRunningImage(GenericVerifyRunningImage):
    """This stage verifies the current running image is the expected image.
The verification can be done by either MD5 hash comparison or by filename
comparison.

Stage Schema
------------
verify_running_image:

    images (list): Image(s) that should be running on the device. If not
        using verify_md5 then this should be the image path on the device.
        If using verify_md5 then this should be the original image location
        from the linux server.

    ignore_flash (bool, optional): Ignore flash directory names. Default True.

    verify_md5 (dict, optional): When this dictionary is defined, the image
            verification will by done by comparing the MD5 hashes of the
            running image against the expected image.

        hostname (str): Linux server that is used to generate the MD5
            hashes. This server must exist in the testbed servers block.

        timeout (int, optional): Maximum time in seconds allowed for the
            hashes to generate. Defaults to 60.

Example
-------
verify_running_image:
    images:
        - test_image.bin
"""
    IGNORE_FLASH = True
    VERIFY_MD5 = False

    def verify_running_image(self, steps, device, images, verify_md5=VERIFY_MD5, ignore_flash=IGNORE_FLASH):
        super().verify_running_image(steps, device, images, verify_md5=verify_md5, ignore_flash=ignore_flash)


class InstallImage(IOSXEInstallImage):
    """This stage installs a provided image onto the device using the install
CLI. It also handles the automatic reloading of your device after the
install is complete.

Stage Schema
------------
install_image:
    images (list): Image to install

    directory (str): directory where packages.conf is created
    save_system_config (bool, optional): Whether or not to save the system
        config if it was modified. Defaults to False.

    install_timeout (int, optional): Maximum time in seconds to wait for install
        process to finish. Defaults to 500.

    reload_timeout (int, optional): Maximum time in seconds to wait for reload
        process to finish. Defaults to 800.

    skip_boot_variable (bool, optional): 
    
    skip_save_running_config (bool, optional): Skip the step to save the the running
                                        configuration to the startup config.

    issu (bool, optional): set the issu for installing image.
        Defaults to False 

    verify_running_image (bool, optional): Compare the image filename with the running
        image version on device. If a match is found, the stage will be skipped.
        Defaults to True.
    
    stack_member_timeout(optional, int): maximum time to to wait for all the members of a stack device 
        to be ready. Default to 180 seconds

    stack_member_interval(optional, int): the interval to check if all the members of a stack device 
        are ready. Default to 30 seconds

    reload_service_args (optional):

        reload_creds (str, optional): The credential to use after the reload is
            complete. The credential name comes from the testbed yaml file.
            Defaults to the 'default' credential.

        prompt_recovery (bool, optional): Enable or disable the prompt recovery
            feature of unicon. Defaults to True.

        error_pattern (list, optional): List of regex strings to check for errors.
            Default: [r"FAILED:.*?$",]
        
        post_reload_wait(int, optional): the time after for before buffer to settle down.
            . Default to 30 seconds

        post_reload_timeout(int, optional): maximum time before accessing the device after
            reload. Default to 60 seconds.
            
        rommon_vars (dict, optional): Dictionary of rommon variables to set during
            the reload process. Default: {"DEBUG_CONF": ""}

        <Key>: <Value>
            Any other arguments that the Unicon reload service supports

Example
-------
install_image:
    images:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: True
    install_timeout: 1000
    reload_timeout: 1000

"""

    # =================
    # Argument Defaults
    # =================
    SAVE_SYSTEM_CONFIG = False
    INSTALL_TIMEOUT = 500
    RELOAD_TIMEOUT = 800
    RELOAD_SERVICE_ARGS = {
        'reload_creds': 'default',
        'prompt_recovery': True,
        'error_pattern': [r"FAILED:.*?$",],
        'post_reload_wait': 15,
        'post_reload_timeout': 60,
        "rommon_vars": {
            "DEBUG_CONF": ""
        }
    }
    ISSU = False
    SKIP_BOOT_VARIABLE = False
    SKIP_SAVE_RUNNING_CONFIG = False
    VERIFY_RUNNING_IMAGE = True
    STACK_MEMBER_TIMEOUT = 300
    STACK_MEMBER_INTERVAL = 30
    RELOAD_WAIT=30
    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('directory'): str,
        Optional('save_system_config'): bool,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
        Optional("reload_wait"): int,
        Optional('issu'): bool,
        Optional('skip_boot_variable'): bool,
        Optional('skip_save_running_config'): bool,
        Optional('verify_running_image', description="Compare the image filename with the running image version on device. If a match is found, the stage will be skipped", default=VERIFY_RUNNING_IMAGE): bool,
        Optional('stack_member_timeout'): int,
        Optional('stack_member_interval'): int,

        Optional('reload_service_args'): {
            Optional('reload_creds'): str,
            Optional('prompt_recovery'): bool,
            Optional('error_pattern'): list,
            Optional('post_reload_wait'): int,
            Optional('post_reload_timeout'):int,
            Optional('rommon_vars'): dict,
            Any(): Any()
        }
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'configure_no_boot_manual',
        'delete_boot_variable',
        'set_boot_variable',
        'unconfigure_and_verify_startup_config',
        'save_running_config',
        'verify_boot_variable',
        'check_start_up_config_variables',
        'verify_running_image',
        'install_image'
    ]


    def check_start_up_config_variables(self, steps, device):
        """ Check if debug config is set in rommon variables
        """
        with steps.start("Check for debug config in rommon variables") as step:
            cmd = 'show romvar' 
            try:
                output = device.parse(cmd)
                if debug_conf:=output.get('rommon_variables', {}).get('debug_conf'):
                    log.info(f"DEBUG_CONF {debug_conf} is set in rommon variables")
                    self.image_to_boot = "bootflash:packages.conf"
                else:
                    self.image_to_boot = None
                    log.info("DEBUG_CONF is not set in rommon variables")
            except Exception as e:
                step.failed("Failed to check for debug config in rommon variables",
                            from_exception=e)


class UnconfigureStackwiseVirtual(BaseStage):
    """This stage unconfigures StackWise Virtual on Cat9k devices and verifies
       the unconfiguration after device reload.

Stage Schema
------------
unconfigure_stackwise_virtual:
    wait_time (int, optional): Wait time in seconds before accessing device
        after svl unconfiguration. Defaults to 180.
    reload_time (int, optional): Reload time in seconds for device reload
        after svl unconfiguration. Defaults to 600.

Example
-------
unconfigure_stackwise_virtual:
    wait_time: 180
    reload_time: 600

"""
    # =================
    # Argument Defaults
    # =================
    WAIT_TIME = 180
    RELOAD_TIME = 600

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('wait_time',
                 description="Wait time in seconds before accessing device "
                             "after svl unconfiguration. Default to 180 seconds"):
        int,
        Optional('reload_time',
                 description="Reload time in seconds for device reload "
                             "after svl unconfiguration. Default to 600 seconds"):
        int,
    }

    exec_order = [
        'check_stackwise_virtual_config',
        'unconfigure_stackwise_virtual',
        'reload_device',
        'verify_stackwise_virtual_unconfig'
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
            subconns = list(device.subconnections)
            for subconn in subconns:
                try:
                    output = subconn.execute("show stackwise-virtual link")
                    device.parse(
                        "show stackwise-virtual link",
                        output=output
                    )
                    step.passed(
                        f"StackWise Virtual configuration exists on {device.name}. "
                        "Proceeding with unconfiguration."
                    )
                    return
                except SchemaEmptyParserError:
                    continue

            # If no member has StackWise Virtual configured, skip the unconfiguration
            self.skipped(
                f"StackWise Virtual is not configured on all members of {device.name}. "
                "Skipping unconfiguration."
            )

    def unconfigure_stackwise_virtual(self, device, steps):
        """Unconfigure StackWise Virtual on the device.
        Args:
            device (obj): Device object
            steps (obj): Steps object
        """
        with steps.start("Unconfiguring StackWise Virtual on the device") as step:
            switch_link_interfaces = {}
            # Identify active/standby consoles, put active first in the list since config
            # and save should run on active first before standby
            active = getattr(device, "active", None) or device
            standby = getattr(device, "standby", None)
            ordered_connections = [active] + ([standby] if standby else [])
            log.debug("Console order (active first): %s",
                     [getattr(c, "alias", device.name) for c in ordered_connections])
            # Gather SVL link information
            parsed = None
            for subconn in ordered_connections:
                try:
                    output = subconn.execute("show stackwise-virtual link")
                    parsed = device.parse("show stackwise-virtual link", output=output)
                    break
                except SchemaEmptyParserError:
                    continue
                except Exception as e:
                    step.failed("Failed to parse SVL link info",
                                from_exception=e)
            if not parsed:
                self.skipped("No SVL link information found on any connection")

            for switch_num, switch_data in parsed.get('switch', {}).items():
                switch_link_interfaces[switch_num] = {}
                for svl_id, svl_data in switch_data.get('svl', {}).items():
                    for port in svl_data.get('ports', {}).keys():
                        switch_link_interfaces[switch_num].setdefault(
                            svl_id, []).append(port)
            log.debug(f"SVL link interfaces to unconfigure per switch: "
                      f"{switch_link_interfaces}")
            NON_FATAL = [
                "Standby doesn't support",
                "Configuration allowed only from Active",
                "not allowed",
                "Incomplete command",
                "Invalid input",
            ]

            svl_dialog = Dialog([
                Statement(
                    pattern=r'.*Are you sure\?\s*\[yes\/no\].*',
                    action='sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
            ])

            # Dialog for copy running-config startup-config
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

            for subconn in ordered_connections:
                alias = getattr(subconn, "alias", device.name)
                for sw, links in switch_link_interfaces.items():
                    for lid, intfs in links.items():
                        for intf in intfs:
                            try:
                                subconn.configure([
                                    f"interface {intf}",
                                    f"no stackwise-virtual link {lid}",
                                    "shutdown", "exit",
                                ], timeout=120, reply=svl_dialog)
                                log.info("Unconfigured %s via %s", intf, alias)
                            except SubCommandFailure as e:
                                err_str = str(e)
                                if any(p in err_str for p in NON_FATAL):
                                    log.debug("Non-fatal on %s (%s): %s",
                                                alias, intf, err_str)
                                else:
                                    step.failed(
                                        f"Failed SVL removal on "
                                        f"{intf} via {alias}",
                                        from_exception=e)

                # Global SVL removal
                try:
                    subconn.configure("no stackwise-virtual",
                                     timeout=120, reply=svl_dialog)
                    log.info("Removed stackwise-virtual via %s", alias)
                except SubCommandFailure as e:
                    step.failed(
                        f"Failed removing SVL on {device.name}",
                        from_exception=e)

                # Save config using copy running-config startup-config
                try:
                    subconn.execute("copy running-config startup-config",reply=copy_run_to_start_dialog)
                except Exception as e:
                    log.warning("Could not save on %s: %s", alias, e)

            step.passed(
                f"StackWise Virtual unconfigured and saved on {device.name}. "
                "Reload required to take effect. Proceeding to reload the device."
            )


    def reload_device(self,
                       device,
                       steps,
                       wait_time=WAIT_TIME,
                       reload_time=RELOAD_TIME):
        """ Reload the device after SVL unconfiguration."""

        def _execute_reload(timeout=reload_time):
            subconns = list(device.subconnections)
            for subconn in subconns:
                ctx = getattr(subconn, 'context', {})
                if isinstance(ctx, dict) and 'image_to_boot' not in ctx:
                    ctx['image_to_boot'] = 'bootflash:packages.conf'

            # Reuse the standard single-RP cat9k reload dialog exactly:
            # reload_statement_list + boot_from_rommon_stmt
            reload_dialog = Dialog(reload_statement_list + [boot_from_rommon_stmt])

            for subconn in subconns:
                alias = getattr(subconn, 'alias', device.name)
                log.info(f"Sending reload on subconnection '{alias}'")
                try:
                    subconn.sendline('reload')
                except Exception as e:
                    log.warning(f"Could not send reload on '{alias}': {e}")

            def _process_reload_dialog(subconn):
                alias = getattr(subconn, 'alias', device.name)
                try:
                    reload_dialog.process(
                        subconn.spawn, timeout=timeout,
                        context=subconn.context)
                    log.info(f"Reload dialog completed on '{alias}'")
                except Exception as e:
                    step.failed(
                        f"Reload dialog ended on '{alias}'",
                        from_exception=e)

            with ThreadPoolExecutor(max_workers=len(subconns)) as executor:
                futures = [executor.submit(_process_reload_dialog, sc)
                           for sc in subconns]
                wait_futures(futures, timeout=timeout + 120,
                             return_when=ALL_COMPLETED)


        log.info(f'Get the recovery details from clean for device {device.name}')
        try:
            recovery_info = device.clean.get('device_recovery')
        except AttributeError:
            log.info(f'There is no recovery info for device {device.name}')
            recovery_info = {}

        if recovery_info:
            log.info(f"Recovery info found for device {device.name}")
            with steps.start("Power cycle device") as step:
                try:
                    device.api.execute_power_cycle_device()
                except Exception as e:
                    log.error(f"Power cycle failed: {e}")
                    with step.start(f"Connecting to device {device.name} after power cycle failure") as connect_attempt:
                        try:
                            device.connect()
                        except Exception as e:
                            log.exception(
                                f"Failed to connect to device {device.name}")
                            connect_attempt.failed(
                                f"Failed to connect to device "
                                f"{device.name} after power cycle",
                                from_exception=e)
                        connect_attempt.passed('Successfully connected to device.')
                    log.info("Attempting to reload device!")

                    with step.start(f"Attempting to reload device {device.name}") as reload_step:
                        try:
                            _execute_reload()
                        except Exception as e:
                            step.failed(
                                f"Failed to boot device {device.name} "
                                f"using reload",
                                from_exception=e)
                        else:
                            log.info(f"Waiting for {wait_time} seconds before reconnecting to the device.")
                            time.sleep(wait_time)
                            if not _disconnect_reconnect(device):
                                reload_step.failed(
                                    f"Failed to reconnect to device "
                                    f"{device.name} after reload")
                            reload_step.passed(
                                f"Device {device.name} reloaded successfully."
                            )
                            step.passx(f"Device {device.name}  successfully booted.")
                else:
                    device.api.device_recovery_boot()

                    log.info(f"Waiting for {wait_time} seconds before reconnecting to the device.")
                    time.sleep(wait_time)
                    # Reconnect to the device
                    try:
                        _disconnect_reconnect(device)
                    except Exception as e:
                        log.exception(f"Failed to reconnect to device {device.name}")
                        step.failed(
                            f"Failed to reconnect to device "
                            f"{device.name}",
                            from_exception=e)
                    step.passed(
                        f"Device {device.name} booted successfully.")
        else:
            log.info(f"No recovery info found for device {device.name}, proceeding with reload.")
            with steps.start(f"Reloading device {device.name}") as step:
                try:
                    _execute_reload()
                except Exception as e:
                    step.failed(
                        f"Failed to boot device {device.name} using reload",
                        from_exception=e)
                else:
                    log.info(f"Waiting for {wait_time} seconds before reconnecting to the device.")
                    time.sleep(wait_time)
                    if not _disconnect_reconnect(device):
                        step.failed(
                            f"Failed to reconnect to device "
                            f"{device.name} after reload")
                    step.passed(f"Device {device.name} reloaded and reconnected successfully.")

    def verify_stackwise_virtual_unconfig(self, device, steps):
        """ After reload, Verify StackWise Virtual unconfiguration on all device members."""
        with steps.start("Verifying StackWise Virtual unconfiguration") as step:
            subconns = list(device.subconnections)
            for subconn in subconns:
                try:
                    output = subconn.execute("show stackwise-virtual link")
                    device.parse("show stackwise-virtual link", output=output)
                    # If parse succeeds, SVL still exists
                    step.failed(
                        f"StackWise Virtual still configured on {device.name}. "
                        "Unconfiguration verification failed."
                    )
                except SchemaEmptyParserError:
                    # Expected empty parser output means SVL is not configured.
                    continue

            # If no member has StackWise Virtual configured, verification passed
            step.passed(
                f"StackWise Virtual unconfiguration verified on all members of {device.name}."
            )