import logging
import unittest

from unittest.mock import Mock, call

from genie.libs.clean.stages.stages import ApplyConfiguration
from genie.libs.clean.stages.tests.utils import  create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Applyconfiguration(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ApplyConfiguration()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        configuration = '''
            configuration: |
            interface ethernet2/1
            no shutdown
        '''

        # And we want the configure method to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()
        self.device.configure = Mock()
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.apply_configuration(
            steps=steps, device=self.device, config_stable_time=4,\
            configuration=configuration, copy_vdc_all=True,\
            copy_directly_to_startup=True, skip_copy_run_start=True
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[1].result)
        self.device.execute.assert_has_calls([
            call('show running-config', timeout=300, error_pattern=[]),
            call('show startup-config', timeout=300, error_pattern=[])])


    def test_fail_to_apply_configuration(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        configuration = '''
            configuration: |
            interface ethernet2/1
            no shutdown
        '''
        file ="test.cfg"

        # And we want the configure method to be mocked.
        # This simulates the fail case.
        self.device.configure = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.apply_configuration(
                steps=steps, device=self.device, config_stable_time=2,\
                configuration=configuration, file="test.cfg"
            )
        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)


    def test_fail_to_execute_copy_run_start(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        configuration = '''
            configuration: |
            interface ethernet2/1
            no shutdown
        '''

        # And we want the configure method to be mocked.
        self.device.configure = Mock()

        # And we want the execute_copy_run_api_to_start to be mocked to raise exception.
        # This simulates the fail case.
        self.device.api.execute_copy_run_to_start = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.apply_configuration(
                    steps=steps, device=self.device, config_stable_time=0,\
                    configuration=configuration, file="test.cfg", copy_vdc_all=True
                )

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[1].result)

    def test_skip_if_no_config_no_configuration_provided(self):
        # When skip_if_no_config is True and no configuration is provided,
        # the stage should skip via self.skipped().
        steps = Steps()

        self.device.configure = Mock()
        self.device.execute = Mock()

        with self.assertRaises(AEtestSkippedSignal):
            self.cls.apply_configuration(
                steps=steps, device=self.device,
                skip_if_no_config=True
            )

        # No steps should have been executed
        self.device.configure.assert_not_called()
        self.device.execute.assert_not_called()

    def test_skip_if_no_config_with_configuration_provided(self):
        # When skip_if_no_config is True but configuration IS provided,
        # the stage should still execute normally.
        steps = Steps()
        configuration = 'interface ethernet2/1\nno shutdown'

        self.device.configure = Mock()
        self.device.execute = Mock()

        self.cls.apply_configuration(
            steps=steps, device=self.device, config_stable_time=0,
            configuration=configuration, skip_if_no_config=True,
            copy_directly_to_startup=True, skip_copy_run_start=True
        )

        # Steps should have been executed
        self.assertGreater(len(steps.details), 0)
        self.assertEqual(Passed, steps.details[1].result)

    def test_skip_if_no_config_false_no_configuration(self):
        # When skip_if_no_config is False (default) and no configuration
        # is provided, the stage should still execute (not skip).
        steps = Steps()

        self.device.configure = Mock()
        self.device.execute = Mock()

        self.cls.apply_configuration(
            steps=steps, device=self.device, config_stable_time=0,
            skip_if_no_config=False,
            copy_directly_to_startup=True, skip_copy_run_start=True
        )

        # Steps should have been executed even without configuration
        self.assertGreater(len(steps.details), 0)

