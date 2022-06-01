import unittest

from unittest import mock

from unicon.eal.dialogs import Statement

from pyats.results import Passed, Failed
from pyats.aetest.steps import Steps
from pyats.aetest.signals import TerminateStepSignal

from genie.libs.clean.stages.tests.utils import create_test_device
from genie.libs.clean.stages.iosxe.stages import TftpBoot



RESULT_METHODS = ['passed', 'failed', 'skipped', 'passx', 'blocked', 'errored', 'aborted']


class TestTftpBoot(unittest.TestCase):

    def setUp(self):
        self.cls = TftpBoot()
        self.device = create_test_device(
            name='aDevice', os='iosxe')

    def test_check_image_length_pass(self):
        steps = Steps()
        image= ['/some/location/on/tftp/server']
        self.cls.check_image_length(
            steps=steps, image=image)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_check_image_length_fail(self):
        steps = Steps()
        image_length_limit = 10
        image= ['/some/location/on/tftp/server']
        #We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.check_image_length(steps,  image=image,
            image_length_limit=image_length_limit
        )

    def test_set_config_register_pass(self):
        steps = mock.MagicMock()
        self.device.api.execute_set_config_register = mock.Mock()

        self.cls.set_config_register(
            steps=steps, device=self.device)

        # Verify the config command was ran
        self.device.api.execute_set_config_register.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()



    def test_set_config_register_fail(self):
        steps = Steps()

        self.device.api.execute_set_config_register = mock.Mock(side_effect=Exception)

        #We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.set_config_register(
                steps=steps, device=self.device
        )
        # Verify the api was called
        self.device.api.execute_set_config_register.assert_called_once()

    @mock.patch('genie.libs.clean.stages.iosxe.stages.Statement')
    @mock.patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_go_to_rommon_pass(self, dialog, statement):
        steps = mock.MagicMock()
        self.device.sendline = mock.Mock()
        self.device.spawn = mock.Mock()
        self.device.is_ha = False
        self.device.subconnections = mock.MagicMock()
        self.device.expect = mock.Mock()
        self.device.destroy_all = mock.Mock()
        save_system_config = mock.Mock()
        reload_dialog = mock.Mock()
        dialog.return_value = reload_dialog

        self.cls.go_to_rommon(
            steps=steps, device=self.device, save_system_config=save_system_config)

        statement.assert_has_calls([
            mock.call(pattern=r".*System configuration has been modified\. Save\? \[yes\/no\].*",
                      action='sendline(yes)' if save_system_config else 'sendline(no)',
                      loop_continue=True,
                      continue_timer=False),
            mock.call(pattern=r".*Proceed with reload\? \[confirm\].*",
                      action='sendline()',
                      loop_continue=False,
                      continue_timer=False)
        ])

        self.device.sendline.assert_called_with("reload")
        reload_dialog.process.assert_called_with(self.device.spawn)
        self.device.expect.assert_called_with(
            ['(.*Initializing Hardware.*|^(.*)((rommon(.*))+>|switch *:).*$)'], timeout=60)

        self.device.destroy_all.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages.pcall')
    def test_tftp_boot_pass(self, pcall):
        steps = mock.MagicMock()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'
        image = 'bootflash:/test.bin'
        ip_address = '127.0.0.0'
        gateway = '127.0.0.1'
        subnet_mask = '255.0.0.0'
        tftp_server ='0.0.0.0'

        self.cls.tftp_boot(
            steps=steps, device=self.device, image=image, ip_address=ip_address, 
            gateway=gateway,subnet_mask=subnet_mask, tftp_server=tftp_server)

        self.device.instantiate.assert_called_once()

        pcall.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages.pcall')
    @mock.patch('genie.libs.clean.stages.iosxe.stages.Lookup')
    def test_tftp_boot_fail_abstraction_lookup(self, lookup, pcall):
        steps = Steps()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'
        lookup_exception = Exception()
        lookup.from_device.side_effect = lookup_exception
        image = 'bootflash:/test.bin'
        ip_address = '127.0.0.0'
        gateway = '127.0.0.1'
        subnet_mask = '255.0.0.0'
        tftp_server ='0.0.0.0'
        with self.assertRaises(TerminateStepSignal):
            self.cls.tftp_boot(
                steps=steps, device=self.device, image=image, ip_address=ip_address,
                gateway=gateway,subnet_mask=subnet_mask, tftp_server=tftp_server)



    @mock.patch('genie.libs.clean.stages.iosxe.stages.pcall')
    def test_tftp_boot_fail_recovery_worker(self, pcall):
        steps = Steps()
        self.device.instantiate = mock.Mock()
        self.device.is_ha = False
        self.device.start = 'telnet 127.0.0.1 0000'
        pcall_exception = Exception()
        pcall.side_effect = pcall_exception
        image = 'bootflash:/test.bin'
        ip_address = '127.0.0.0'
        gateway = '127.0.0.1'
        subnet_mask = '255.0.0.0'
        tftp_server ='0.0.0.0'
        with self.assertRaises(TerminateStepSignal):
            self.cls.tftp_boot(
                steps=steps, device=self.device, image=image, ip_address=ip_address, 
                gateway=gateway,subnet_mask=subnet_mask, tftp_server=tftp_server)

        self.device.instantiate.assert_called_once()

        pcall.assert_called_once()

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_pass(self, _disconnect_reconnect):
        steps = mock.MagicMock()
        _disconnect_reconnect.return_value = True

        self.cls.reconnect(steps=steps, device=self.device)

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    @mock.patch('genie.libs.clean.stages.iosxe.stages._disconnect_reconnect')
    def test_reconnect_fail(self, _disconnect_reconnect):
        steps = Steps()
        _disconnect_reconnect.return_value = False
        with self.assertRaises(TerminateStepSignal):
            self.cls.reconnect(steps=steps, device=self.device)

    def test_reset_config_register_pass(self):
        steps = mock.MagicMock()
        self.device.api.execute_set_config_register = mock.Mock()

        self.cls.reset_config_register(
            steps=steps, device=self.device)

        # Verify the config command was ran
        self.device.api.execute_set_config_register.assert_called_once()

        #  step_context comes from the following snippet
        #  with steps.start('...') as step_context:
        step_context = steps.start.return_value.__enter__.return_value

        # Verify no step_context methods called
        for result in RESULT_METHODS:
            getattr(step_context, result).assert_not_called()

    def test_set_config_register_fail(self):
        steps = Steps()

        self.device.api.execute_set_config_register = mock.Mock(side_effect=Exception)

        #We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.reset_config_register(
                steps=steps, device=self.device
        )
        # Verify the api was called
        self.device.api.execute_set_config_register.assert_called_once()

    def test_write_memory_pass(self):
        steps = Steps()
        self.device.api.execute_write_memory = mock.Mock()

        self.cls.write_memory(
            steps=steps, device=self.device)

        # Verify the config command was ran
        self.device.api.execute_write_memory.assert_called_once()

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_write_memory__fail(self):
        steps = Steps()

        self.device.api.execute_write_memory = mock.Mock(side_effect=Exception)

        #We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.write_memory(
                steps=steps, device=self.device
        )
        # Verify the api was called
        self.device.api.execute_write_memory.assert_called_once()