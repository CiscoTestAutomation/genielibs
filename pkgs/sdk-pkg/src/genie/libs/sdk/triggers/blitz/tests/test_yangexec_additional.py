import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.sdk.triggers.blitz import yangexec
from genie.libs.sdk.triggers.blitz.verifiers import (
    GnmiDefaultVerifier,
    NetconfDefaultVerifier,
)


class FakeVerifier(object):
    edit_result = True
    get_result = True
    raise_on_get = False

    def __init__(self, device, returns, log, format=None,
                 steps=None, datastore=None, rpc_data=None):
        self.device = device
        self.returns = returns
        self.format = format or {}

    def edit_config_verify(self, *args, **kwargs):
        return self.edit_result

    def get_config_verify(self, *args, **kwargs):
        if self.raise_on_get:
            raise RuntimeError('verify failed')
        return self.get_result


class FakeRpcVerify(object):
    def __init__(self, *args, **kwargs):
        self.with_defaults = ['report-all']
        self.datastore = ['running', 'candidate']


class TestYangExecAdditional(unittest.TestCase):

    def setUp(self):
        FakeVerifier.edit_result = True
        FakeVerifier.get_result = True
        FakeVerifier.raise_on_get = False

    def test_capability_and_pause_helpers(self):
        self.assertTrue(yangexec.in_capabilities(
            ['cap-a', 'cap-b'], {'includes': 'cap-a'}))
        self.assertFalse(yangexec.in_capabilities(
            ['cap-a'], {'includes': ['missing']}))
        self.assertFalse(yangexec.in_capabilities(
            ['cap-a', 'cap-b'], {'excludes': 'cap-b'}))

        self.assertTrue(yangexec._included_excluded(
            {'module': 'enabled'}, {'module': 'enabled'}))
        self.assertFalse(yangexec._included_excluded(
            {'module': 'enabled'}, {'module': 'disabled'}))
        self.assertTrue(yangexec._included_excluded(
            {'module': ['a', 'b']}, {'module': ['a']}))
        self.assertFalse(yangexec._included_excluded(
            {'module': ['a']}, {'module': ['missing']}))

        self.assertEqual(yangexec._validate_pause(None), 0)
        self.assertEqual(yangexec._validate_pause(2), 2)
        self.assertEqual(yangexec._validate_pause('1.5'), 1.5)
        self.assertEqual(yangexec._validate_pause('bad'), 0)
        self.assertEqual(yangexec._validate_pause(object()), 0)

    def test_get_verifier_class_defaults_custom_and_invalid(self):
        self.assertIs(
            yangexec.get_verifier_class({}, 'netconf'),
            NetconfDefaultVerifier,
        )
        self.assertIs(
            yangexec.get_verifier_class({}, 'gnmi'),
            GnmiDefaultVerifier,
        )
        self.assertEqual(
            yangexec.get_verifier_class({
                'verifier': {
                    'class': (
                        'genie.libs.sdk.triggers.blitz.tests.scripts.'
                        'verifiers.CustomVerifier'
                    )
                }
            }, 'gnmi').__name__,
            'CustomVerifier',
        )
        self.assertIsNone(yangexec.get_verifier_class({
            'verifier': {'class': 'missing.module.Verifier'}
        }, 'gnmi'))
        self.assertIsNone(yangexec.get_verifier_class({
            'verifier': {'bad': 'format'}
        }, 'gnmi'))

    def test_run_netconf_capabilities_and_early_returns(self):
        device = SimpleNamespace(server_capabilities=['cap-a'])

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier):
            self.assertFalse(yangexec.run_netconf(
                'capabilities', device, None, {}, {}, [], format={}))
            self.assertTrue(yangexec.run_netconf(
                'capabilities',
                device,
                None,
                {},
                {},
                {'includes': ['cap-a']},
                format={},
            ))
            self.assertFalse(yangexec.run_netconf(
                'get', device, None, {}, {}, [], format={}))

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec, 'RpcVerify',
                             return_value=FakeRpcVerify()):
            self.assertTrue(yangexec.run_netconf(
                'edit-config',
                device,
                None,
                {},
                {'nodes': [{'edit-op': 'create', 'default': 'true'}]},
                [],
                format={},
            ))

        self.assertFalse(yangexec.run_netconf(
            'get',
            device,
            None,
            {},
            {'nodes': []},
            [],
            format={'sequence': True},
        ))

    def test_run_netconf_raw_invalid_timeout_and_unknown_operation(self):
        device = SimpleNamespace(server_capabilities=[], timeout=None)
        invalid_rpc = {'rpc': '<rpc><broken></rpc>'}

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier):
            self.assertFalse(yangexec.run_netconf(
                'rpc', device, None, {}, invalid_rpc, [], format={}))

        FakeVerifier.raise_on_get = True
        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec, 'get_datastore_state',
                             return_value=('running', {})), \
                patch.object(yangexec, 'gen_ncclient_rpc',
                             return_value=('unknown', {})), \
                patch.object(yangexec, 'netconf_send',
                             return_value=[('unknown', '<rpc-error/>')]):
            self.assertTrue(yangexec.run_netconf(
                'unknown',
                device,
                None,
                {'type': 'running', 'lock': False, 'retry': 0},
                {'nodes': []},
                [],
                format={'negative_test': True, 'timeout': 'bad'},
            ))
        self.assertIsNone(device.timeout)

    def test_run_netconf_success_paths_with_mocks(self):
        device = SimpleNamespace(server_capabilities=[], timeout=None)

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec, 'sleep') as sleep_mock, \
                patch.object(yangexec, 'get_datastore_state',
                             return_value=('candidate', {'candidate': []})), \
                patch.object(yangexec, 'gen_ncclient_rpc',
                             return_value=('edit-config',
                                           {'target': 'candidate'})), \
                patch.object(yangexec, 'netconf_send',
                             return_value=[('edit-config', '<ok/>')]):
            self.assertTrue(yangexec.run_netconf(
                'edit-config',
                device,
                None,
                {},
                {'nodes': []},
                [],
                format={'pause': '1', 'timeout': '2'},
            ))

        self.assertEqual(device.timeout, 2)
        self.assertEqual(sleep_mock.call_count, 2)

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec, 'get_datastore_state',
                             return_value=('running', {})), \
                patch.object(yangexec, 'netconf_send',
                             return_value=[('rpc', '<rpc-reply/>')]) as send_mock:
            self.assertTrue(yangexec.run_netconf(
                'rpc',
                device,
                None,
                {'type': 'running', 'lock': False, 'retry': 0},
                {'rpc': '<rpc><get/></rpc>'},
                [],
                format={},
            ))
        send_mock.assert_called_once()

    def test_run_gnmi_mocked_operation_branches(self):
        device = Mock()
        device.capabilities.return_value = ['cap-a']

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec.GnmiMessage, 'run_set',
                             return_value='set-response') as run_set:
            self.assertTrue(yangexec.run_gnmi(
                'edit-config',
                device,
                None,
                {},
                {'rpc': {'set': True}},
                [],
                format={},
            ))
        run_set.assert_called_once()

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec.GnmiMessage, 'run_get',
                             return_value='get-response') as run_get:
            self.assertTrue(yangexec.run_gnmi(
                'get',
                device,
                None,
                {},
                {'rpc': {'get': True}},
                [],
                format={'transaction_time': 3},
            ))
        run_get.assert_called_once()

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier), \
                patch.object(yangexec.GnmiMessage, 'run_subscribe',
                             return_value='thread') as run_subscribe:
            self.assertEqual(yangexec.run_gnmi(
                'subscribe',
                device,
                None,
                {},
                {'rpc': {'subscribe': True}},
                [],
                async_=True,
                format={},
            ), 'thread')
        run_subscribe.assert_called_once()

        with patch.object(yangexec, 'get_verifier_class',
                          return_value=FakeVerifier):
            self.assertFalse(yangexec.run_gnmi(
                'capabilities', device, None, {}, {}, [], format={}))
            self.assertTrue(yangexec.run_gnmi(
                'capabilities',
                device,
                None,
                {},
                {},
                {'includes': ['cap-a']},
                format={},
            ))
            self.assertTrue(yangexec.run_gnmi(
                'unsupported', device, None, {}, {}, [], format={}))
            self.assertFalse(yangexec.run_gnmi(
                'get', device, None, {}, {}, [], format={'sequence': True}))


if __name__ == '__main__':
    unittest.main()
