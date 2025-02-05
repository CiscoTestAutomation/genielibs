import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.stages import InstallRemoveSmu
from genie.libs.clean.stages.tests.utils import create_test_device


from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class RemoveInactiveSmu(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallRemoveSmu()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock()

        self.device.parse = Mock(return_value={
                                 'location': {
                                     'Switch 1': {
                                         'pkg_state': {
                                             1: {'type': 'IMG',
                                                 'state': 'C',
                                                 'filename_version': '17.17.01.0.207986'},
                                             2: {'type': 'SMU',
                                                 'state': 'I',
                                                 'filename_version': r'flash://server/image.smu.bin'}},
                                         'auto_abort_timer': 'inactive'
                                         }}})

        # Call the method to be tested (clean step inside class)
        self.cls.remove_smu_image(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_remove_inactive_smu(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to raise an exception when called.
        # This simulates the fail case.
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.remove_smu_image(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
