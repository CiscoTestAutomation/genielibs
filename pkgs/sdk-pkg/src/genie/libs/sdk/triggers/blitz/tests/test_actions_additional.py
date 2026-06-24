import tempfile
import unittest
from types import SimpleNamespace
from threading import Thread
from unittest.mock import Mock, patch

from pyats.results import Failed, Passed, Passx

from genie.libs.sdk.triggers.blitz import actions as actions_module
from genie.libs.sdk.triggers.blitz import markup as markup_module
from genie.libs.sdk.triggers.blitz.actions import (
    active_subscriptions,
    add_result_as_extra,
    api,
    check_yang_subscribe,
    yang,
    yang_snapshot,
    yang_snapshot_restore,
)


class Health(object):

    def _filter_and_save_action_output(self, section, ret_dict, save, output):
        return {'saved_vars': {'health_value': 'saved-health-value'}}


class LogLineCounterMock(object):

    def __init__(self, logfile):
        self.logfile = logfile

    def _get_lines(self, end_size):
        return 8

    def close(self):
        pass


class MultipartEncoderMock(object):

    content_type = 'multipart/form-data; boundary=test'

    def __init__(self, payload):
        self.payload = payload


class BadString(object):

    def __str__(self):
        raise RuntimeError('string conversion failed')


class ActionSteps(object):

    def __init__(self):
        self.result = Passed

    def start(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def failed(self, *args, **kwargs):
        self.result = Failed

    def passed(self, *args, **kwargs):
        self.result = Passed

    def passx(self, *args, **kwargs):
        self.result = Passx


class TestHealthResultDecorator(unittest.TestCase):

    def _runtime(self, notify=False):
        return SimpleNamespace(
            job=SimpleNamespace(uid='job-1'),
            testbed=SimpleNamespace(name='tb'),
            args=SimpleNamespace(
                health_notify_webex=notify,
                health_webex=False,
            ),
            env=SimpleNamespace(
                host=SimpleNamespace(name='host-1', distro='darwin'),
                prefix='/tmp/pyats',
                python=SimpleNamespace(version='3.10'),
            ),
            health_results={'health_data': []},
            health_webex={
                'msg': (
                    '{device_name} {health_name} {health_type} '
                    '{health_result} {health_value} {jobid} {host} '
                    '{host_os} {python_env} {pyats_ver} {python_ver} '
                    '{fullid} {testbed_name} {starttime} {stoptime}'
                ),
                'space': 'room-id',
                'email': None,
                'headers': {},
                'url': 'https://webex.example.test',
            },
        )

    def _section(self, logfile):
        client = Mock()
        client.get_section.return_value = {
            'fullid': 'job-1.health',
            'logfile': logfile,
            'logs': {
                'file': logfile,
                'begin': 10,
                'begin_lines': 2,
            },
        }
        client.get_section_ctx.return_value = SimpleNamespace(logfile=logfile)
        return SimpleNamespace(reporter=SimpleNamespace(client=client))

    def test_health_result_is_added_to_runtime_and_extra(self):
        @add_result_as_extra
        def health_action(*args, **kwargs):
            return {'health_data': {'cpu': 10}}

        runtime = self._runtime()
        section = self._section('/tmp/health.log')
        steps = SimpleNamespace(result=SimpleNamespace(name='passed'))

        with patch.object(actions_module, 'runtime', runtime), \
                patch.object(actions_module.os.path, 'getsize',
                             return_value=42), \
                patch.object(actions_module, 'LogLineCounter',
                             LogLineCounterMock):
            output = health_action(
                self=Health(),
                section=section,
                steps=steps,
                name='cpu_check',
                device=SimpleNamespace(name='PE1'),
            )

        self.assertEqual(output, {'health_data': {'cpu': 10}})
        self.assertEqual(len(runtime.health_results['health_data']), 1)
        self.assertEqual(
            runtime.health_results['health_data'][0]['health_output'],
            {'cpu': 10},
        )
        section.reporter.client.add_extra.assert_called_once()

    def test_health_result_sends_webex_notification_with_saved_value(self):
        @add_result_as_extra
        def health_action(*args, **kwargs):
            return {'value': 10}

        runtime = self._runtime(notify=True)
        steps = SimpleNamespace(result=SimpleNamespace(name='failed'))

        with tempfile.NamedTemporaryFile('w') as logfile:
            logfile.write('log text')
            logfile.flush()
            section = self._section(logfile.name)

            with patch.object(actions_module, 'runtime', runtime), \
                    patch.object(actions_module.os.path, 'getsize',
                                 return_value=42), \
                    patch.object(actions_module.os.path, 'isfile',
                                 return_value=False), \
                    patch.object(actions_module, 'LogLineCounter',
                                 LogLineCounterMock), \
                    patch.object(actions_module, 'MultipartEncoder',
                                 MultipartEncoderMock), \
                    patch.object(actions_module.requests, 'post',
                                 return_value=SimpleNamespace(
                                     status_code=200, text='ok')), \
                    patch.object(actions_module, 'version',
                                 return_value='1.0'):
                output = health_action(
                    self=Health(),
                    section=section,
                    steps=steps,
                    name='cpu_check',
                    save=[{'variable_name': 'health_value'}],
                    ret_dict={'saved_vars': {}},
                )

        self.assertEqual(output, {'value': 10})
        self.assertEqual(
            runtime.health_webex['headers']['Content-Type'],
            MultipartEncoderMock.content_type,
        )

    def test_health_result_without_output_skips_extra_handling(self):
        @add_result_as_extra
        def health_action(*args, **kwargs):
            return None

        runtime = self._runtime()
        section = self._section('/tmp/health.log')
        steps = SimpleNamespace(result=SimpleNamespace(name='passed'))

        with patch.object(actions_module, 'runtime', runtime):
            output = health_action(
                self=Health(),
                section=section,
                steps=steps,
                name='no_output',
            )

        self.assertIsNone(output)
        self.assertEqual(runtime.health_results['health_data'], [])
        section.reporter.client.add_extra.assert_not_called()


class TestYangActionsAdditional(unittest.TestCase):

    def setUp(self):
        active_subscriptions.clear()

    def tearDown(self):
        active_subscriptions.clear()

    def _blitz(self):
        return SimpleNamespace(parent=SimpleNamespace())

    def test_yang_invalid_protocol_fails_step(self):
        steps = ActionSteps()
        device = SimpleNamespace(name='PE1')

        output = yang(
            self=self._blitz(),
            device=device,
            steps=steps,
            section=SimpleNamespace(),
            name='yang',
            protocol='invalid',
            datastore='running',
            content={},
            operation='get',
        )

        self.assertIsNone(output)
        self.assertEqual(steps.result, Failed)

    def test_yang_missing_hostname_returns_without_failure(self):
        steps = ActionSteps()

        output = yang(
            self=self._blitz(),
            device=object(),
            steps=steps,
            section=SimpleNamespace(),
            name='yang',
            protocol='netconf',
            datastore='running',
            content={},
            operation='get',
        )

        self.assertIsNone(output)
        self.assertEqual(steps.result, Passed)

    def test_yang_registers_on_change_subscription_by_connection_device_name(self):
        steps = ActionSteps()
        subscription = Thread()
        subscription.sub_mode = 'ON_CHANGE'
        subscription.request = 'subscribe-request'
        connection = SimpleNamespace(device=SimpleNamespace(name='PE1'))
        device = SimpleNamespace(name='PE1', netconf=connection)
        blitz = self._blitz()
        blitz.parent.yang_snapshot = Mock()

        with patch.object(actions_module, 'run_netconf',
                          return_value={'raw': 'output'}), \
                patch.object(actions_module, 'yang_handler',
                             return_value=subscription):
            output = yang(
                self=blitz,
                device=device,
                steps=steps,
                section=SimpleNamespace(),
                name='yang',
                protocol='netconf',
                datastore='running',
                content={'nodes': []},
                operation='edit-config',
                connection='netconf',
            )

        self.assertIsNone(output)
        self.assertIs(active_subscriptions['PE1'], subscription)
        blitz.parent.yang_snapshot.register.assert_called_once_with(
            device, 'netconf', 'netconf', 'edit-config', {'nodes': []})

    def test_yang_result_status_changes_passed_step(self):
        steps = ActionSteps()
        device = SimpleNamespace(name='PE1')

        with patch.object(actions_module, 'run_gnmi',
                          return_value={'ok': True}), \
                patch.object(actions_module, 'yang_handler',
                             return_value={'ok': True}):
            output = yang(
                self=self._blitz(),
                device=device,
                steps=steps,
                section=SimpleNamespace(),
                name='yang',
                protocol='gnmi',
                datastore='running',
                content={},
                operation='get',
                result_status='passx',
            )

        self.assertEqual(output, {'ok': True})
        self.assertEqual(steps.result, Passx)

    def test_check_yang_subscribe_failure_marks_step_failed(self):
        steps = ActionSteps()
        subscription = Mock()
        subscription.request = 'request'
        subscription.result = False
        subscription.stopped.side_effect = [False, True]
        active_subscriptions['PE1'] = subscription

        with patch.object(actions_module.time, 'sleep'):
            check_yang_subscribe(
                self=self._blitz(),
                steps=steps,
                device=SimpleNamespace(name='PE1'),
            )

        self.assertEqual(steps.result, Failed)
        self.assertNotIn('PE1', active_subscriptions)

    def test_check_yang_subscribe_stopped_subscription_is_removed(self):
        steps = ActionSteps()
        subscription = Mock()
        subscription.request = 'request'
        subscription.stopped.return_value = True
        active_subscriptions['PE1'] = subscription

        check_yang_subscribe(
            self=self._blitz(),
            steps=steps,
            device=SimpleNamespace(name='PE1'),
        )

        subscription.stop.assert_called_once()
        self.assertEqual(steps.result, Passed)
        self.assertNotIn('PE1', active_subscriptions)

    def test_yang_snapshot_action_creates_snapshot_object_and_passes(self):
        steps = ActionSteps()
        snapshot = Mock()
        snapshot.snapshot.return_value = True
        blitz = self._blitz()

        with patch.object(actions_module, 'YangSnapshot',
                          return_value=snapshot):
            output = yang_snapshot(
                self=blitz,
                device=SimpleNamespace(name='PE1'),
                steps=steps,
                section=SimpleNamespace(),
                name='yang_snapshot',
            )

        self.assertTrue(output)
        self.assertEqual(steps.result, Passed)
        snapshot.snapshot.assert_called_once()

    def test_yang_snapshot_action_failure_marks_step_failed(self):
        steps = ActionSteps()
        snapshot = Mock()
        snapshot.snapshot.return_value = False
        blitz = self._blitz()
        blitz.parent.yang_snapshot = snapshot

        output = yang_snapshot(
            self=blitz,
            device=SimpleNamespace(name='PE1'),
            steps=steps,
            section=SimpleNamespace(),
            name='yang_snapshot',
        )

        self.assertFalse(output)
        self.assertEqual(steps.result, Failed)

    def test_yang_snapshot_restore_none_marks_step_passed(self):
        steps = ActionSteps()
        snapshot = Mock()
        snapshot.snapshot_restore.return_value = None
        blitz = self._blitz()
        blitz.parent.yang_snapshot = snapshot

        output = yang_snapshot_restore(
            self=blitz,
            device=SimpleNamespace(name='PE1'),
            steps=steps,
            section=SimpleNamespace(),
            name='yang_snapshot_restore',
        )

        self.assertIsNone(output)
        self.assertEqual(steps.result, Passed)

    def test_yang_snapshot_restore_failure_marks_step_failed(self):
        steps = ActionSteps()
        snapshot = Mock()
        snapshot.snapshot_restore.return_value = False
        blitz = self._blitz()
        blitz.parent.yang_snapshot = snapshot

        output = yang_snapshot_restore(
            self=blitz,
            device=SimpleNamespace(name='PE1'),
            steps=steps,
            section=SimpleNamespace(),
            name='yang_snapshot_restore',
        )

        self.assertFalse(output)
        self.assertEqual(steps.result, Failed)


class TestLoggingHardeningAdditional(unittest.TestCase):

    def test_api_debug_logging_does_not_fail_on_bad_output_string(self):
        bad_output = BadString()
        steps = ActionSteps()
        blitz = SimpleNamespace(parameters={})

        with patch.object(actions_module, 'api_handler',
                          return_value=bad_output):
            output = api(
                self=blitz,
                steps=steps,
                section=SimpleNamespace(),
                name='api',
                function='get_value',
            )

        self.assertIs(output, bad_output)
        self.assertEqual(steps.result, Passed)

    def test_load_saved_variable_debug_logging_does_not_fail(self):
        bad_output = BadString()
        blitz = SimpleNamespace(
            parameters={'save_variable_name': {'bad_output': bad_output}},
            parent=SimpleNamespace(parameters={}),
        )

        key, value = markup_module._load_saved_variable(
            blitz, SimpleNamespace(parent=blitz.parent),
            '%VARIABLES{bad_output}')

        self.assertIsNone(key)
        self.assertIs(value, bad_output)

    def test_save_variable_debug_logging_does_not_fail(self):
        bad_output = BadString()
        blitz = SimpleNamespace(
            parameters={},
            parent=SimpleNamespace(parameters={}),
        )

        markup_module.save_variable(
            blitz, SimpleNamespace(parent=blitz.parent),
            'bad_output', output=bad_output)

        self.assertIs(
            blitz.parameters['save_variable_name']['bad_output'],
            bad_output)
