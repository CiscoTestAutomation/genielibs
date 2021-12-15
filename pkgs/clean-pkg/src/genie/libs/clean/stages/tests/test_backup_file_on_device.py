import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import BackupFileOnDevice
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class VerifyEnoughAvailableDiskSpace(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = BackupFileOnDevice()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
                        1940303872 bytes total (1036210176 bytes free)
        '''
        }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_enough_available_disk_space(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    
    
    def test_fail_to_get_file_size(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        1940303872 bytes total (1036210176 bytes free)
        '''
        }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_enough_available_disk_space(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    

    def test_fail_to_get_available_disk_space(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             4096  Nov 25 2016 18:42:07 -07:00  test.bin
        '''
        }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_enough_available_disk_space(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    

    def test_fail_low_available_disk_space(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        data = {'dir bootflash:/': '''
                   Directory of bootflash:/
                        11  drwx            16384  Nov 25 2016 19:32:53 -07:00  lost+found
                        12  -rw-                0  Dec 13 2016 11:36:36 -07:00  ds_stats.txt
                        104417  drwx             4096  Apr 10 2017 09:09:11 -07:00  .prst_sync
                        80321  drwx             4096  Nov 25 2016 19:40:38 -07:00  .rollback_timer
                        64257  drwx             4096  Nov 25 2016 19:41:02 -07:00  .installer
                        48193  drwx             4096  Nov 25 2016 19:41:14 -07:00  virtual-instance-stby-sync
                        8033  drwx             8500  Nov 25 2016 18:42:07 -07:00  test.bin
                        1940303872 bytes total (7000 bytes free)
        '''
        }

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_enough_available_disk_space(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    

class CreateBackup(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = BackupFileOnDevice()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    
    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        # And we want the copy method to be mocked so that 
        # it simulates pass case.
        self.device.copy = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.create_backup(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_create_backup(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        copy_dir = "bootflash:/"
        copy_file = "test.bin"

        # And we want the copy method to be mocked to rise exception, so that 
        # it simulates fail case.
        self.device.copy = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.create_backup(
            steps=steps, device=self.device, copy_dir=copy_dir, copy_file=copy_file
        )
        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

