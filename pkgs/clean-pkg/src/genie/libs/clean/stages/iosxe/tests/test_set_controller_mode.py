import logging
import unittest

from types import SimpleNamespace
from unittest.mock import Mock, MagicMock
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import SetControllerMode
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.parameters import ParameterDict

from pyats.aetest.steps import Steps
from pyats.kleenex.testbed_config import TestbedConfigCollector
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


def set_active_connection(device, via):
    """Add a current default connection with its selected testbed via."""
    device.connections.update({
        'a': {'protocol': 'telnet'},
        'ssh': {'protocol': 'ssh'},
    })
    device.connectionmgr.connections['cli'] = SimpleNamespace(
        via=via, connected=True)
    device.default_connection_alias = 'cli'
    device.destroy_all = Mock()


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
        self.device.parse = Mock()
        self.device.api.get_username_password = Mock(
            return_value=('admin', 'admin'))

        # Call the method to be tested (clean step inside class)
        self.cls.set_controller_mode(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_reuses_connect_stage_via_for_reconnect(self):
        steps = Steps()
        set_active_connection(self.device, via='a')
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.parse = Mock(return_value={})
        self.device.api.get_username_password = Mock(
            return_value=('admin', 'admin'))

        self.cls.set_controller_mode(
            steps=steps, device=self.device, mode='disable')

        self.device.destroy_all.assert_called_once_with()
        self.device.connect.assert_called_once_with(
            learn_tokens=False,
            via='a',
        )

    def test_includes_platform_reload_dialog_for_grub_handling(self):
        """Verify the stage appends the platform's reload dialog so that
        devices entering the grub prompt are handled by the Unicon
        platform layer rather than hardcoded clean stage logic."""
        steps = Steps()
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.parse = Mock()
        self.device.api.get_username_password = Mock(
            return_value=('admin', 'admin'))

        # Use the real C8KV reload service dialog which contains
        # boot_from_rommon_stmt and grub_prompt_stmt.
        from unicon.eal.dialogs import Dialog
        from unicon.plugins.iosxe.c8kv.statements import \
            boot_from_rommon_stmt
        from unicon.plugins.iosxe.statements import grub_prompt_stmt
        from unicon.plugins.generic.service_statements import \
            reload_statement_list
        from unicon.plugins.generic.statements import \
            default_statement_list
        reload_dialog = Dialog(
            [boot_from_rommon_stmt, grub_prompt_stmt]
            + reload_statement_list
            + default_statement_list)
        self.device.reload = Mock()
        self.device.reload.dialog = reload_dialog

        self.cls.set_controller_mode(
            steps=steps, device=self.device, mode='disable')

        dialog = self.device.execute.call_args.kwargs['service_dialog']
        patterns = [stmt.pattern for stmt in dialog]

        # The C8KV reload dialog's grub prompt statement must be present
        self.assertIn(grub_prompt_stmt.pattern, patterns)
        # The C8KV boot_from_rommon_stmt must be present
        self.assertIn(boot_from_rommon_stmt.pattern, patterns)

    def test_default_admin_password_change_handled(self):
        """Verify the stage keeps targeted handlers for the default-admin
        password change forced after the NVRAM reset."""
        steps = Steps()
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.parse = Mock()
        self.device.api.get_username_password = Mock(
            return_value=('admin', 'Secret123'))

        self.cls.set_controller_mode(
            steps=steps, device=self.device, mode='disable')

        dialog = self.device.execute.call_args.kwargs['service_dialog']
        statements = {stmt.pattern: stmt for stmt in dialog}

        # controller-mode confirmation prompts
        self.assertIn(r"Continue\? \[confirm\]", statements)
        self.assertIn(r"Do you want to abort\? \(yes/\[no\]\):", statements)

        def sent_value(pattern):
            """Run the statement action and return what was sent."""
            spawn = Mock()
            stmt = statements[pattern]
            stmt.action(spawn, **stmt.args)
            return spawn.sendline.call_args.args[0]

        # factory-default credentials are sent, not the testbed ones
        self.assertEqual('admin', sent_value(r"Username:"))
        self.assertEqual('admin', sent_value(r"Password:"))
        # the configured password is used for the forced password change
        self.assertEqual('Secret123', sent_value(r"Enter new password:"))
        self.assertEqual('Secret123', sent_value(r"Confirm password:"))

    def test_press_return_continues_through_authentication(self):
        """The controller-mode Press RETURN prompt must not end execute."""
        steps = Steps()
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.parse = Mock()
        self.device.api.get_username_password = Mock(
            return_value=('admin', 'Secret132'))

        from unicon.eal.dialogs import Dialog, Statement
        self.device.reload = Mock()
        reload_press_return = Statement(
            pattern=r".*Press RETURN to get started.*",
            action="sendline()",
            loop_continue=False,
            continue_timer=False)
        final_prompt = Statement(
            pattern=r"Router#",
            action=None,
            loop_continue=False,
            continue_timer=False)
        self.device.reload.dialog = Dialog([reload_press_return, final_prompt])

        self.cls.set_controller_mode(
            steps=steps, device=self.device, mode='enable',
            reload_timeout=1800)

        dialog = self.device.execute.call_args.kwargs['service_dialog']
        press_returns = [
            stmt for stmt in dialog
            if stmt.pattern == r".*Press RETURN to get started.*"
        ]
        press_return = press_returns[0]

        self.assertEqual(2, len(press_returns))
        self.assertTrue(press_return.loop_continue)
        self.assertFalse(press_returns[1].loop_continue)
        self.assertEqual(1800,
                         self.device.execute.call_args.kwargs['timeout'])

        spawn = Mock()
        press_return.action(spawn, **press_return.args)
        spawn.sendline.assert_called_once_with('')

        # Authentication and the forced password change remain in the same
        # dialog after Press RETURN.
        patterns = [stmt.pattern for stmt in dialog]
        for pattern in (r"Username:", r"Password:",
                        r"Enter new password:", r"Confirm password:",
                        r"Router#"):
            self.assertIn(pattern, patterns)

    def test_skipped(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()
        self.device.execute = Mock()
        self.device.parse = MagicMock()
        d = {'version': {'router_operating_mode': 'Controller-Managed'}}
        self.device.parse.return_value = d

        # Call the method to be tested (clean step inside class)
        # Assert it raises a skipped signal
        with self.assertRaises(AEtestSkippedSignal):
            self.cls.set_controller_mode(
                steps=steps, device=self.device
            )


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

    def test_reuses_connect_stage_via_with_token_learning(self):
        steps = Steps()
        set_active_connection(self.device, via='a')
        self.device.connect = Mock(
            return_value='Router operating mode: Autonomous')

        self.cls.confirm_and_set_default(
            steps=steps, device=self.device, mode='disable')

        self.device.destroy_all.assert_called_once_with()
        self.device.connect.assert_called_once_with(
            learn_tokens=True,
            overwrite_testbed_tokens=True,
            via='a',
        )

    def test_pass_mode_disable(self):
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
        Router operating mode: Autonomous
        6 Gigabit Ethernet interfaces
        2 Ten Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        8388608K bytes of physical memory.
        6070271K bytes of eUSB flash at bootflash:.

        Configuration register is 0x2102
        '''

        # And we want the following methods to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        self.cls.confirm_and_set_default(
            steps=steps, device=self.device, mode='disable'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_mode_disable_reuses_active_via_with_token_learning(self):
        steps = Steps()
        set_active_connection(self.device, via='a')
        self.device.connect = Mock(
            return_value='Router operating mode: Autonomous')

        self.cls.confirm_and_set_default(
            steps=steps, device=self.device, mode='disable')

        self.device.destroy_all.assert_called_once_with()
        self.device.connect.assert_called_once_with(
            learn_tokens=True,
            overwrite_testbed_tokens=True,
            via='a',
        )

    def test_mode_enable_prefers_explicit_via(self):
        steps = Steps()
        set_active_connection(self.device, via='a')
        self.device.connect = Mock(
            return_value='Router operating mode: Controller-Managed')
        parsed_output = MagicMock()
        parsed_output.q.contains_key_value.return_value.get_values.side_effect = [
            '17.15.1a', ['17.12.1a']
        ]
        self.device.parse = Mock(return_value=parsed_output)
        self.device.execute = Mock()

        self.cls.confirm_and_set_default(
            steps=steps,
            device=self.device,
            mode='enable',
            via='ssh',
        )

        self.device.destroy_all.assert_called_once_with()
        self.device.connect.assert_called_once_with(
            learn_tokens=True,
            overwrite_testbed_tokens=True,
            via='ssh',
        )

    def test_pass_mode_disable_publishes_autonomous_platform(self):
        steps = Steps()
        collector = TestbedConfigCollector()
        self.device.platform = 'c8000be'
        self.device.connect = Mock(
            return_value='Router operating mode: Autonomous')

        self.cls.confirm_and_set_default(
            steps=steps,
            device=self.device,
            mode='disable',
            testbed_config=collector,
        )

        self.assertEqual(
            {
                'devices': {
                    'PE1': {
                        'platform': 'c8000be',
                    },
                },
            },
            collector.as_dict(),
        )
        self.assertEqual('SetControllerMode',
                         collector.documents[0]['source']['stage'])

    def test_pass_mode_enable_publishes_learned_sdwan_platform(self):
        steps = Steps()
        collector = TestbedConfigCollector()
        self.device.platform = 'c8000be'

        def connect(**kwargs):
            self.device.platform = 'sdwan'
            return 'Router operating mode: Controller-Managed'

        self.device.connect = Mock(side_effect=connect)
        self.device.execute = Mock()
        active_versions = Mock()
        active_versions.get_values.return_value = '17.9.1'
        inactive_versions = Mock()
        inactive_versions.get_values.return_value = []
        parsed_output = Mock()
        parsed_output.q.contains_key_value.side_effect = [
            active_versions,
            inactive_versions,
        ]
        self.device.parse = Mock(return_value=parsed_output)

        self.cls.confirm_and_set_default(
            steps=steps,
            device=self.device,
            mode='enable',
            testbed_config=collector,
        )

        self.device.connect.assert_called_once_with(
            learn_tokens=True,
            overwrite_testbed_tokens=True,
        )
        self.assertEqual(
            {
                'devices': {
                    'PE1': {
                        'platform': 'sdwan',
                    },
                },
            },
            collector.as_dict(),
        )

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
