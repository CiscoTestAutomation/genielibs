import logging
import unittest

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.sdwan.stages import SetControllerMode
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.parameters import ParameterDict

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class SetControllermode(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = SetControllerMode()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.api.get_username_password = Mock(return_value=('admin', 'admin'))

        # Call the method to be tested (clean step inside class)
        self.cls.set_controller_mode(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


class ConfirmAndSetDefault(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = SetControllerMode()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = '''
        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        License Mode: Controller-Managed

        Smart Licensing Status: Registration Not Applicable/Not Applicable

        cisco ASR1001-X (1NG) processor (revision 1NG) with 3746359K/6147K bytes of memory.
        Processor board ID FXS2412Q36T
        Router operating mode: Controller-Managed
        6 Gigabit Ethernet interfaces
        2 Ten Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        8388608K bytes of physical memory.
        6070271K bytes of eUSB flash at bootflash:.

        Configuration register is 0x2102
        '''

        data1 = '''
                vEdge# show sdwan software
        VERSION         ACTIVE  DEFAULT  PREVIOUS  CONFIRMED  TIMESTAMP
        ---------------------------------------------------------------------------------
        10.106.1.0.12    false   false    true      user       2020-03-30T02:15:00-00:00
        10.106.1.0.32    true    false    false     user       2020-04-11T09:43:37-00:00
        10.106.2.0.1857  false   true     false     auto       2020-03-30T02:13:24-00:00

        Total Space:387M Used Space:141M Available Space:241M     
        '''

        # And we want the following methods to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock(return_value=data)
        self.device.execute = Mock(return_value=data1)
        self.device.instantiate = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.confirm_and_set_default(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_fail_inactive_version(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = '''
        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        License Mode: Controller-Managed

        Smart Licensing Status: Registration Not Applicable/Not Applicable

        cisco ASR1001-X (1NG) processor (revision 1NG) with 3746359K/6147K bytes of memory.
        Processor board ID FXS2412Q36T
        Router operating mode: Controller-Managed
        6 Gigabit Ethernet interfaces
        2 Ten Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        8388608K bytes of physical memory.
        6070271K bytes of eUSB flash at bootflash:.

        Configuration register is 0x2102
        '''
        data1 = '''
                vEdge# show sdwan software
        VERSION         ACTIVE  DEFAULT  PREVIOUS  CONFIRMED  TIMESTAMP
        ---------------------------------------------------------------------------------
        10.106.1.0.12    false   false    true      user       2020-03-30T02:15:00-00:00
        10.106.1.0.32    false    false    false     user       2020-04-11T09:43:37-00:00
        10.106.2.0.1857  false   true     false     auto       2020-03-30T02:13:24-00:00

        Total Space:387M Used Space:141M Available Space:241M     
        '''
         # And we want the following methods to be mocked.
        self.device.connect = Mock(return_value=data)
        self.device.execute = Mock(return_value=data1)
        self.device.instantiate = Mock()

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.confirm_and_set_default(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    

    def test_fail_to_set_controller_mode(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = '''
               A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.

        License Mode: Autonomous

        Smart Licensing Status: Registration Not Applicable/Not Applicable

        cisco ASR1001-X (1NG) processor (revision 1NG) with 3746359K/6147K bytes of memory.
        Processor board ID FXS2412Q36T
        Router operating mode: Autonomous
        6 Gigabit Ethernet interfaces
        2 Ten Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        8388608K bytes of physical memory.
        6070271K bytes of eUSB flash at bootflash:.

        Configuration register is 0x2102
        '''
        data1 = '''
                vEdge# show sdwan software
        VERSION         ACTIVE  DEFAULT  PREVIOUS  CONFIRMED  TIMESTAMP
        ---------------------------------------------------------------------------------
        10.106.1.0.12    false   false    true      user       2020-03-30T02:15:00-00:00
        10.106.1.0.32    true    false    false     user       2020-04-11T09:43:37-00:00
        10.106.2.0.1857  false   true     false     auto       2020-03-30T02:13:24-00:00

        Total Space:387M Used Space:141M Available Space:241M     
        '''
        # And we want the following methods to be mocked.
        self.device.connect = Mock(return_value=data)
        self.device.execute = Mock(return_value=data1)
        self.device.instantiate = Mock()

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.confirm_and_set_default(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[1].result)

