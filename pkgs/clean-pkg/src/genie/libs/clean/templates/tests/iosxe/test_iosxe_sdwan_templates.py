import logging
import unittest

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.parameters import ParameterDict

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal, AEtestPassedSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestIosxeSdwanCleanTemplate(unittest.TestCase):

    def setUp(self):

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_set_controller_mode_pass(self):
        # setting the expected output as default hostname in the sdwan template
        Expected_output = 'enable'

        # To get the sdwan specific template
        Actual_output = self.device.api.clean.template

        # Check that the result is expected
        self.assertEqual(Expected_output, Actual_output['set_controller_mode']['mode'])

