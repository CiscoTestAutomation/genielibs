import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import DeleteFilesFromServer
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Passx, Skipped
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class DeleteFiles(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls =  DeleteFilesFromServer()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.cls.history = {}
    
    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        files = "/home/cisco/kickstart.bin"
        server = "1.1.1.1"

        # And we want the delete_file_on_server api to be mocked so that 
        # it simulates pass case.
        self.device.api.delete_file_on_server = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_files(
            steps=steps, device=self.device, files=files, server=server
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_skip_no_files_to_delete(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        server = "1.1.1.1"

        # When there is no files to delete the step status will be skipped.
        self.cls.delete_files(
            steps=steps, device=self.device, server=server
        )

        # Check the overall result is as expected
        self.assertEqual(Skipped, steps.details[0].result)

    
    def test_skip_no_server_provided(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        files = "/home/cisco/kickstart.bin"

        # When there is no server the step status will be skipped.
        self.cls.delete_files(
            steps=steps, device=self.device, files=files
        )

        # Check the overall result is as expected
        self.assertEqual(Skipped, steps.details[0].result)
    
    
    def test_fail_to_delete_files(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        files = "/home/cisco/kickstart.bin"
        server = "1.1.1.1"

        # And we want the delete_file_on_server api to raise an exception when called.
        # it simulates pass case.
        self.device.api.delete_file_on_server = Mock(side_effect=Exception)
        
        self.cls.delete_files(
            steps=steps, device=self.device, files=files, server=server
        )

        # Check the overall result is as expected
        self.assertEqual(Passx, steps.details[0].result)
    
