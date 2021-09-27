import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.stages import ChangeBootVariable
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class DeleteBootVariable(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ChangeBootVariable()

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
        # This simulates the device rejecting a config.
        self.device.configure = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_boot_variable(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class ConfigureBootVariable(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        steps = Steps()

        self.cls.configure_boot_variable(
            steps=steps, device=self.device, images=['bootflash:image.bin']
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_pass_current_running_image(self):
        data = {
            'show version': '''
                Cisco IOS XE Software, Version 16.09.01
                Cisco IOS Software [Fuji], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.1, RELEASE SOFTWARE (fc2)
                Technical Support: http://www.cisco.com/techsupport
                Copyright (c) 1986-2018 by Cisco Systems, Inc.
                Compiled Tue 17-Jul-18 16:57 by mcpre
                
                
                Cisco IOS-XE software, Copyright (c) 2005-2018 by cisco Systems, Inc.
                All rights reserved.  Certain components of Cisco IOS-XE software are
                licensed under the GNU General Public License ("GPL") Version 2.0.  The
                software code licensed under GPL Version 2.0 is free software that comes
                with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
                GPL code under the terms of GPL Version 2.0.  For more details, see the
                documentation or "License Notice" file accompanying the IOS-XE software,
                or the applicable URL provided on the flyer accompanying the IOS-XE
                software.
                
                
                ROM: IOS-XE ROMMON
                
                csr1000v-1 uptime is 1 day, 7 hours, 36 minutes
                Uptime for this control processor is 1 day, 7 hours, 37 minutes
                System returned to ROM by reload
                System image file is "bootflash:packages.conf"
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
                
                License Level: ax
                License Type: Default. No valid license found.
                Next reload license Level: ax
                
                cisco CSR1000V (VXE) processor (revision VXE) with 1217428K/3075K bytes of memory.
                Processor board ID 9VC0Z4MCDFA
                4 Gigabit Ethernet interfaces
                32768K bytes of non-volatile configuration memory.
                3018864K bytes of physical memory.
                7774207K bytes of virtual hard disk at bootflash:.
                0K bytes of WebUI ODM Files at webui:.
                
                Configuration register is 0x2102''',
        }

        steps = Steps()
        self.device.execute = Mock(side_effect=lambda x: data[x])

        self.cls.configure_boot_variable(
            steps=steps, device=self.device, images=None, current_running_image=True
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_set_boot_variable(self):
        steps = Steps()
        self.device.api.execute_set_boot_variable = Mock(side_effect=Exception)

        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_boot_variable(
                steps=steps, device=self.device, images=['bootflash:image.bin']
            )

        self.assertEqual(Failed, steps.details[0].result)


class SetConfigurationRegister(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        steps = Steps()

        self.cls.set_configuration_register(
            steps=steps, device=self.device, config_register='0x2102'
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_set_configuration_register(self):
        steps = Steps()
        self.device.api.execute_set_config_register = Mock(side_effect=Exception)

        with self.assertRaises(TerminateStepSignal):
            self.cls.set_configuration_register(
                steps=steps, device=self.device, config_register='0x2102'
            )

        self.assertEqual(Failed, steps.details[0].result)


class WriteMemory(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        steps = Steps()
        self.device.execute = Mock(return_value='[OK]')

        self.cls.write_memory(
            steps=steps, device=self.device
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_write_memory(self):
        steps = Steps()
        self.device.api.write_memory = Mock(side_effect=Exception)

        with self.assertRaises(TerminateStepSignal):
            self.cls.write_memory(
                steps=steps, device=self.device
            )

        self.assertEqual(Failed, steps.details[0].result)


class VerifyBootVariable(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        bootvar = 'harddisk:/vmlinux_PE1.bin'

        data = {
            'show bootvar': '''
                BOOT variable = {},12;
                CONFIG_FILE variable =
                BOOTLDR variable does not exist
                Configuration register is 0x2102
    
                Standby not ready to show bootvar'''.format(bootvar)
        }

        steps = Steps()
        self.device.execute = Mock(side_effect=lambda x: data[x])

        self.cls.verify_boot_variable(
            steps=steps, device=self.device, images=[bootvar]
        )

        self.assertEqual(Passed, steps.details[0].result)

    def test_config_register_mismatch(self):
        data = {
            'show bootvar': '''
                BOOT variable = harddisk:/vmlinux_PE1.bin,12;
                CONFIG_FILE variable =
                BOOTLDR variable does not exist
                Configuration register is 0x2102
    
                Standby not ready to show bootvar'''
        }

        steps = Steps()
        self.device.execute = Mock(side_effect=lambda x: data[x])

        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_boot_variable(
                steps=steps, device=self.device, images=['shouldnt exist']
            )

        self.assertEqual(Failed, steps.details[0].result)


class VerifyConfigurationRegister(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        confreg = 'banana'

        data = {
            'show bootvar': '''
                BOOT variable = harddisk:/vmlinux_PE1.bin,12;
                CONFIG_FILE variable =
                BOOTLDR variable does not exist
                Configuration register is {}
    
                Standby not ready to show bootvar'''.format(confreg)
        }

        steps = Steps()
        self.device.execute = Mock(side_effect=lambda x: data[x])

        self.cls.verify_configuration_register(
            steps=steps, device=self.device, config_register=confreg
        )

        self.assertEqual(Passed, steps.details[0].result)


class BlackBoxTest(CommonStageTests, unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='iosxe')
