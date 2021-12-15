import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.nxos.stages import ChangeBootVariable
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
        self.device = create_test_device('PE1', os='nxos')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_delete_boot_variable api to be mocked so that 
        # it simulates pass case.
        self.device.api.execute_delete_boot_variable = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_boot_variable(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    
    
    def test_fail_to_delete_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_delete_boot_variable api to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_delete_boot_variable = Mock(side_effect=Exception)

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
        self.device = create_test_device('PE1', os='nxos')


    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = {
            'kickstart': 'bootflash:///n3000-uk9-kickstart.6.0.2.U6.10.bin',
            'system': 'bootflash:///n3000-uk10.225.0.2.U6.10.bin',
        }

        # And we want the execute_change_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_change_boot_variable = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.configure_boot_variable(
            steps=steps, device=self.device, images=images
        )

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_pass_current_running_image(self):
        data = {
            'show version': '''
                Cisco Nexus Operating System (NX-OS) Software
                TAC support: http://www.cisco.com/tac
                Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
                Copyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.
                The copyrights to certain works contained herein are owned by
                other third parties and are used and distributed under license.
                Some parts of this software are covered under the GNU Public
                License. A copy of the license is available at
                http://www.gnu.org/licenses/gpl.html.

                Software
                BIOS:      version 1.4.0
                loader:    version N/A
                kickstart: version 6.0(2)U6(10)
                system:    version 6.0(2)U6(10)
                Power Sequencer Firmware:
                        Module 1: version v4.4
                BIOS compile time:       12/09/2013
                kickstart image file is: bootflash:///n3000-uk9-kickstart.6.0.2.U6.10.bin
                kickstart compile time:  3/30/2017 9:00:00 [03/30/2017 19:37:34]
                system image file is:    bootflash:///n3000-uk10.225.0.2.U6.10.bin
                system compile time:     3/30/2017 9:00:00 [03/30/2017 20:04:06]


                Hardware
                cisco Nexus 3048 Chassis ("48x1GE + 4x10G Supervisor")
                Intel(R) Celeron(R) CPU        P4505  @ 1.87GHz with 3665288 kB of memory.
                Processor Board ID FOC19243WQN

                Device name: n3k
                bootflash:    2007040 kB

                Kernel uptime is 796 day(s), 15 hour(s), 58 minute(s), 29 second(s)

                Last reset at 2131 usecs after  Thu Jan 18 21:17:51 2018

                Reason: Disruptive upgrade
                System version: 6.0(2)U6(5b)
                Service:

                plugin
                Core Plugin, Ethernet Plugin
                '''
        }
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute and execute_change_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])
        self.device.api.execute_change_boot_variable = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.configure_boot_variable(
            steps=steps, device=self.device, images=None, current_running_image=True
        )

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)
    

    def test_fail_to_retrieve_current_running_image(self):
        data = {
            'show version': '''
                Cisco Nexus Operating System (NX-OS) Software
                TAC support: http://www.cisco.com/tac
                Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
                Copyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved.
                The copyrights to certain works contained herein are owned by
                other third parties and are used and distributed under license.
                Some parts of this software are covered under the GNU Public
                License. A copy of the license is available at
                http://www.gnu.org/licenses/gpl.html.

                Software
                BIOS:      version 1.4.0
                loader:    version N/A
                kickstart: version 6.0(2)U6(10)
                system:    version 6.0(2)U6(10)
                Power Sequencer Firmware:
                        Module 1: version v4.4
                BIOS compile time:       12/09/2013
                kickstart image file is: bootflash:///n3000-uk9-kickstart.6.0.2.U6.10.bin
                kickstart compile time:  3/30/2017 9:00:00 [03/30/2017 19:37:34]
                system image file is:    bootflash:///n3000-uk10.225.0.2.U6.10.bin
                system compile time:     3/30/2017 9:00:00 [03/30/2017 20:04:06]


                Hardware
                cisco Nexus 3048 Chassis ("48x1GE + 4x10G Supervisor")
                Intel(R) Celeron(R) CPU        P4505  @ 1.87GHz with 3665288 kB of memory.
                Processor Board ID FOC19243WQN

                Device name: n3k
                bootflash:    2007040 kB

                Kernel uptime is 796 day(s), 15 hour(s), 58 minute(s), 29 second(s)

                Last reset at 2131 usecs after  Thu Jan 18 21:17:51 2018

                Reason: Disruptive upgrade
                System version: 6.0(2)U6(5b)
                Service:

                plugin
                Core Plugin, Ethernet Plugin
                '''
        }
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute and execute_change_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock(side_effect=lambda x: data[x])
        self.device.api.execute_change_boot_variable = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_boot_variable(
                steps=steps, device=self.device, images=None, current_running_image=True
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

    def test_fail_to_configure_boot_variable(self):

        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = {
            'kickstart': 'bootflash:///n3000-uk9-kickstart.6.0.2.U6.10.bin',
            'system': 'bootflash:///n3000-uk10.225.0.2.U6.10.bin',
        }

        # And we want the execute_change_boot_variable api to raise an exception when called.
        # This simulates the fail case.        
        self.device.api.execute_change_boot_variable = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.configure_boot_variable(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class SaveRunningConfig(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='nxos')

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

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_save_running_config(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_copy_run_to_start api to raise an exception when called.
        # This simulates the fail case.        
        self.device.api.execute_copy_run_to_start = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.save_running_config(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class VerifyBootVariable(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='nxos')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        images = {
            'kickstart': ['slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin'],
            'system': ['slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin']
        }

        data = {
            'show boot': '''
                Current Boot Variables:

                sup-1
                kickstart variable = slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin
                system variable = slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin
                Boot POAP Disabled
                sup-2
                kickstart variable = slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin
                system variable = slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin
                Boot POAP Disabled
                No module boot variable set

                Boot Variables on next reload:

                sup-1
                kickstart variable = slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin
                system variable = slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin
                Boot POAP Disabled
                sup-2
                kickstart variable = slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin
                system variable = slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin
                Boot POAP Disabled
                No module boot variable set
                '''
        }

        steps = Steps()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_boot_variable(
            steps=steps, device=self.device, images=images
        )

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_verify_boot_variable(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        images = {
            'kickstart': ['slot0:/n7000-s2-kickstart.8.3.0.CV.0.658.gbin'],
            'system': ['slot0:/n7000-s2-dk10.34.3.0.CV.0.658.gbin']
        }

        # And we want the execute method to be mocked with device console output.
        self.device.api.is_next_reload_boot_variable_as_expected = Mock(side_effect=Exception)
        
        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_boot_variable(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class VerifyHaFileTransfer(unittest.TestCase):

    def setUp(self):
        self.cls = ChangeBootVariable()
        self.device = create_test_device('PE1', os='nxos')
        self.device.is_ha = True

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value='No file currently being auto-copied')

        # Call the method to be tested (clean step inside class)
        self.cls.verify_ha_file_transfer(
            steps=steps, device=self.device
        )

        # Check the overall result is as expected
        self.assertEqual(Passed, steps.details[0].result)

    
    def test_fail_to_verify_ha_file_transfer(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        max_time=0
        check_interval=0

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value='Auto-Copy on standby is not yet completed')

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_ha_file_transfer(
                steps=steps, device=self.device, standby_copy_max_time=max_time,
                standby_copy_check_interval=check_interval
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
    
