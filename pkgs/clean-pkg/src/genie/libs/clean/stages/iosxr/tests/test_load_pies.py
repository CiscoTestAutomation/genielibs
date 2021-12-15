import logging
import unittest

from unittest.mock import Mock, MagicMock

from genie.libs.clean.stages.iosxr.stages import LoadPies
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Install_Pies(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = LoadPies()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxr')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_install_pie method to be mocked.
        # This simulates the pass case.
        self.device.api.execute_install_pie = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.install_pies(
            steps=steps, device=self.device, files=['/auto/path/to/image/asr9k-mcast-px.pie-7.3.1.08I']
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_install_pie(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_install_pie method to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_install_pie = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_pies(
                steps=steps, device=self.device, files=['/auto/path/to/image/asr9k-mcast-px.pie-7.3.1.08I']
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class Verify_Pies_Installed(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = LoadPies()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxr')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        data = {
            'show install active summary': '''
                Default Profile:
                SDRs:
                    Owner
                Active Packages:
                    disk0:asr9k-mini-px-6.1.21.15I
                    disk0:asr9k-mpls-px-6.1.21.15I
                    disk0:asr9k-mcast-px-6.1.21.15I
                    disk0:asr9k-mgbl-px-6.1.21.15I
               ''',
        }

        self.device.execute = Mock(side_effect=lambda x: data[x])
        self.cls.installed_packages = ['asr9k-mini-px-6.1.21.15I', 'asr9k-mpls-px-6.1.21.15I', 'asr9k-mcast-px-6.1.21.15I', 'asr9k-mgbl-px-6.1.21.15I']

        # And we want the verify_installed_pies method to be mocked.
        # This simulates the pass case.
        self.device.api.verify_installed_pies(self.cls.installed_packages, 0, 0)

        # Call the method to be tested (clean step inside class)
        self.cls.verify_pies_installed(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_fail_to_verify_pies(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.installed_packages = []

        # And we want the verify_installed_pies method to be mocked.
        # This simulates the fail case.
        self.device.api.verify_installed_pies = Mock(return_value = None)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_pies_installed(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
        
