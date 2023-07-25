"""IOSXE CAT9K specific clean stages"""

# Python
import logging
import time

from pyats.async_ import pcall

from genie.abstract import Lookup
from genie.libs import clean
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.utils.timeout import Timeout

# Genie
from genie.libs.clean.stages.iosxe.stages import (
    ChangeBootVariable as IOSXEChangeBootVariable)
from genie.libs.clean.stages.iosxe.stages import (
    TftpBoot as IOSXETftpBoot)
from genie.libs.clean.stages.stages import VerifyRunningImage as GenericVerifyRunningImage

# MetaParser
from genie.metaparser.util.schemaengine import Optional
from genie.libs.clean import BaseStage

from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

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


class RommonBoot(BaseStage):
    """This stage boots an image onto the device through rommon. Using either
a local image or one from a tftp server.

Stage Schema
------------
rommon_boot:

    image (list): Image to boot with

    tftp (optional): If specified boot via tftp otherwise boot using local
        image.

        ip_address (list, optional): Management ip address to configure to reach to the
            tftp server

        subnet_mask (str, optional): Management subnet mask

        gateway (str, optional): Management gateway

        tftp_server (str, optional): Tftp server that is reachable with management interface
    
    recovery_password (str): Enable password for device
        required after bootup. Defaults to None.

    recovery_enable_password (str): Enable password for device
        required after bootup. Defaults to None.

    recovery_username (str): Enable username for device
        required after bootup. Defaults to None.

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time allowed for the booting process.
        Defaults to 600.

    config_reg_timeout (int, optional): Max time to set config-register.
        Defaults to 30.

Example
-------
rommon_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    tftp:
        ip_address: [10.1.7.126, 10.1.7.127]
        gateway: 10.1.7.1
        subnet_mask: 255.255.255.0
        tftp_server: 11.1.7.251
    recovery_password: nbv_12345
    recovery_username: user_12345
    recovery_enable_password: en
    save_system_config: False
    timeout: 600
    config_reg_timeout: 10

There is more than one ip address, one for each supervisor.

To pass tftp information and tftp server ip from the testbed, refer the example below


testbed:
  name: 
  passwords: 
    tacacs: test
    enable: test
  servers:
    tftp:                       
        address: 10.x.x.x
        credentials:
            default:
                username: user
                password: 1234
devices:
    uut1:
        management:
            address:
                ipv4: '10.1.1.1/16'
            gateway:
                ipv4: '10.1.0.1'

"""

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_ENABLE_PASSWORD = None
    RECOVERY_USERNAME = None
    SAVE_SYSTEM_CONFIG = True
    TIMEOUT = 600
    ETHER_PORT = 0

    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        Optional('tftp'): {
            Optional('ip_address'): list,
            Optional('subnet_mask'): str,
            Optional('gateway'): str,
            Optional('tftp_server'): str
        },
        Optional('save_system_config'): bool,
        Optional('recovery_password'): str,
        Optional('recovery_username'): str,
        Optional('recovery_enable_password'): str,
        Optional('timeout'): int,
        Optional('ether_port'): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variables',
        'write_memory',
        'go_to_rommon',
        'rommon_boot',
        'reconnect',
    ]

    def delete_boot_variables(self, steps, device):
        with steps.start("Delete configured boot variables") as step:
            try:
                device.configure('no boot system')
            except Exception as e:
                step.failed("Failed to delete configured boot variables", from_exception=e)

    def write_memory(self, steps, device):
        with steps.start("Write memory") as step:

            try:
                device.api.execute_write_memory()
            except Exception as e:
                step.failed("Failed to write memory", from_exception=e)

    def go_to_rommon(self, steps, device, save_system_config=SAVE_SYSTEM_CONFIG):
        with steps.start("Bring device down to rommon mode"):

            reload_dialog = Dialog([
                Statement(pattern=r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                          action='sendline(yes)' if save_system_config else 'sendline(no)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*Proceed with reload\? \[confirm\].*",
                          action='sendline()',
                          loop_continue=False,
                          continue_timer=False),
            ])

            # Using sendline, as we dont want unicon boot to kick in and send "boot"
            # to the device. Cannot use device.reload() directly as in case of HA,
            # we need both sup to do the commands
            device.sendline('reload')
            reload_dialog.process(device.spawn)

            if device.is_ha:
                def reload_check(device, target):
                    device.expect(['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'],
                                  target=target, timeout=90)

                # check if device is a stack device(stack with 2 members is similar to HA devices)
                if len(device.subconnections) > 2:
                    pcall(reload_check,
                          cargs=(device,),
                          iargs=[[alias] for alias in device.connections.defaults.connections])
                else:
                    pcall(reload_check,
                          ckwargs={'device': device},
                          ikwargs=[{'target': 'active'},
                                   {'target': 'standby'}])
            else:
                device.expect(['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'], timeout=60)

            log.info("Device is reloading")
            device.destroy_all()

    def rommon_boot(self, steps, device, image, tftp=None, timeout=TIMEOUT, recovery_password=RECOVERY_PASSWORD,
                  recovery_username=RECOVERY_USERNAME, recovery_enable_password=RECOVERY_ENABLE_PASSWORD, ether_port=ETHER_PORT):

        with steps.start("Boot device from rommon") as step:
            if not tftp:
                tftp = {}
            
            # Check if management attribute in device object, if not set to empty dict
            if not hasattr(device, 'management'):
                setattr(device, "management", {})
            
            try:
                # Getting the tftp information, if the info not provided by user, it takes from testbed
                tftp.setdefault("ip_address", [str(device.management.get('address', '').get('ipv4', '').ip)])
                tftp.setdefault("subnet_mask", str(device.management.get('address', '').get('ipv4', '').netmask))
                tftp.setdefault("gateway", str(device.management.get('gateway').get('ipv4')))
                tftp.setdefault("tftp_server", device.testbed.servers.get('tftp', {}).get('address'))

                log.info("checking if all the tftp information is given by the user")
                if not all(tftp.values()):
                    log.warning(f"Some TFTP information is missing: {tftp}")
            except Exception as e:
                log.warning(f"Tftp information is missing. Please provide it either from testbed or clean stage {tftp}.")
                
            # Need to instantiate to get the device.start
            # The device.start only works because of a|b
            device.instantiate(connection_timeout=timeout)

            try:
                abstract = Lookup.from_device(device, packages={'clean': clean})
            except Exception as e:
                step.failed("Abstraction lookup failed", from_exception=e)

            # device.start only gets filled with single rp devices
            # for multiple rp devices we need to use subconnections
            if device.is_ha and hasattr(device, 'subconnections'):
                start = [i.start[0] for i in device.subconnections]
            else:
                start = device.start

            common_kwargs = {
                'device': device,
                'timeout': timeout
            }

            if tftp:
                tftp.update({'image': image, 'ether_port': ether_port})
                common_kwargs.update({'tftp_boot': tftp})
            else:
                common_kwargs.update({'golden_image': image})

            # Update recovery username and password
            common_kwargs.update({
                 'recovery_username': recovery_username,
                 'recovery_en_password':recovery_enable_password,
                 'recovery_password': recovery_password
            })

            try:
                pcall(
                    targets=abstract.clean.recovery.recovery.recovery_worker,
                    start=start,
                    ikwargs=[{'item': i} for i, _ in enumerate(start)],
                    ckwargs=common_kwargs
                )
            except Exception as e:
                step.failed("Failed to boot the device from rommon", from_exception=e)

    def reconnect(self, steps, device):
        with steps.start("Reconnect to device") as step:

            if hasattr(device, 'chassis_type') and device.chassis_type.lower() == 'stack':
                log.info("Sleep for 90 seconds in order to sync")
                time.sleep(90)

            if not _disconnect_reconnect(device):
                step.failed("Failed to reconnect")


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
