import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import DeleteBackupFromDevice
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class RestoreBackup(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = DeleteBackupFromDevice()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the copy method to be mocked
        # To simulate pass case
        self.device.copy = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.restore_backup(
            steps=steps, device=self.device, delete_dir='bootflash:',\
            delete_file='ISSUCleanGolden.cfg_backup', restore_from_backup=True
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_fail_to_restore_backup(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the copy method to be mocked
        # To simulate fail case
        self.device.copy = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.restore_backup(
                steps=steps, device=self.device, delete_dir='bootflash:',\
                delete_file='ISSUCleanGolden.cfg_backup', restore_from_backup=True
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class DeleteFile(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = DeleteBackupFromDevice()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked
        # To simulate pass case
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_file(
            steps=steps, device=self.device, delete_dir='bootflash:',\
            delete_file='ISSUCleanGolden.cfg_backup'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_fail_to_delete_file(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked
        # To simulate fail case
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_file(
                steps=steps, device=self.device, delete_dir='bootflash:',\
                delete_file='ISSUCleanGolden.cfg_backup'
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class DeleteFilesOnStandby(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = DeleteBackupFromDevice()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.device.is_ha = True

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked
        # To simulate pass case
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_file_on_stby(
            steps=steps, device=self.device, delete_dir='bootflash:',\
            delete_file='ISSUCleanGolden.cfg_backup',\
            delete_dir_stby='bootflash-stby:'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_skip_to_delete_files_on_standby(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked
        # To simulate skip case
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_file_on_stby(
            steps=steps, device=self.device, delete_dir='bootflash:',\
            delete_file='ISSUCleanGolden.cfg_backup', delete_dir_stby=None
        )

        # Check that the result is expected
        self.assertEqual(Skipped, steps.details[0].result)

    
    def test_fail_to_delete_files_on_standby(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked
        # To simulate fail case
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_file_on_stby(
                steps=steps, device=self.device, delete_dir='bootflash:',\
                delete_file='ISSUCleanGolden.cfg_backup', delete_dir_stby='bootflash-stby:'
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

