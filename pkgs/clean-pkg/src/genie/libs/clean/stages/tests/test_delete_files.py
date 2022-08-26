import unittest

from unittest.mock import Mock, call

from genie.libs.clean.stages.stages import DeleteFiles
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed



class TestDeleteFiles(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls =  DeleteFiles()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.cls.history = {}

    def test_delete_files(self):
        steps = Steps()
        files = ["/home/cisco/*.bin"]

        # And we want the delete_file_on_server api to be mocked so that
        # it simulates pass case.
        self.device.api.delete_files = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_files(
            steps=steps, device=self.device, files=files
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

        # Check if the API was called with the matching location and filename regex
        self.device.api.delete_files.assert_has_calls(
            [call(locations=['/home/cisco'], filenames=['(?s:.*\\.bin)\\Z'])])

    def test_delete_files_regex(self):
        steps = Steps()
        files = ["/home/cisco/.*.bin"]

        # And we want the delete_file_on_server api to be mocked so that
        # it simulates pass case.
        self.device.api.delete_files = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_files(
            steps=steps, device=self.device, files=files, regex=True
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

        # Check if the API was called with the matching location and filename regex
        self.device.api.delete_files.assert_has_calls([
            call(locations=['/home/cisco'], filenames=['.*.bin'])])
