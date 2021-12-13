import logging
import unittest

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device


from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class DeleteBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_boot_variable(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_delete_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure method to raise an exception when called.
        # This simulates the fail case.
        self.device.configure = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_boot_variable(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class SetBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

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
        self.device.execute = Mock(return_value = data['dir bootflash:/'])

        # And we want the execute_set_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_set_boot_variable = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.set_boot_variable(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_set_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
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
        self.device.execute = Mock(return_value = data['dir bootflash:/'])

        # And we want the execute_set_boot_variable api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_set_boot_variable = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.set_boot_variable(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class SaveRunningConfig(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_copy_run_to_start = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.save_running_config(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_save_running_config(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_copy_run_to_start = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.save_running_config(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class VerifyBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='cat9k')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.new_boot_var = 'bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin'

        data1 = {'show boot': '''
            starfleet-1#show boot
            BOOT variable = bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;
            Configuration Register is 0x102
            MANUAL_BOOT variable = no
            BAUD variable = 9600
            ENABLE_BREAK variable does not exist
            BOOTMODE variable does not exist
            IPXE_TIMEOUT variable does not exist
            CONFIG_FILE variable =
        '''
        }

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(return_value=data1['show boot'])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_boot_variable(
            steps=steps, device=self.device
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_verify_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.cls.new_boot_var = 'flash:cat9k_iosxe.BLD_V173_999.SSA.bin'

        data1 = {'show boot': '''
            starfleet-1#show boot
            BOOT variable = bootflash:cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;
            Configuration Register is 0x102
            MANUAL_BOOT variable = no
            BAUD variable = 9600
            ENABLE_BREAK variable does not exist
            BOOTMODE variable does not exist
            IPXE_TIMEOUT variable does not exist
            CONFIG_FILE variable =
        '''
        }

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock(return_value=data1['show boot'])

        # And we want the execute_copy_run_to_start api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_copy_run_to_start = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.save_running_config(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class Installimage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    
    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.new_boot_var = 'flash:cat9k_iosxe.BLD_V173_999.SSA.bin'
        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.install_image(
            steps=steps, device=self.device, images=images
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    

    def test_fail_to_install_image(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.history = {}

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class WaitForReload(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.device.hostname = 'PE1'


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.wait_for_reload(
            steps=steps, device=self.device, reload_timeout=2
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    

    def test_fail_to_wait_for_reload(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect to be mocked raise an exception when called.
        # This simulates the fail case.
        self.device.connect = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.wait_for_reload(
                steps=steps, device=self.device, reload_timeout=2
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

