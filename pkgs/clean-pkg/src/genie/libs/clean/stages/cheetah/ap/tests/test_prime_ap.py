import re
import unittest

from ipaddress import ip_interface
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, call, patch

from genie.libs.clean.stages.cheetah.ap.stages import PrimeAp
from unicon.core.errors import TimeoutError


class TestPrimeAp(unittest.TestCase):

    def test_default_wait_and_check_interval(self):
        self.assertEqual(PrimeAp.WLC_READINESS_TIMEOUT, 3600)
        self.assertEqual(PrimeAp.CHECK_INTERVAL, 30)

    def test_radio_mac_uses_parsed_radio_interface(self):
        device = Mock()
        device.parse.return_value = {
            'interface': {
                'Dot11Radio0': {
                    'radio_mac_address': 'C4:18:FC:FE:7E:A0',
                },
            },
        }

        self.assertEqual(
            PrimeAp._get_radio_mac(device), 'c418.fcfe.7ea0')
        device.parse.assert_called_once_with('show interfaces dot11radio 0')
        device.execute.assert_not_called()

    @patch.object(PrimeAp, '_monitor_registration')
    @patch.object(
        PrimeAp, '_get_controller_details',
        return_value=('controller', '192.0.2.10'))
    @patch.object(PrimeAp, '_get_registration')
    def test_readiness_wait_is_independent_of_registration_timeout(
            self, get_registration, get_controller_details, monitor):
        registration = MagicMock()
        registration.kipc.group_id = 'wireless-registration'
        registration.wait_for_wlc_ready.side_effect = [
            {'status': 'timeout'}, {'status': 'ready'}]
        get_registration.return_value = (
            registration, 'ap-1', 'AP-1', '0011.2233.4455')
        device = self._device(Mock())
        device.connected = True

        PrimeAp().prime_ap_to_controller(
            device,
            MagicMock(),
            coordination_group='wireless-registration',
            max_time=5,
            readiness_timeout=60,
            check_interval=30,
        )

        registration.wait_for_wlc_ready.assert_has_calls([call(30), call(30)])
        self.assertEqual(registration.wait_for_wlc_ready.call_count, 2)
        device.connect.assert_not_called()
        device.state_machine.detect_state.assert_called_once_with(
            device.spawn, device.context)
        device.enable.assert_called_once_with()
        monitor.assert_called_once()

    def test_coordinated_prime_does_not_fall_back_to_controller_connection(self):
        device = self._device(Mock())

        with self.assertRaisesRegex(
                RuntimeError, 'requires an injected KIPC context'):
            PrimeAp().prime_ap_to_controller(
                device,
                MagicMock(),
                controller_name='controller',
                controller_ip_address='192.0.2.10',
                coordination_group='wireless-registration',
            )

        device.connect.assert_not_called()
        device.testbed.devices['controller'].connect.assert_not_called()

    def test_coordinated_verify_does_not_connect_to_controller_without_kipc(self):
        device = self._device(Mock())
        steps = MagicMock()

        PrimeAp().verify_primed_ap(
            device,
            steps,
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            coordination_group='wireless-registration',
        )

        steps.start.return_value.__enter__.return_value.failed.assert_called_once()
        device.testbed.devices['controller'].connect.assert_not_called()

    def test_console_failure_evidence_is_bounded_and_redacted(self):
        device = SimpleNamespace(
            spawn=SimpleNamespace(
                buffer=('x' * 9000) + 'password: hidden\n',
                read_update_buffer=Mock(side_effect=RuntimeError('EOF')),
            ),
        )

        evidence = PrimeAp._get_console_failure_evidence(
            device, RuntimeError('device output'))

        self.assertEqual(evidence['error'], 'RuntimeError')
        self.assertLessEqual(len(evidence['console_tail']), 8192)
        self.assertNotIn('hidden', evidence['console_tail'])
        self.assertIn('password: <redacted>', evidence['console_tail'])

    @staticmethod
    def _device(events):
        state_machine = Mock()
        state_machine.current_state = 'disable'
        spawn = Mock()
        controller = SimpleNamespace(
            name='controller',
            model='c9800',
            connect=Mock(),
            api=SimpleNamespace(
                get_ap_state=Mock(return_value='Registered'),
            ),
        )

        return SimpleNamespace(
            name='ap',
            custom={},
            testbed=SimpleNamespace(devices={controller.name: controller}),
            context={},
            disconnect=Mock(side_effect=lambda: events.disconnect()),
            connect=Mock(side_effect=lambda **kwargs: events.connect(**kwargs)),
            enable=Mock(side_effect=lambda: events.enable()),
            parse=Mock(return_value={
                'interface': {
                    'Dot11Radio0': {
                        'radio_mac_address': '00:11:22:33:44:55',
                    },
                },
            }),
            spawn=spawn,
            state_machine=state_machine,
            api=SimpleNamespace(
                get_username_password=Mock(return_value=('cisco', 'cisco')),
                execute_prime_ap=Mock(
                    side_effect=lambda **kwargs: events.execute_prime_ap() or True
                ),
                verify_operation_state=Mock(return_value=True),
                verify_controller_name=Mock(return_value=True),
                verify_controller_ip=Mock(return_value=True),
            ),
        )

    def test_get_controller_details_from_single_wlc(self):
        controller = SimpleNamespace(
            name='controller',
            model='c9800',
            management={
                'wireless': {
                    'address': {
                        'ipv4': ip_interface('192.0.2.10/24'),
                    },
                },
            },
        )
        ap = SimpleNamespace(
            name='APAC4A.56BF.6984',
            platform='ap',
            custom={},
        )
        ap.testbed = SimpleNamespace(devices={
            ap.name: ap,
            controller.name: controller,
        })

        details = PrimeAp._get_controller_details(ap, None, None)

        self.assertEqual(details, ('controller', '192.0.2.10'))

    def test_get_controller_details_from_ap_custom_controller_name(self):
        controller = SimpleNamespace(
            name='controller',
            model='c9800',
            management={
                'wireless': {
                    'address': {
                        'ipv4': ip_interface('192.0.2.10/24'),
                    },
                },
            },
        )
        ap = SimpleNamespace(
            name='ap',
            platform='ap',
            custom={
                'controller_name': 'custom-controller',
                'controller_ip_address': '198.51.100.20',
            },
        )
        ap.testbed = SimpleNamespace(devices={
            ap.name: ap,
            controller.name: controller,
        })

        details = PrimeAp._get_controller_details(ap, None, None)

        self.assertEqual(details, ('custom-controller', '192.0.2.10'))

    def test_get_controller_details_from_multiple_aps(self):
        controller = SimpleNamespace(
            name='controller',
            model='c9800',
            management={
                'wireless': {
                    'address': {
                        'ipv4': ip_interface('192.0.2.10/24'),
                    },
                },
            },
        )
        ap = SimpleNamespace(name='ap', platform='ap', custom={})
        another_ap = SimpleNamespace(name='another-ap', platform='ap', custom={})
        ap.testbed = SimpleNamespace(devices={
            ap.name: ap,
            another_ap.name: another_ap,
            controller.name: controller,
        })

        details = PrimeAp._get_controller_details(ap, None, None)

        self.assertEqual(details, ('controller', '192.0.2.10'))

    def test_get_controller_details_from_named_controller_with_multiple_wlcs(self):
        controller_1 = SimpleNamespace(
            name='controller-1',
            model='c9800',
            management={
                'wireless': {
                    'address': {
                        'ipv4': ip_interface('192.0.2.10/24'),
                    },
                },
            },
        )
        controller_2 = SimpleNamespace(
            name='controller-2',
            model='c9800',
            management={
                'wireless': {
                    'address': {
                        'ipv4': ip_interface('192.0.2.20/24'),
                    },
                },
            },
        )
        ap = SimpleNamespace(name='ap', platform='ap', custom={})
        ap.testbed = SimpleNamespace(devices={
            ap.name: ap,
            controller_1.name: controller_1,
            controller_2.name: controller_2,
        })

        details = PrimeAp._get_controller_details(
            ap, 'controller-2', None)

        self.assertEqual(details, ('controller-2', '192.0.2.20'))

    def test_get_controller_details_from_management_address(self):
        controller = SimpleNamespace(
            name='controller',
            model='c9800',
            management={
                'address': {
                    'ipv4': ip_interface('192.0.2.11/24'),
                },
            },
        )
        ap = SimpleNamespace(name='ap', platform='ap', custom={})
        ap.testbed = SimpleNamespace(devices={
            ap.name: ap,
            controller.name: controller,
        })

        details = PrimeAp._get_controller_details(ap, None, None)

        self.assertEqual(details, ('controller', '192.0.2.11'))

    @patch('genie.libs.clean.stages.cheetah.ap.stages.Dialog.process')
    def test_login_is_processed_before_enable(self, process):
        events = Mock()
        device = self._device(events)
        steps = MagicMock()

        PrimeAp().prime_ap_to_controller(
            device,
            steps,
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            max_time=5,
            sleep_time=0,
            check_interval=1,
        )

        self.assertEqual(events.mock_calls, [
            call.connect(),
            call.execute_prime_ap(),
            call.enable(),
        ])
        device.api.get_username_password.assert_called_once_with(creds='default')
        process.assert_has_calls([
            call(device.spawn, timeout=5),
            call(device.spawn, timeout=5),
        ])
        self.assertEqual(process.call_count, 2)
        device.state_machine.detect_state.assert_called_once_with(
            device.spawn, device.context)
        device.connect.assert_called_once_with()
        controller = device.testbed.devices['controller']
        controller.connect.assert_not_called()
        controller.api.get_ap_state.assert_not_called()

    def test_login_dialog_uses_default_credentials(self):
        events = Mock()
        device = self._device(events)
        dialog = PrimeAp._get_login_dialog(device, 'controller')

        joined_statement, username_statement, password_statement = list(dialog)[:3]
        username_statement.action(device.spawn)
        password_statement.action(device.spawn)

        device.spawn.sendline.assert_has_calls([call('cisco'), call('cisco')])
        self.assertFalse(password_statement.loop_continue)

    def test_login_dialog_matches_target_controller(self):
        events = Mock()
        device = self._device(events)
        dialog = PrimeAp._get_login_dialog(device, 'controller.example')

        joined_statement = list(dialog)[0]

        self.assertTrue(
            re.match(
                joined_statement.pattern,
                'AP has joined controller controller.example'))
        self.assertFalse(
            re.match(
                joined_statement.pattern,
                'AP has joined controller other-controller'))
        self.assertTrue(joined_statement.loop_continue)
        joined_statement.action(device.spawn, **joined_statement.args)
        device.spawn.sendline.assert_called_once_with('')

    def test_reload_dialog_stops_on_ok(self):
        dialog = PrimeAp._get_reload_dialog()
        statement = list(dialog)[0]

        self.assertTrue(re.match(statement.pattern, '[  OK  ]'))
        self.assertFalse(statement.loop_continue)

    @patch('genie.libs.clean.stages.cheetah.ap.stages.Dialog.process')
    def test_reload_processes_login(self, process):
        events = Mock()
        device = self._device(events)

        PrimeAp().prime_ap_to_controller(
            device,
            MagicMock(),
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            max_time=5,
            sleep_time=0,
            check_interval=1,
        )

        process.assert_has_calls([
            call(device.spawn, timeout=5),
            call(device.spawn, timeout=5),
        ])
        self.assertEqual(process.call_count, 2)
        device.connect.assert_called_once_with()
        device.enable.assert_called_once_with()

    @patch('genie.libs.clean.stages.cheetah.ap.stages.Dialog.process')
    def test_no_reload_skips_login(self, process):
        events = Mock()
        device = self._device(events)
        process.side_effect = TimeoutError

        PrimeAp().prime_ap_to_controller(
            device,
            MagicMock(),
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            max_time=5,
            sleep_time=0,
            check_interval=1,
        )

        self.assertEqual(events.mock_calls, [
            call.connect(),
            call.execute_prime_ap(),
        ])
        process.assert_called_once_with(device.spawn, timeout=5)
        device.api.execute_prime_ap.assert_called_once()
        device.connect.assert_called_once_with()
        device.enable.assert_not_called()
        controller = device.testbed.devices['controller']
        controller.connect.assert_not_called()
        controller.api.get_ap_state.assert_not_called()

    @patch('genie.libs.clean.stages.cheetah.ap.stages.Dialog.process')
    def test_standalone_accepts_sleep_time_compatibility(self, process):
        events = Mock()
        device = self._device(events)
        process.side_effect = TimeoutError

        PrimeAp().prime_ap_to_controller(
            device,
            MagicMock(),
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            max_time=5,
            sleep_time=7,
        )

    def test_verify_primed_ap_uses_controller_state(self):
        events = Mock()
        device = self._device(events)

        PrimeAp().verify_primed_ap(
            device,
            MagicMock(),
            controller_name='controller',
            controller_ip_address='192.0.2.10',
        )

        controller = device.testbed.devices['controller']
        controller.connect.assert_called_once_with()
        controller.api.get_ap_state.assert_called_once_with(ap_name='ap')
        device.api.verify_operation_state.assert_called_once_with(
            operation_state='UP')
        device.api.verify_controller_name.assert_called_once_with(
            controller_name='controller')
        device.api.verify_controller_ip.assert_called_once_with(
            controller_ip_address='192.0.2.10')

    @patch('genie.libs.clean.stages.cheetah.ap.stages.Timeout')
    def test_standalone_verification_retries_until_success(self, timeout_cls):
        timeout = timeout_cls.return_value
        timeout.iterate.side_effect = [True, True]
        device = self._device(Mock())
        device.api.verify_operation_state.side_effect = [False, True]
        device.api.verify_controller_name.side_effect = [False, True]
        device.api.verify_controller_ip.side_effect = [False, True]

        PrimeAp().verify_primed_ap(
            device,
            MagicMock(),
            controller_name='controller',
            controller_ip_address='192.0.2.10',
            max_time=60,
            check_interval=5,
        )

        timeout_cls.assert_called_once_with(60, 5)
        self.assertEqual(device.api.verify_operation_state.call_count, 2)
        self.assertEqual(device.api.verify_controller_name.call_count, 2)
        self.assertEqual(device.api.verify_controller_ip.call_count, 2)
        timeout.sleep.assert_called_once_with()

    @patch.object(PrimeAp, '_get_registration')
    def test_verify_primed_ap_resolves_controller_alias(
            self, get_registration):
        events = Mock()
        device = self._device(events)
        controller = device.testbed.devices.pop('controller')
        controller.name = 'vidya-vwlc'
        controller.alias = 'wlc'
        device.testbed.devices[controller.name] = controller

        registration = Mock()
        registration.is_registration_confirmed.return_value = True
        get_registration.return_value = (
            registration, 'ap-1', 'ap', '0011.2233.4455')

        PrimeAp().verify_primed_ap(
            device,
            MagicMock(),
            controller_name='wlc',
            controller_ip_address='192.0.2.10',
            coordination_group='wlc-registration',
            ap_id='ap-1',
            ap_name='ap',
            radio_mac='0011.2233.4455',
        )

        device.api.verify_controller_name.assert_called_once_with(
            controller_name='vidya-vwlc')
        controller.connect.assert_not_called()

    def test_reload_dialog_matches_ansi_colored_ok(self):
        dialog = PrimeAp._get_reload_dialog()
        statement = list(dialog)[0]

        self.assertTrue(
            re.match(statement.pattern, '[\x1b[32m  OK  \x1b[0m] Stopped capwapd.'))
