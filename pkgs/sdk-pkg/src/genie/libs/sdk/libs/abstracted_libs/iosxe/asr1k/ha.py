'''HA useful function'''

# Python
import re
import time
import logging
from os.path import basename, getsize

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

# HA
from ..ha import HA as HA_iosxe

# Abstract
from genie.abstract import Lookup

# Genie
from genie.libs import parser
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.common import set_filetransfer_attributes

# ATS
from pyats.utils.objects import R, find
from pyats.utils.fileutils import FileUtils

# module logger
logger = logging.getLogger(__name__)


class HA(HA_iosxe):

    def _reloadLc(self, lc):
        """Do the reload LC action for asr1k devices.

        Args:
          Mandatory:
            lc (`str`) : LC slot number need to reload.

        Raises:
            Unicon errors

        Example:
            >>> _reloadLc(lc='R0')
        """
        # unicon
        dialog = Dialog([
            Statement(pattern=r'\(y\/n\)\?.*',
                                action='sendline(y)',
                                loop_continue=True,
                                continue_timer=False)
        ])
        # Execute command to reload LC
        self.device.execute('hw-module slot {} reload'.format(lc), reply=dialog)
        time.sleep(5)

    def _prepare_issu(self, steps, upgrade_image):
        """Prepare the device for ISSU:

            1. Check currect image version and upgrade image version
            2. Copy upgrade image to standby RP

        Raises:
            Unicon errors
            Exception

        Example:
            >>> _prepare_issu(steps=steps, upgrade_image='someimage')
        """

        # Init
        device = self.device
        filetransfer = FileUtils.from_device(device)

        if not hasattr(self.device, 'filetransfer_attributes'):
            filetransfer = FileUtils.from_device(self.device)
            set_filetransfer_attributes(self, self.device, filetransfer)

        for disk in ['harddisk:', 'stby-harddisk:']:

            # Check for space on RP and SRP
            logger.info("Verify '{}' has enough space".format(disk))
            try:
                self.check_disk_space(device=device, disk=disk,
                                      image=upgrade_image)
            except Exception as e:
                raise Exception("FAIL: Device '{}' does not have enough space -"
                                " skipping ISSU".format(disk))

            # Copy ISSU upgrade image to disk
            logger.info("Copy ISSU upgrade image to {}".format(disk))
            from_url = '{protocol}://{address}/{upgrade_image}'.format(
                        protocol=device.filetransfer_attributes['protocol'],
                        address=device.filetransfer_attributes['server_address'],
                        upgrade_image=upgrade_image)
            filetransfer.copyfile(source=from_url, destination=disk,
                                  device=device, timeout_seconds='600')

            # Verify location:<filename> exists
            output = device.execute('dir {disk}{image}'.format(disk=disk,
                                    image=basename(upgrade_image)))
            if 'Error' not in output:
                logger.info("Copied ISSU image to '{}'".format(disk))
            else:
                raise Exception("Unable to copy ISSU image to '{}'".format(disk))

    def _perform_issu(self, steps, upgrade_image, timeout=300):
        """Perform the ISSU steps in sequence on the ASR1K device:

            1.  Execute 'issu loadversion' to begin ISSU process
            2.  Poll until standby RP reaches 'ok' state
            3.  Verify ISSU state is now 'loadversion'
            4.  Execute 'issu runversion' to initiate RP failover
            5.  Reconnect to the device
            6.  Verify ISSU state is now 'runversion'
            7.  Execute 'issu acceptversion' to cancel rollback timer
            8.  Verify ISSU state is now 'acceptversion'
            9.  Verify ISSU rollback timer has been cancelled
            10. Poll until standby RP reaches 'ok' state
            11. Save running-configuration to startup-configuration
            12. Execute 'issu commitversion' to complete ISSU process
            13. Reload the device and then reconnect to it
            14. Verify device is now booted with ISSU upgrade image

        Raises:
            Unicon errors
            Exception

        Example:
            >>> _perform_issu(steps=steps, upgrade_image='someimage')
        """

        # Init
        device = self.device
        lookup = Lookup.from_device(device)
        filetransfer = FileUtils.from_device(device)
        image_name = basename(upgrade_image)

        # ======================================================================
        #                           Get standby RP
        # ======================================================================
        with steps.start("Get standby RP information", continue_=True) as step:
            platform_dict = lookup.parser.show_platform.\
                            ShowPlatform(device=device).parse()
            # Standby RP
            rs = R(['slot', '(?P<val1>.*)', 'rp', '(?P<val2>.*)', 'state', 'ok, standby'])
            ret = find([platform_dict], rs, filter_=False, all_keys=True)
            if not ret:
                raise Exception("Device '{}' does not have standby RP - cannot "
                                "perform ISSU".format(device.name))
            standby_rp = ret[0][1][1]
            srp = re.search('(?P<srp>(\d))', standby_rp).groupdict()['srp']
            logger.info("Standby RP on '{dev}' is: '{standby_rp}'".format(
                        dev=device.name, standby_rp=standby_rp))

        # ======================================================================
        #                          issu loadversion
        # ======================================================================
        with steps.start("Execute 'issu loadversion' to begin ISSU process",
                         continue_=True) as step:
            try:
                output = device.execute('issu loadversion rp {srp} file '
                                        'stby-harddisk:{image}'.format(srp=srp,
                                        image=image_name), timeout=600)
                if 'FAILED' in output:
                    device.execute('issu abortversion', timeout=timeout)
                    raise Exception("Unable to execute 'issu loadversion'")
            except Exception as e:
                raise Exception("Unable to execute 'issu loadversion'")

            # Poll until standby RP reaches 'ok' state in 'show platform'
            logger.info("Poll until standby RP reaches 'ok' state")
            platform_timeout = Timeout(max_time=1200, interval=120)
            while platform_timeout.iterate():
                platform_dict = lookup.parser.show_platform.\
                                ShowPlatform(device=device).parse()
                # Create requirement to find standby-RP with 'ok, standby' state
                rs = R(['slot', '(?P<val1>.*)', 'rp', '(?P<val2>.*)', 'state', 'ok, standby'])
                ret = find([platform_dict], rs, filter_=False, all_keys=True)
                if ret:
                    logger.info("Stanby RP '{}' is in 'ok' state".\
                                format(standby_rp))
                    break
                # Standby RP is not 'ok' state as yet, sleep and recheck
                platform_timeout.sleep()

            # Verify issu state
            logger.info("Verify ISSU state is now 'loadversion'")
            try:
                self.check_issu_state(device=device, slot=standby_rp,
                                      expected_state='loadversion')
                logger.info("ISSU state is 'loadversion' as exepcted")
            except Exception as e:
                raise Exception(str(e))

        # ======================================================================
        #                          issu runversion
        # ======================================================================
        with steps.start("Execute 'issu runversion' to initiate RP failover",
                         continue_=True) as step:
            try:
                output = device.execute('issu runversion', timeout=timeout)
            except SubCommandFailure:
                # Timeout Unicon SubCommandFailure expected
                # Wait a bit as the device is booting with the ISSU upgrade image
                time.sleep(timeout)
                pass

            # Reconnect to device
            logger.info("Reconnect to the device after runversion")
            reconnect_timeout = Timeout(max_time=1200, interval=120)
            self._reconnect(steps=steps, timeout=reconnect_timeout)

            # Verify issu state
            logger.info("Verify ISSU state is now 'runversion'")
            try:
                self.check_issu_state(device=device, slot=standby_rp,
                                      expected_state='runversion')
                logger.info("ISSU state is 'runversion' as exepcted")
            except Exception as e:
                raise Exception(str(e))

        # ======================================================================
        #                          issu acceptversion
        # ======================================================================
        with steps.start("Execute 'issu acceptversion' to cancel rollback timer",
                         continue_=True) as step:
            try:
                output = device.execute('issu acceptversion', timeout=timeout)
                if 'FAILED' in output:
                    raise Exception("Unable to execute 'issu acceptversion'")
            except Exception as e:
                raise Exception("Unable to execute 'issu acceptversion'",
                                from_exception=e)

            # Verify issu state
            logger.info("Verify ISSU state is now 'acceptversion'")
            try:
                self.check_issu_state(device=device, slot=standby_rp,
                                      expected_state='acceptversion')
                logger.info("ISSU state is 'acceptversion' as exepcted")
            except Exception as e:
                raise Exception(str(e))

            # Verify rollback timer
            logger.info("Verify ISSU rollback timer is now 'inactive'")
            try:
                self.check_issu_rollback_timer(device=device, slot=standby_rp,
                                               expected_state='inactive')
                logger.info("ISSU rollback timer is 'inactive' as exepcted")
            except Exception as e:
                raise Exception(str(e))

            # Poll until standby RP reaches 'ok' state in 'show platform'
            logger.info("Poll until standby RP reaches 'ok' state")
            platform_timeout = Timeout(max_time=1200, interval=120)
            while platform_timeout.iterate():
                platform_dict = lookup.parser.show_platform.\
                                ShowPlatform(device=device).parse()
                # Create requirement to find standby-RP with 'ok, standby' state
                rs = R(['slot', '(?P<val1>.*)', 'rp', '(?P<val2>.*)', 'state', 'ok, standby'])
                ret = find([platform_dict], rs, filter_=False, all_keys=True)
                if ret:
                    logger.info("Stanby RP '{}' is in 'ok' state".\
                                format(standby_rp))
                    break
                # Standby RP is not 'ok' state as yet, sleep and recheck
                platform_timeout.sleep()

            # Save running-configuration to startup-configuration
            logger.info("Save running-configuration to startup-configuration")
            filetransfer.copyconfiguration(source='running-config',
                                           destination='startup-config',
                                           device=device)

        # ======================================================================
        #                          issu commitversion
        # ======================================================================
        with steps.start("Execute 'issu commitversion'", continue_=True) as step:
            try:
                output = device.execute('issu commitversion', timeout=timeout)
                if 'FAILED' in output:
                    raise Exception("Unable to execute 'issu commitversion'")
            except Exception as e:
                raise Exception("Unable to execute 'issu commitversion'",
                                from_exception=e)

        # ======================================================================
        #                          reload device
        # ======================================================================
        try:
            reload_timeout = Timeout(max_time=1200, interval=120)
            self.reload(steps=steps, timeout=reload_timeout)
        except Exception as e:
            raise Exception("Unable to reload the device after ISSU completed",
                            from_exception=e)

        # ======================================================================
        #                          verify image version
        # ======================================================================
        with steps.start("Verify device is loaded with upgraded image after ISSU",
                         continue_=True) as step:
            try:
                output = device.execute('show version | i image')
                if image_name in output:
                    logger.info("ISSU upgrade image is successfully loaded on "
                                "the device '{}'".format(device.name))
            except Exception as e:
                raise Exception("Unable to execute 'show version'",
                                from_exception=e)


    def check_disk_space(cls, device, disk, image):
        ''' Check if the ISSU state is in the expected state

            Args:
                device (`obj`): Device Object.
                disk (`str`): Memory location to check for space upto threshold:
                              - harddisk
                              - stby-harddisk:
                image (`str`): ISSU upgrade image full path

            Returns:
                None

            Raises:
                Exception: - Cannot parse 'dir <>' output
                           - Not enough space on disk

            Example:
                >>> check_disk_space(device=uut, disk='harddisk', image=image)
        '''

        # Acceptable states for ISSU to be in
        assert disk in ['harddisk:', 'stby-harddisk:']

        try:
            output = device.execute('dir {}'.format(disk))
        except Exception as e:
            raise Exception("Unable to execute 'dir {}'".format(disk))

        # 78704144384 bytes total (59693568000 bytes free)
        m = re.search('(?P<total>(\d+)) +bytes +total +\((?P<free>(\d+)) '
                      '+bytes +free\)', output)
        bytes_total = m.groupdict()['total']
        bytes_free = m.groupdict()['free']

        if getsize(image) > int(bytes_free):
            raise Exception("Not enough space on '{}' to copy ISSU image".\
                            format(disk))
        else:
            logger.info("Enough space on '{}' to copy ISSU image".format(disk))

    def check_issu_state(cls, device, slot, expected_state, attempt=3, sleep=5):
        ''' Check if the ISSU state is in the expected state

            Args:
                device (`obj`): Device Object.
                expected_state (`str`): Acceptable ISSU states are:
                                        - loadversion
                                        - runversion
                                        - acceptversion
                                        - commitversion
                slot (`str`): Slot for which we need to check ISSU state
                attempt (`int`): Attempt numbers when learn the feature.
                sleep (`int`): The sleep time.

            Returns:
                None

            Raises:
                AssertionError: 'expected_state' is not as expected
                Exception: Cannot parse 'show issu state detail' output
                           No output form 'show issu state detail'
                           Unable to execute 'show issu state detail'

            Example:
                >>> check_issu_state(device=uut, slot='R1',
                                     expected_state='commitversion')
        '''
        assert expected_state in ['loadversion', 'runversion', 'acceptversion',
                                  'commitversion']
        lookup = Lookup.from_device(device)

        for i in range(attempt):
            try:
                issu_dict = lookup.parser.show_issu.\
                            ShowIssuStateDetail(device=device).parse()
                rs = R(['slot', slot, 'last_operation', expected_state])
                ret = find([issu_dict], rs, filter_=False, all_keys=True)
                if ret:
                    break
            except SchemaEmptyParserError as e:
                raise Exception("No output or unable to parse 'show issu state "
                                "detail'", from_exception=e)
            except Exception as e:
                raise Exception("Unable to execute 'show issu state detail'",
                                from_exception=e)
            time.sleep(sleep)
        else:
            raise AssertionError("FAIL: ISSU state not '{}' - this is "
                                 "unexpected".format(expected_state))

    def check_issu_rollback_timer(cls, device, slot, expected_state, attempt=3, sleep=5):
        ''' Check if the ISSU state is in the expected state

            Args:
                device (`obj`): Device Object.
                expected_state (`str`): Acceptable ISSU states are:
                                        - active
                                        - inactive
                slot (`str`): Slot for which we need to check ISSU rollback timer
                attempt (`int`): Attempt numbers when learn the feature.
                sleep (`int`): The sleep time.

            Returns:
                None

            Raises:
                AssertionError: 'expected_state' is not as expected
                Exception: Cannot parse 'show issu rollback timer' output
                           No output form 'show issu rollback timer'
                           Unable to execute 'show issu rollback timer'

            Example:
                >>> check_issu_rollback_timer(device=uut, slot='R1',
                                              expected_state='inactive')
        '''
        assert expected_state in ['active', 'inactive']
        lookup = Lookup.from_device(device)

        for i in range(attempt):
            try:
                issu_dict = lookup.parser.show_issu.\
                            ShowIssuRollbackTimer(device=device).parse()
                if issu_dict and 'rollback_timer_state' in issu_dict and\
                   issu_dict['rollback_timer_state'] == expected_state:
                   break
            except SchemaEmptyParserError as e:
                raise Exception("No output or unable to parse 'show issu "
                                "rollback timer'", from_exception=e)
            except Exception as e:
                raise Exception("Unable to execute 'show issu rollback timer'",
                                from_exception=e)
            time.sleep(sleep)
        else:
            raise AssertionError("FAIL: ISSU rollback timer not '{}' - "
                                 "this is unexpected".format(expected_state))
