# Python
import os
import logging

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# pyATS
from pyats.utils.objects import R, find

# PLATFORM
from genie.libs.sdk.apis.iosxe.platform.get import get_diffs_platform

# Logger
log = logging.getLogger(__name__)

def is_platform_slot_in_state(device, slot, state="ok, active", max_time=1200,
    interval=120):
    """ Verify if slot is in state

        Args:
            device ('obj'): Device object
            slot ('str'): Slot number
            state ('str'): State being checked
            max_time ('int'): Max time checking
            interval ('int'): Interval checking
        Return:
            True
            False
        Raises:
            None
    """
    log.info("Verifying state of slot {slot}".format(slot=slot))
    timeout = Timeout(max_time=max_time, interval=interval)

    rs = R(["slot", slot, "rp", "(?P<val2>.*)", "state", state])

    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            log.info(
                "Slot {slot} reached state '{state}'".format(
                    slot=slot, state=state
                )
            )
            return True

        timeout.sleep()

    return False


def verify_changes_platform(device, platform_before, platform_after,
    max_time=1200, interval=120):
    """ Verify if there are changes between outputs from 'show platform'
        Args:
            device ('obj'): Device object
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
            max_time ('int'): Max time in seconds retrying
            interval ('int'): Interval of each retry
        Return:
            True
            False
        Raises:
            None
    """

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        if get_diffs_platform(
            platform_before=platform_before, platform_after=platform_after
        ):
            return True
        else:
            try:
                platform_after = device.parse("show platform")
            except SchemaEmptyParserError:
                pass

        timeout.sleep()

    return False

def verify_file_exists(device, file, size=None, dir_output=None):
    '''Verify that the given file exist on device with the same name and size
        Args:
            device ('obj'): Device object
            file ('str'): File path on the device, i.e. bootflash:/path/to/file
            size('int'): Expected file size (Optional)
            dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        Returns:
            Boolean value of whether file exists or not
    '''
    filename = os.path.basename(file)
    directory = ''.join([os.path.dirname(file), '/'])

    # 'dir' output
    try:
        dir_out = device.parse('dir {}'.format(directory), output=dir_output)
    except SchemaEmptyParserError:
        log.info(
            "Folder '{}' does not exist on {}"
            .format(directory, device.name))
        return False

    device_dir = dir_out.get('dir', {}).get('dir')

    # Check device directory
    if not device_dir:
        log.warning(
            "Device directory does not exists on {}".format(device.name)
        )
        return False

    # Check if file exists
    exist = filename in dir_out.get('dir').get(device_dir, {}).get('files', {})

    if not exist:
        log.info("File '{}' does not exist on {}".format(file, device.name))
        return exist
    elif not size:
        # Size not provided, just check if file exists
        log.info("File name '{}' exists on {}".format(file, device.name))
        return exist

    # Get filesize from output
    file_size = device.api.get_file_size(file=file, output=dir_output)

    # Check expected vs actual size
    log.info("Expected size: {} bytes, Actual size : {} bytes".format(
             size if size > -1 else 'Unknown',
             file_size if file_size > -1 else 'Unknown'))

    # Check file sizes match
    if size > -1 and file_size > -1:
        return size == file_size
    else:
        log.warning("File '{}' exists, but could not verify the file size".\
                    format(file))
        return True


def verify_boot_variable(device, boot_images, output=None):
    ''' Verifies given boot_images are set to the next-reload BOOT vars
        Args:
            device ('obj'): Device object
            boot_images ('str'): System images
    '''

    if boot_images == device.api.get_boot_variables(boot_var='next', output=output):
        log.info("Given boot images '{}' are set to 'BOOT' variable".\
                 format(boot_images))
        return True
    else:
        log.info("Given boot images '{}' are not set to 'BOOT' variable".\
                 format(boot_images))
        return False

def verify_config_register(device, config_register, next_reload=False,
    output=None):
    ''' Check current config register value
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value of config register
    '''

    # Get config-register
    value = device.api.get_config_register(next_reload=next_reload, output=output)
    if config_register == value:
        log.info("Configuration register has been correctly set to '{}'".\
                 format(config_register))
        return True
    else:
        log.error("Configuration register value '{}' is incorrect".\
                  format(value))
        return False

def verify_module_status(device, timeout=180, interval=30, ignore_modules=None):
    ''' Check status of slot using 'show platform'
        Args:
            device ('obj'): Device object
            timeout ('int'): Max timeout to re-check slot status
            interval ('int'): Max interval to re-check slot status
            ignore_modules ('list'): Modules to ignore status check
    '''

    timeout = Timeout(max_time=timeout, interval=interval)
    while timeout.iterate():
        # Reset
        failed_slots = []
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Check state for all slots
        failed_slots = Dq(output).contains('state').\
                            not_contains_key_value('state', 'empty').\
                            not_contains_key_value('state',
                                                   '.*ok.*|standby|ha-standby|Ready',
                                                   value_regex=True).\
                            get_values('slot')

        # To ignore specified modules
        if ignore_modules:
            for module in ignore_modules:
                if module in failed_slots:
                    failed_slots.remove(module)
            log.info("Ignoring the following modules '{}'".\
                     format(ignore_modules))

        if not failed_slots:
            log.info("All modules on '{}' are in stable state".\
                     format(device.name))
            break
        else:
            log.warning("The following modules are not in stable state {}".\
                        format(failed_slots))
            log.warning("Sleeping {} seconds before rechecking".format(interval))
            timeout.sleep()
            continue
    else:
        raise Exception("Modules on '{}' are not in stable state".\
                        format(device.name))

def verify_mpls_rlist_summary_before_and_after_sso(device,
                                                   active_rlist_summary_bsso,
                                                   standby_rlist_summary_bsso,
                                                   current_lspvif_adj_label_count=False):
    ''' Verify whether rlist summary is same before and after sso on both active and standby device
        Args:
            device ('obj'): Device object
            active_rlist_summary_bsso ('int'): active device rlist summary result before sso
            standby_rlist_summary_bsso ('int'): standby device rlist summary result before sso
            current_lspvif_adj_label_count ('bool'): True if current lspvif adjaceny label count needs to be verified
                                                     False if current lspvif adjaceny label count need not be verified
        Return:
            True if rlist summary are same on active and standby device before and after sso
            or else returns False
    '''

    # current count Rlist
    active_rlist_bsso = active_rlist_summary_bsso.q.contains(
        "current_count").get_values("rlist")[0]
    standby_rlist_bsso = standby_rlist_summary_bsso.q.contains(
        "current_count").get_values("rlist")[0]

    # current count Rentry
    active_rentry_bsso = active_rlist_summary_bsso.q.contains(
        "current_count").get_values("rentry")[0]
    standby_rentry_bsso = standby_rlist_summary_bsso.q.contains(
        "current_count").get_values("rentry")[0]
        
    try:
        active_rlist_summary_asso = device.parse(
            "show platform software fed switch active mpls rlist summary")
        standby_rlist_summary_asso = device.parse(
            "show platform software fed switch standby mpls rlist summary")
    except SchemaEmptyParserError:
        raise SchemaEmptyParserError(
            "Failed to parse commands"
        )

    active_rlist_asso = active_rlist_summary_asso.q.contains(
        "current_count").get_values("rlist")[0]
    standby_rlist_asso = standby_rlist_summary_asso.q.contains(
        "current_count").get_values("rlist")[0]
    active_rentry_asso = active_rlist_summary_asso.q.contains(
        "current_count").get_values("rentry")[0]
    standby_rentry_asso = standby_rlist_summary_asso.q.contains(
        "current_count").get_values("rentry")[0]

    # verify rlist
    if not ((active_rlist_bsso == active_rlist_asso) and (
            active_rentry_bsso == active_rentry_asso)):
        log.debug("Current count rlist and rentry verification failed after sso")
        return False
        
    # verify rentry
    if not ((standby_rlist_bsso == standby_rlist_asso) and (
            standby_rentry_bsso == standby_rentry_asso)):
        log.debug("Current count rlist and rentry verification failed after sso")
        return False

    # Maximum reached Rlist
    active_rlist_bsso = active_rlist_summary_bsso.q.contains(
        "maximum_reached").get_values("rlist")[0]
    active_rlist_asso = active_rlist_summary_asso.q.contains(
        "maximum_reached").get_values("rlist")[0]
    standby_rlist_bsso = standby_rlist_summary_bsso.q.contains(
        "maximum_reached").get_values("rlist")[0]
    standby_rlist_asso = standby_rlist_summary_asso.q.contains(
        "maximum_reached").get_values("rlist")[0]
        
    # Maximum reached Rentry
    active_rentry_bsso = active_rlist_summary_bsso.q.contains(
        "maximum_reached").get_values("rentry")[0]
    active_rentry_asso = active_rlist_summary_asso.q.contains(
        "maximum_reached").get_values("rentry")[0]
    standby_rentry_bsso = standby_rlist_summary_bsso.q.contains(
        "maximum_reached").get_values("rentry")[0]
    standby_rentry_asso = standby_rlist_summary_asso.q.contains(
        "maximum_reached").get_values("rentry")[0]

    if not ((active_rlist_bsso <= active_rlist_asso *
         2 and active_rlist_bsso >= active_rlist_asso) and (
            active_rentry_bsso <= active_rentry_asso *
            2 and active_rentry_asso >= active_rentry_bsso)):
        log.debug("Maximum Reached entry verification failed on active switch")
        return False

    if not ((standby_rlist_bsso <= standby_rlist_asso *
         2 and standby_rlist_bsso >= standby_rlist_asso) and (
            standby_rentry_bsso <= standby_rentry_asso *
            2 and standby_rentry_asso >= standby_rentry_bsso)):
        log.debug("Maximum Reached entry verification failed on standby switch")
        return False

    if current_lspvif_adj_label_count:
        # Currrent lspvif adj label count
        active_adj_bsso = active_rlist_summary_bsso.q.get_values(
            "current_lspvif_adj_label_count")[0]
        active_adj_asso = active_rlist_summary_asso.q.get_values(
            "current_lspvif_adj_label_count")[0]
        if not active_adj_bsso == active_adj_asso:
            log.debug(
                "current_lspvif_adj_label_count verification failed on active switch")
            return False
        
        standby_adj_bsso = standby_rlist_summary_bsso.q.get_values(
            "current_lspvif_adj_label_count")[0]
        standby_adj_asso = standby_rlist_summary_asso.q.get_values(
            "current_lspvif_adj_label_count")[0]
        if not standby_adj_bsso == standby_adj_asso:
            log.debug(
                "current_lspvif_adj_label_count verification failed on standby switch")
            return False
    return True

def verify_platform_model_number(device, pid, output=None):
    ''' Verify given pid are as expected model number or chassis type
        Args:
            device ('obj'): Device object
            pid ('str'): Product Identifcation Number(PID)  or model number or chassis type
    '''

    if pid == device.api.get_platform_model_number():
        log.info("Given pid '{}' is as expected platform 'model number' or 'chassis type'".\
                 format(pid))
        return True
    else:
        log.info("Given pid '{}' is not as expected platform 'model number' or 'chassis type'".\
                 format(pid))
        return False

def verify_platform_details(device,      
                            expected_hw_ver=None,
                            expected_mac_address=None,
                            expected_model_name=None,
                            expected_ports= None,
                            expected_slot = None,
                            expected_sn= None,
                            expected_sw_ver= None,
                            max_time=15,
                            check_interval=5):
    """Verify  verify platform details in device
        Args:
            device (`obj`): Device object
            expected_hw_ver ('str'): Expected hardware version. Default to None if no inputs
            expected_mac_address ('str'): Expected mac_address. Default to None if no inputs
            expected_model_name ('str'): Expected model name. Default to None if no inputs
            expected_ports ('str'): Expected ports. Default to None if no inputs
            expected_slot ('str'): Expected slot. Default to None if no inputs
            expected_sn ('str'): Expected serial number . Default to None if no inputs
            expected_sw_ver ('str'): Expected software version. Default to None if no inputs
            max_time (`int`, Optional): Max time, default: 15 seconds
            check_interval (`int`, Optional): Check interval, default: 5 seconds
        Returns:
            result ('bool'): Verified result
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show platform')
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        platform_details_result = True

        expected_platform_details ={
            'hw_ver': expected_hw_ver, 
            'mac_address': expected_mac_address,
            'name': expected_model_name, 
            'ports': expected_ports,
            'slot': expected_slot, 
            'sn': expected_sn,
            'sw_ver':expected_sw_ver
        }
        
        log.info("Verify if 'Expected platform_details' is Equal-to 'Actual platform_details' on device i.e {}".format(device.name))
        for platform_details, platform_details_value  in expected_platform_details.items():
            if platform_details_value:
                actual_platform_details = out.q.contains('rp').get_values(platform_details, 0)

                log.info(f"*Expected '{platform_details} is': {platform_details_value} , Actual '{platform_details} is': {actual_platform_details}")
                if (platform_details_value) and (actual_platform_details) != platform_details_value:
                    log.error(f"Expected '{platform_details} ' is NOT-EQUAL to '{platform_details}' present in device '{device.name}'")
                    platform_details_result = False
                else:
                    log.info(f"Expected '{platform_details}' is EQUAL-TO '{platform_details}' present in device '{device.name}'")
        
        if platform_details_result:
            return True

        timeout.sleep()

    return False

def verify_number_of_interfaces(device,     
                            expected_fast_ethernet=None,
                            expected_gigabit_ethernet=None,
                            expected_two_gigabit_ethernet=None,
                            expected_five_gigabit_ethernet = None,
                            expected_ten_gigabit_ethernet= None,
                            expected_virtual_ethernet= None,
                            max_time=15,
                            check_interval=5):
    """ Verify  verify number of interfaces in device
        Args:
            device (`obj`): Device object
            expected_fast_ethernet ('str'): Expected fast ethernet interfaces. 
            Default to None if no inputs
            expected_gigabit_ethernet ('str'): Expected gigabit ethernet interfaces.
            Default to None if no inputs
            expected_two_gigabit_ethernet ('str'): Expected 2.5 gigabit ethernet interfaces. 
            Default to None if no inputs
            expected_five_gigabit_ethernet ('str'): Expected five gigabit ethernet interfaces. 
            Default to None if no inputs
            expected_ten_gigabit_ethernet ('str'): Expected ten gigabit ethernet interfaces. 
            Default to None if no inputs
            expected_virtual_ethernet ('str'): Expected virtual gigabit ethernet interfaces. 
            Default to None if no inputs
            max_time ('int', Optional): Max time, default: 15 seconds
            check_interval ('int', Optional): Check interval, default: 5 seconds
        Returns:
            result ('bool'): Verified result
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show version')
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        number_of_intfs_result = True

        expected_ethernet_interfaces ={
            'FastEthernet': expected_fast_ethernet, 
            'Gigabit Ethernet': expected_gigabit_ethernet,
            '2.5 Gigabit Ethernet': expected_two_gigabit_ethernet, 
            'Five Gigabit Ethernet': expected_five_gigabit_ethernet,
            'Ten Gigabit Ethernet': expected_ten_gigabit_ethernet, 
            'Virtual Ethernet': expected_virtual_ethernet
        }

        log.info("Verify if 'Expected number_of_interfaces' is Equal-to 'Actual number_of_interfaces' on  device i.e {}".format(device.name))
        for type_of_intfs, ethernet_interfaces  in expected_ethernet_interfaces.items():
            if ethernet_interfaces:
                number_of_intfs = out.q.contains('version').contains('number_of_intfs').get_values(type_of_intfs, 0)

                log.info(f"*Expected '{type_of_intfs} interfaces': {ethernet_interfaces} , Actual '{type_of_intfs} interfaces': {number_of_intfs}")
                if (ethernet_interfaces) and (number_of_intfs) != ethernet_interfaces:
                    log.error(f"Expected '{type_of_intfs} interfaces' is NOT-EQUAL to '{type_of_intfs} interfaces' present in device '{device.name}'")
                    number_of_intfs_result = False
                else:
                    log.info(f"Expected '{type_of_intfs} interfaces' is EQUAL-TO '{type_of_intfs} interfaces' present in device '{device.name}'")

        if number_of_intfs_result:
            return True
        timeout.sleep()

    return False
