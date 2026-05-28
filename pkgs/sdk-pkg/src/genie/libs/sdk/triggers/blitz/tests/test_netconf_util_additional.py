import unittest
from itertools import count
from types import SimpleNamespace
from unittest.mock import Mock, patch

from genie.libs.sdk.triggers.blitz import netconf_util
from genie.libs.sdk.triggers.blitz.netconf_util import (
    NetconfSubscription,
    NetconfSubscriptionOnce,
    NetconfSubscriptionPoll,
    NetconfSubscriptionStream,
    gen_ncclient_rpc,
    get_datastore_state,
    netconf_send,
    try_lock,
)


SUBSCRIBE_OK = """<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <subscription-id> 101 </subscription-id>
</rpc-reply>"""

SUBSCRIBE_ERROR = """
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <rpc-error><error-tag>invalid-value</error-tag></rpc-error>
</rpc-reply>"""


class RpcError(object):
    def __init__(self, tag='operation-failed', message='failed'):
        self.tag = tag
        self.message = message


class RpcReply(object):
    def __init__(self, ok=True, text='<ok/>', tag='operation-failed'):
        self.ok = ok
        self.error = RpcError(tag)
        self.errors = [self.error]
        self.xml = '<rpc-error/>'
        self.text = text

    def __str__(self):
        return self.text


class FakeNetconfDevice(object):
    def __init__(self):
        self.connected = False
        self.lock_replies = []
        self.lock_targets = []
        self.unlock_targets = []
        self.edit_config_reply = RpcReply()
        self.commit_replies = []
        self.discard_reply = RpcReply(text='<discarded/>')
        self.get_config_reply = RpcReply(text='<get-config/>')
        self.get_reply = RpcReply(text='<get/>')
        self.dispatch_reply = RpcReply(text='<subscribe/>')
        self.request_reply = '<rpc-reply/>'

    def connect(self):
        self.connected = True

    def lock(self, target):
        self.lock_targets.append(target)
        if self.lock_replies:
            return self.lock_replies.pop(0)
        return RpcReply()

    def unlock(self, target=None):
        self.unlock_targets.append(target)

    def edit_config(self, **kwargs):
        self.edit_config_kwargs = kwargs
        return self.edit_config_reply

    def commit(self):
        if self.commit_replies:
            return self.commit_replies.pop(0)
        return RpcReply(text='<commit/>')

    def discard_changes(self):
        return self.discard_reply

    def get_config(self, **kwargs):
        self.get_config_kwargs = kwargs
        return self.get_config_reply

    def get(self, **kwargs):
        self.get_kwargs = kwargs
        return self.get_reply

    def dispatch(self, **kwargs):
        self.dispatch_kwargs = kwargs
        return self.dispatch_reply

    def request(self, rpc):
        self.request_rpc = rpc
        return self.request_reply


class TestNetconfUtilAdditional(unittest.TestCase):

    def setUp(self):
        NetconfSubscription.subscription_queue = {}

    def test_subscribe_response_helpers_and_modes(self):
        payload = [('subscribe', SUBSCRIBE_OK)]
        sub = NetconfSubscription(
            device=None,
            payload=payload,
            verifier=Mock(),
            stream_max=1,
        )

        self.assertEqual(sub.subscription_id, '101')
        self.assertTrue(NetconfSubscription.validate_subscribe_response(payload))
        self.assertFalse(
            NetconfSubscription.validate_subscribe_response(
                [('subscribe', SUBSCRIBE_ERROR)]
            )
        )
        self.assertFalse(
            NetconfSubscription.validate_subscribe_response([('subscribe', '')])
        )
        self.assertEqual(sub._trim_xml_header(SUBSCRIBE_OK).splitlines()[0],
                         '<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">')

        with patch.object(NetconfSubscriptionOnce, 'start') as start_mock:
            subscribe_thread = NetconfSubscription.run_subscribe(
                None, payload, verifier=Mock(), stream_max=1)
        self.assertIsInstance(subscribe_thread, NetconfSubscriptionOnce)
        self.assertIn('101', NetconfSubscription.subscription_queue)
        start_mock.assert_called_once()

        self.assertFalse(
            NetconfSubscription.run_subscribe(
                None, payload, request_mode='unknown', verifier=Mock())
        )
        self.assertFalse(
            NetconfSubscription.run_subscribe(
                None, [('subscribe', SUBSCRIBE_ERROR)], verifier=Mock())
        )

    def test_subscription_stream_once_and_poll_process_notifications(self):
        notification = SimpleNamespace(notification_xml=SUBSCRIBE_OK)
        device = Mock()
        device.take_notification.return_value = notification
        verifier = Mock()
        verifier.subscribe_verify.return_value = True

        stream = NetconfSubscriptionStream(
            device,
            [('subscribe', SUBSCRIBE_OK)],
            verifier=verifier,
            stream_max=1,
        )
        with patch.object(netconf_util.time, 'time',
                          side_effect=count(0, 2)):
            stream.run()
        self.assertTrue(stream.result)
        verifier.subscribe_verify.assert_called_with(SUBSCRIBE_OK)

        verifier.reset_mock()
        once = NetconfSubscriptionOnce(
            device,
            [('subscribe', SUBSCRIBE_OK)],
            verifier=verifier,
            stream_max=1,
        )
        with patch.object(netconf_util.time, 'time',
                          side_effect=count(0, 2)):
            once.run()
        self.assertTrue(once.result)
        verifier.subscribe_verify.assert_called_with(SUBSCRIBE_OK)

        poll = NetconfSubscriptionPoll(
            device,
            [('subscribe', SUBSCRIBE_OK)],
            verifier=verifier,
            stream_max=1,
            sample_interval=0,
            rpc='<establish-subscription/>',
        )
        with patch.object(netconf_util.time, 'time',
                          side_effect=count(0, 2)), \
                patch.object(netconf_util.time, 'sleep') as sleep_mock, \
                patch.object(netconf_util, 'netconf_send',
                             return_value=[('rpc', SUBSCRIBE_OK)]) as send_mock:
            poll.run()
        self.assertEqual(poll.subscription_id, '101')
        sleep_mock.assert_called_once_with(0)
        send_mock.assert_called_once()

    def test_gen_ncclient_rpc_operations(self):
        self.assertIsNone(gen_ncclient_rpc({}))

        op, kwargs = gen_ncclient_rpc({
            'operation': 'edit-config',
            'datastore': 'candidate',
            'nodes': [],
        })
        self.assertEqual(op, 'edit-config')
        self.assertEqual(kwargs['target'], 'candidate')

        op, kwargs = gen_ncclient_rpc({
            'operation': 'get-config',
            'datastore': 'running',
            'with-defaults': 'report-all',
            'nodes': [],
        })
        self.assertEqual(op, 'get-config')
        self.assertEqual(kwargs['source'], 'running')
        self.assertEqual(kwargs['with_defaults'], 'report-all')

        op, kwargs = gen_ncclient_rpc({
            'operation': 'get',
            'with-defaults': 'trim',
            'nodes': [],
        })
        self.assertEqual(op, 'get')
        self.assertEqual(kwargs['with_defaults'], 'trim')

        for operation in ('action', 'get-data', 'edit-data'):
            op, kwargs = gen_ncclient_rpc({'operation': operation, 'nodes': []})
            self.assertEqual(op, operation)
            self.assertIn('rpc_command', kwargs)

        op, kwargs = gen_ncclient_rpc({'operation': 'unsupported', 'nodes': []})
        self.assertEqual(op, 'unsupported')
        self.assertEqual(kwargs, {})

    def test_get_datastore_state(self):
        device = SimpleNamespace(
            datastore=['running', 'candidate', 'startup', 'intent', 'operational']
        )
        target, state = get_datastore_state('', device)
        self.assertEqual(target, 'candidate')
        self.assertIn('lock_running', state['candidate'])
        self.assertEqual(state['startup'], ['lock_ok'])
        self.assertEqual(state['intent'], [])
        self.assertEqual(state['operational'], [])

        target, state = get_datastore_state('', SimpleNamespace(datastore=[]))
        self.assertEqual(target, 'running')
        self.assertEqual(state, {})

    def test_try_lock_success_retry_non_retry_and_timeout(self):
        device = FakeNetconfDevice()
        self.assertTrue(try_lock(device, 'candidate', timer=1))
        self.assertEqual(device.lock_targets, ['candidate'])

        device = FakeNetconfDevice()
        device.lock_replies = [
            RpcReply(ok=False, tag='lock-denied'),
            RpcReply(ok=True),
        ]
        with patch.object(netconf_util.time, 'sleep') as sleep_mock:
            self.assertTrue(try_lock(device, 'running', timer=2, sleeptime=0))
        sleep_mock.assert_called_once_with(0)

        device = FakeNetconfDevice()
        device.lock_replies = [RpcReply(ok=False, tag='access-denied')]
        self.assertFalse(try_lock(device, 'running', timer=3, sleeptime=0))

        device = FakeNetconfDevice()
        device.lock_replies = [
            RpcReply(ok=False, tag='in-use'),
            RpcReply(ok=False, tag='in-use'),
        ]
        with patch.object(netconf_util.time, 'sleep'):
            self.assertFalse(try_lock(device, 'running', timer=2, sleeptime=0))

    def test_netconf_send_edit_config_commit_and_unlock_paths(self):
        device = FakeNetconfDevice()
        ds_state = {'candidate': ['commit', 'lock_ok', 'lock_running']}
        result = netconf_send(
            device,
            [('edit-config', {'target': 'candidate', 'config': '<config/>'})],
            ds_state,
            lock=True,
            lock_retry=1,
        )

        self.assertEqual(result, [('edit-config', '<ok/>')])
        self.assertTrue(device.connected)
        self.assertEqual(device.lock_targets, ['candidate', 'running'])
        self.assertEqual(device.unlock_targets, ['running', 'candidate'])

        device = FakeNetconfDevice()
        device.commit_replies = [
            RpcReply(ok=False, text='<commit-failed/>', tag='lock-denied'),
            RpcReply(ok=True, text='<commit-ok/>'),
        ]
        result = netconf_send(
            device,
            [('edit-config', {'target': 'candidate', 'config': '<config/>'})],
            {'candidate': ['commit', 'lock_ok']},
            lock=True,
            lock_retry=1,
        )

        self.assertEqual(result, [('edit-config', '<ok/>')])
        self.assertEqual(device.lock_targets, ['candidate', 'running'])
        self.assertEqual(device.unlock_targets, ['running', 'candidate'])

    def test_netconf_send_other_operations_and_errors(self):
        device = FakeNetconfDevice()
        device.commit_replies = [
            RpcReply(ok=False, text='<commit-failed/>', tag='operation-failed')
        ]

        result = netconf_send(
            device,
            [
                ('commit', {}),
                ('get-config', {'source': 'running'}),
                ('get', {}),
                ('subscribe', {'rpc_command': '<rpc/>'}),
            ],
            {},
            lock=False,
        )

        self.assertEqual(result[0], ('commit', '<rpc-error/>'))
        self.assertEqual(result[1:], [
            ('get-config', '<get-config/>'),
            ('get', '<get/>'),
            ('subscribe', '<subscribe/>'),
        ])

        device = FakeNetconfDevice()
        device.commit_replies = [
            RpcReply(ok=False, text='<commit-failed/>', tag='operation-failed')
        ]
        result = netconf_send(
            device,
            [('rpc', {'rpc': '<edit-config><candidate/></edit-config>'})],
            {},
            lock=True,
            lock_retry=1,
        )
        self.assertEqual(result, [('rpc', '<rpc-reply/>')])
        self.assertEqual(device.lock_targets, ['candidate'])
        self.assertEqual(device.unlock_targets, ['candidate'])

        device = FakeNetconfDevice()
        device.edit_config = Mock(side_effect=RuntimeError('boom'))
        result = netconf_send(
            device,
            [('edit-config', {'target': 'running', 'config': '<config/>'})],
            {'running': ['lock_ok']},
            lock=True,
            lock_retry=1,
        )
        self.assertEqual(result[0][0], 'traceback')
        self.assertIn('boom', result[0][1])
        self.assertEqual(device.unlock_targets, ['running'])


if __name__ == '__main__':
    unittest.main()
