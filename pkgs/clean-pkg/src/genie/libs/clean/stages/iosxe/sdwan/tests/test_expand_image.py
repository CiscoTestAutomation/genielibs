import logging
import unittest

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.sdwan.stages import ExpandImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.parameters import ParameterDict

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class EraseConfig(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ExpandImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.erase_config(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


class CleanPackage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ExpandImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.clean_package(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


class Expand_Image(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ExpandImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'ExpandImage': self.cls.mock_value})
        self.cls.history['ExpandImage'].parameters =  OrderedDict()
        
        data = '''
        Sample Outputs:
            WARNING: bootflash:asr1000-universalk9.17.06.01a.SPA.18.conf
            WARNING: packages.conf will replace the identical file that already exists in bootflash:
        '''

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        self.cls.expand_image(
            steps=steps, device=self.device, image=['bootflash:stay-isr-image.bin']
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

