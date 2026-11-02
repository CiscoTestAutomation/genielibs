import re
import unittest
import logging

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.stages import InstallImage
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon import Connection
from unicon.core.errors import SubCommandFailure
from unicon.core.errors import TimeoutError as UniconTimeoutError
from unicon.mock.mock_device import MockDeviceTcpWrapper

logger = logging.getLogger(__name__)

class TestInstallImage(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE cat9k device """

    def setUp(self):
        self.cls = InstallImage()
        self.device = create_test_device('router', os='iosxe', platform='cat9k')
        self.device.state_machine = Mock()
        self.device.spawn = Mock()
        self.device.spawn.read_update_buffer = Mock(return_value='')
        self.device.spawn.match_buffer = Mock(return_value=False)
        # Unicon's expect service wraps a timeout in SubCommandFailure.
        self.device.expect = Mock(side_effect=SubCommandFailure(
            'Failed to match buffer on spawn',
            UniconTimeoutError('Timeout occurred')))

        self.device.api = Mock()
        self.device.api.get_platform_default_dir = Mock(return_value='bootflash:/')
        self.device.api.get_file_size_from_server = Mock(return_value=100000)
        self.device.api.verify_enough_disk_space = Mock(return_value=True)
        self.device.api.get_running_image = Mock(return_value='old_image.bin')
        self.device.api.copy_from_device = Mock(return_value=True)

        self.image = 'image.bin'
        self.install_command = (
            'install add file image.bin activate commit prompt-level none')
        self.already_added_output = (
            'install_add_activate_commit: START\n'
            '  [1] R0 FAILED: Super package already added. '
            'Add operation not allowed\n'
            '  [1] R1 FAILED: Super package already added. '
            'Add operation not allowed\n'
            'FAILED: install_add_activate_commit image.bin\n')

        # Mock the history attribute
        self.cls.history = {
            "InstallImage": type('MockParameters', (), {
                'parameters': {"image_mapping": {}}
            })()
        }

        self.data = {
            'show version | include operating mode': '',
            'show install summary': '',
            'show version': '''
                Cisco IOS XE Software, Version 17.12.01
                cisco C9300-24U (X86_64_LINUX_IOSXE) processor
            ''',
            'show install active': '''
                [ Switch 1 ] Active Package(s) Information:
                State (St): I - Inactive, U - Activated & Uncommitted,
                            C - Activated & Committed, D - Deactivated & Uncommitted
                --------------------------------------------------------------------------------
                Type  St   Filename/Version
                --------------------------------------------------------------------------------
                IMG   C    26.01.01.0.228502

                --------------------------------------------------------------------------------
                Auto abort timer: inactive
                --------------------------------------------------------------------------------
            ''',
            'install add file image.bin activate commit prompt-level none': '''
                install_add_activate_commit: START Sat Apr 11 20:33:55 UTC 2015
                install_add: START Sat Apr 11 20:33:55 UTC 2015
                install_add: Adding IMG
                  [1]  R0 FAILED: System configuration has been modified. Please save configuration and resubmit command.
                  [1]  R1 FAILED: Install ISSU in progress. Abort the ISSU upgrade to proceed
                FAILED: add_activate_commit image.bin Sat Apr 11 20:33:55 UTC 2015
            ''',
            'show issu state detail': '''
                Current ISSU Status: Enabled
                Previous ISSU Operation: Failed
                =======================================================
                System Check                        Status
                -------------------------------------------------------
                Platform ISSU Support               Yes
                Standby Online                      Yes
                Autoboot Enabled                    Yes
                SSO Mode                            Yes
                Install Boot                        Yes
                Valid Boot Media                    Yes
                Operational Mode                    HA-STANDALONE
                =======================================================
                No ISSU operation is in progress
            ''',
            'install abort issu': '''
                install_abort: START Sat Apr 11 20:34:13 UTC 2015
                FAILED: install_abort : System configuration has been modified. Please save configuration and resubmit command.
            ''',
            'copy running-config startup-config': '''
                Destination filename [startup-config]?
                Building configuration...
                [OK]
            ''',
            'write memory': '''
                Building configuration...
                [OK]
            ''',
            'show platform software install-manager r0 operation current detail': '',
            'show platform software install-manager r0 operation history detail': '',
            'request platform software trace archive': '''
                Done with creation of the archive file: [bootflash:archive.tar.gz]
            ''',
            'dir': '''
                Directory of bootflash:/
            ''',
            'install commit': '''
                install_commit: START
                install_commit: SUCCESS
            ''',
        }

    @staticmethod
    def _mock_execute(get_output):
        """Raise like unicon execute when append_error_pattern matches."""
        def _execute(command, append_error_pattern=None, **kwargs):
            output = get_output(command)
            for pattern in append_error_pattern or []:
                if re.search(pattern, output):
                    raise SubCommandFailure(
                        'sub_command failure, patterns matched in the output:',
                        [pattern], 'service result', output)
            return output
        return Mock(side_effect=_execute)

    @patch('genie.libs.sdk.apis.iosxe.support.tech_support.datetime')
    def test_issu_abort_failure_does_not_clear_install_state(
            self, mock_datetime):
        mock_datetime.utcnow.return_value.strftime.return_value = '20250101T000000000'
        
        steps = Steps()

        self.device.execute = self._mock_execute(
            lambda command: self.data.get(command, ''))

        # Keep the unit test fast and deterministic by avoiding long dialog waits.
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps,
                device=self.device,
                images=[self.image],
                reload_wait=1,
            )

        self.assertEqual(Failed, steps.details[1].result)
        self.device.api.execute_clear_install_state.assert_not_called()

    def _set_stale_install_state(self):
        self.data['show issu state detail'] = '''
            Current ISSU Status: In Progress
            Previous ISSU Operation: Successful
            Install Boot                       No
            Valid Boot Media                   No
            Current state : Added state
            Auto abort timer: inactive
            Running image: tftp://223.255.254.254/image.bin
        '''
        self.data['show install package image.bin'] = '''
              Package: image.bin
                Size: 1220600805
              Internal package information:
                Name: rp_super
                Build: BLD_POLARIS_DEV_LATEST_20260929_003227
        '''
        self.data['show install summary'] = '''
            IMG   C    27.01.01.0.255252
            IMG   I    27.01.01.0.255544
            Auto abort timer: inactive
        '''

    def _connect_install_console(self, install_output):
        commands = self.data.copy()
        commands[self.install_command] = {
            'response': [
                install_output, 'SUCCESS: install_add_activate_commit'],
            'response_type': 'circular',
        }
        commands[''] = ''
        commands['enable'] = ''
        commands['config term'] = {'new_state': 'configure'}
        console = MockDeviceTcpWrapper(
            device_os='iosxe', hostname='router', port=0, state='execute',
            mock_data={
                'execute': {'prompt': 'router#', 'commands': commands},
                'configure': {'prompt': 'router(config)#',
                              'commands': {'end': {'new_state': 'execute'},
                                           'system mode insecure': ''}},
            })
        console.start()
        self.addCleanup(console.stop)
        connection = Connection(
            hostname='router', os='iosxe',
            start=['telnet 127.0.0.1 {}'.format(console.ports[0])],
            init_exec_commands=[], init_config_commands=[], log_stdout=False,
            settings={'GRACEFUL_DISCONNECT_WAIT_SEC': 0,
                      'POST_DISCONNECT_WAIT_SEC': 0})
        self.addCleanup(connection.disconnect)
        connection.connect(mit=True)
        return connection

    def _assert_stale_dialog_recovery(self, install_output):
        self.device.model = 'c9300'
        self._set_stale_install_state()
        connection = self._connect_install_console(install_output)
        events = []
        install_attempts = 0

        def _execute(command, **kwargs):
            nonlocal install_attempts
            events.append(command)
            if command.startswith('install add file'):
                install_attempts += 1
            if command == 'show issu state detail':
                self.assertRegex(
                    connection.spawn.match.match_output, r'router#\s*$')
            return connection.execute(command, **kwargs)

        self.device.execute = Mock(side_effect=_execute)
        self.device.expect = Mock(side_effect=connection.expect)
        self.device.reload = Mock()
        self.device.api.execute_clear_install_state = Mock(
            side_effect=lambda: events.append('clear install state') or True)
        self.device.api.execute_copy_run_to_start = Mock(
            side_effect=lambda: events.append('save config') or True)

        steps = Steps()
        self.cls.install_image(
            steps=steps, device=self.device, images=[self.image],
            install_timeout=10, reload_wait=1)

        self.assertEqual(Passed, steps.details[1].result)
        self.assertEqual(
            1, self.device.api.execute_clear_install_state.call_count)
        self.assertEqual(2, install_attempts)
        self.assertLess(
            events.index(self.install_command),
            events.index('show issu state detail'))
        self.assertLess(events.index('show issu state detail'),
                        events.index('clear install state'))
        self.assertLess(events.index('clear install state'),
                        events.index('save config'))
        install_positions = [index for index, event in enumerate(events)
                             if event.startswith('install add file')]
        self.assertLess(events.index('save config'),
                        install_positions[1])
        self.assertNotIn('install abort issu', events)

    def test_stale_tftp_issu_is_cleared_after_real_failure_footer(self):
        self._assert_stale_dialog_recovery(self.already_added_output)

    def test_stale_issu_dialog_reaches_prompt_before_recovery(self):
        self._assert_stale_dialog_recovery(
            '  [1] R0 FAILED: Install ISSU in progress. '
            'Abort the ISSU upgrade to proceed\n'
            'FAILED: install_add_activate_commit image.bin\n')

    def test_unrelated_failure_footer_still_fails_without_recovery(self):
        connection = self._connect_install_console(
            'FAILED: install_add_activate_commit : '
            'Abort xFSU install since requirement does not met\n')
        self.device.execute = Mock(wraps=connection.execute)
        steps = Steps()
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps, device=self.device, images=[self.image],
                install_timeout=10, reload_wait=1)

        self.assertEqual(Failed, steps.details[1].result)
        self.device.api.collect_install_log.assert_called_once_with(
            reconnect=True, reconnect_timeout=1)
        self.device.api.execute_clear_install_state.assert_not_called()
        self.device.configure.assert_not_called()
        self.assertNotIn(
            'show issu state detail',
            [call.args[0] for call in self.device.execute.call_args_list])

    def test_stale_issu_with_smus_is_not_cleared(self):
        self._set_stale_install_state()
        image_summary = self.data['show install summary']
        for state in ('C', 'U', 'D', 'I'):
            with self.subTest(smu_state=state):
                self.data['show install summary'] = (
                    image_summary +
                    '\nSMU {} cat9k.CSCtest.smu.bin\n'.format(state))
                self.device.execute = self._mock_execute(
                    lambda command: self.already_added_output
                    if command == self.install_command
                    else self.data.get(command, ''))
                steps = Steps()
                with self.assertRaises(TerminateStepSignal):
                    self.cls.install_image(
                        steps=steps, device=self.device, images=[self.image],
                        reload_wait=1)
                self.assertIn(
                    'SMUs are present', steps.details[1].result.reason)
                self.device.api.execute_clear_install_state.assert_not_called()
                self.device.api.execute_copy_run_to_start.assert_not_called()
                self.device.configure.assert_not_called()
                self.assertEqual(1, sum(
                    call.args[0] == self.install_command
                    for call in self.device.execute.call_args_list))

    def test_ticket_stale_issu_after_abort_is_cleared(self):
        # Ticket device: earlier ISSU aborted, standby activated, TFTP boot.
        self._set_stale_install_state()
        self.data['show issu state detail'] = '''
            Current ISSU Status: In Progress
            Previous ISSU Operation: Abort Successful
            Install Boot                        No
            Valid Boot Media                    No
            Current state : Standby activated state
            Auto abort timer: inactive
            Abort Reason: Failed Remote Restart
            Running image: tftp://11.15.10.165//short/image.bin
        '''
        self.data['show install summary'] = '''
            IMG   C    27.01.01.0.255252
            Auto abort timer: inactive
        '''
        issu_output = (
            '  [1] R0 FAILED: Install ISSU in progress. '
            'Abort the ISSU upgrade to proceed\n'
            'FAILED: add_activate_commit image.bin\n')
        package_command = 'show install package image.bin'
        # The build lookup is informational and must not block recovery.
        for package_error, build in (
                (None, 'BLD_POLARIS_DEV_LATEST_20260929_003227'),
                (UniconTimeoutError('lookup timed out'), 'None')):
            with self.subTest(package_error=package_error):
                attempts = []

                def _get_output(command):
                    if command == self.install_command:
                        attempts.append(command)
                        return (issu_output if len(attempts) == 1 else
                                'SUCCESS: install_add_activate_commit')
                    if command == package_command and package_error:
                        raise package_error
                    return self.data.get(command, '')

                self.device.execute = self._mock_execute(_get_output)
                self.device.reload = Mock()
                self.device.api.execute_clear_install_state = Mock(
                    return_value=True)
                steps = Steps()
                with self.assertLogs('genie.libs.clean.stages.iosxe.stages',
                                     level='WARNING') as logs:
                    self.cls.install_image(
                        steps=steps, device=self.device,
                        images=[self.image], reload_wait=1)
                self.assertEqual(Passed, steps.details[1].result)
                self.assertTrue(any(
                    'inactive: [], installing: ' + build in line
                    for line in logs.output))
                (
                    self.device.api.execute_clear_install_state
                ).assert_called_once()
                self.assertEqual(2, len(attempts))
                self.assertNotIn('install abort issu', [
                    call.args[0]
                    for call in self.device.execute.call_args_list])

    def test_active_tftp_issu_is_never_cleared(self):
        # Only a stuck Added/Standby activated state may be cleared.
        issu_output = (
            '  [1] R0 FAILED: Install ISSU in progress. '
            'Abort the ISSU upgrade to proceed\n'
            'FAILED: add_activate_commit image.bin\n')
        for field, replacement in (
                ('Current state : Added state',
                 'Current state : Activate commit state'),
                ('Install Boot                       No',
                 'Install Boot                       Yes'),
                ('Auto abort timer: inactive',
                 'Auto abort timer: 01:59:50')):
            with self.subTest(state=replacement):
                self._set_stale_install_state()
                self.data['show issu state detail'] = (
                    self.data['show issu state detail'].replace(
                        field, replacement))
                self.device.execute = self._mock_execute(
                    lambda command: issu_output
                    if command == self.install_command
                    else self.data.get(command, ''))
                steps = Steps()
                with self.assertRaises(TerminateStepSignal):
                    self.cls.install_image(
                        steps=steps, device=self.device, images=[self.image],
                        reload_wait=1)
                self.assertEqual(Failed, steps.details[1].result)
                (
                    self.device.api.execute_clear_install_state
                ).assert_not_called()
                self.device.configure.assert_not_called()

    def test_state_diagnostic_failure_preserves_install_error(self):
        self._set_stale_install_state()
        for command in ('show issu state detail', 'show install summary'):
            for error in (UniconTimeoutError('diagnostic timed out'),
                          ConnectionError('diagnostic connection dropped')):
                with self.subTest(command=command, error=type(error).__name__):
                    def _get_output(cmd):
                        if cmd == self.install_command:
                            return self.already_added_output
                        if cmd == command:
                            raise error
                        return self.data.get(cmd, '')

                    self.device.execute = self._mock_execute(_get_output)
                    steps = Steps()
                    with self.assertRaises(TerminateStepSignal):
                        self.cls.install_image(
                            steps=steps, device=self.device,
                            images=[self.image],
                            reload_wait=1)
                    reason = steps.details[1].result.reason
                    self.assertIn(command + ' also failed', reason)
                    self.assertIn(str(error), reason)
                    self.assertIn('Super package already added', reason)
                    self.assertIn(
                        'FAILED: install_add_activate_commit', reason)
                    self.assertEqual(Failed, steps.details[1].result)
                    (
                        self.device.api.execute_clear_install_state
                    ).assert_not_called()
                    (
                        self.device.api.execute_copy_run_to_start
                    ).assert_not_called()
                    self.device.configure.assert_not_called()

    @patch('genie.libs.clean.stages.iosxe.stages.Dialog')
    def test_empty_install_output_with_dialog_success_does_not_fail(self, dialog):
        steps = Steps()
        dialogs = []

        def _dialog(statements):
            mock_dialog = Mock()
            mock_dialog.statements = statements
            dialogs.append(mock_dialog)
            return mock_dialog

        dialog.side_effect = _dialog

        def _execute(cmd, **kwargs):
            if cmd == 'install add file image.bin activate commit prompt-level none':
                success_statement = next(
                    statement for statement in dialogs[0].statements
                    if 'SUCCESS:' in str(statement.pattern)
                    and getattr(statement, 'action', None)
                )
                success_statement.action(None, None)
                return ''
            return self.data.get(cmd, '')

        self.device.execute = Mock(side_effect=_execute)
        self.device.reload = Mock()

        self.cls.install_image(
            steps=steps,
            device=self.device,
            images=[self.image],
            reload_wait=1,
        )

        self.assertFalse(any(detail.result == Failed for detail in steps.details))
