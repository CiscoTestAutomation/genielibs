import logging
import unittest

from unittest.mock import Mock, MagicMock, call, ANY
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device


from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal

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

        def mock_execute(*args, **kwargs):
            assert args == ('puts [open "bootflash:/packages.conf" w+] {}',)

        self.device.tclsh = mock_execute

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

        def mock_execute(*args, **kwargs):
            assert args == ('puts [open "bootflash:/packages.conf" w+] {}',)

        self.device.tclsh = mock_execute

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
        self.device.reload = Mock()
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
        self.device.reload = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class TestInstallImage(unittest.TestCase):

    def test_iosxe_install_image_pass(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.reload = Mock()
        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        device.reload.assert_has_calls([
            call('install add file sftp://server/image.bin activate commit', reply=ANY,
                 reload_creds='default', prompt_recovery=True, error_pattern=['FAILED:.*?$'],
                 timeout=500, device_recovery=False)
        ])
        self.assertEqual(Passed, steps.details[0].result)

    def test_iosxe_install_image_skip(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.api.get_running_image.return_value = 'sftp://server/image.bin'
        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])
        self.assertEqual(Skipped, steps.details[0].result)

    def test_iosxe_install_image_grub_boot_image(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.reload = Mock()
        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'],
                          reload_service_args=dict(grub_boot_image='packages.conf'))

        device.reload.assert_has_calls([
            call('install add file sftp://server/image.bin activate commit', reply=ANY,
                 reload_creds='default', prompt_recovery=True, error_pattern=['FAILED:.*?$'],
                 grub_boot_image='packages.conf', device_recovery=False, timeout=500)
        ])
        self.assertEqual(Passed, steps.details[0].result)

class TestVerifyRunningImage(unittest.TestCase):

    def setUp(self):
        self.cls = InstallImage()
        self.device = create_test_device('PE1', os='iosxe', platform='cat9k')

    def test_iosxe_verify_running_image_skipped(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Wed 15-Jun-11 08:54 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
ROM: Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]

issu-asr-lns uptime is 1 hour, 16 minutes
Uptime for this control processor is 1 hour, 17 minutes
System returned to ROM by reload
System image file is "flash:/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco ASR1006 (RP2) processor with 4254354K/6147K bytes of memory.
3 ATM interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1826815K bytes of eUSB flash at bootflash:.
78085207K bytes of SATA hard disk at harddisk:.

Configuration register is 0x1
                    '''
                }

            def __call__(self, cmd, *args, **kwargs):
                output = self.data.get(cmd)
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()
        with self.assertRaises(AEtestSkippedSignal):
            self.cls.verify_running_image(steps=steps,
                                          device=self.device,
                                          images=['/path/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin']
            )

        self.assertEqual(Skipped, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('show version')
        ])

        self.assertEqual(self.cls.history['InstallImage'].parameters['image_mapping'],
                         {'/path/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin':
                          'flash:/asr1000-universalk9.BLD_MCP_DEV_LATEST_20110615_044519.SSA.bin'})
