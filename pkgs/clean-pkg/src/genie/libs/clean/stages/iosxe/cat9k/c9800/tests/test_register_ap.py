import copy
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

from genie.libs.clean.stages.iosxe.cat9k.c9800.stages import RegisterAp


class FakeKIPC:

    def __init__(self, participants):
        self.group_id = 'registration'
        self.coordinator = participants[0]
        self.participants = participants
        self.values = {}
        self.on_publish = None

    def publish(self, path, payload, **kwargs):
        if kwargs.get('if_unset') and path in self.values:
            return False
        self.values[path] = copy.deepcopy(payload)
        if self.on_publish:
            self.on_publish(path, payload)
        return True

    def read(self, path, default=None):
        return copy.deepcopy(self.values.get(path, default))

    def snapshot(self, prefix=None):
        return {
            path: copy.deepcopy(value)
            for path, value in self.values.items()
            if prefix is None or path.startswith(prefix)
        }


class TestRegisterAp(unittest.TestCase):

    @staticmethod
    def _steps():
        steps = MagicMock()
        steps.start.return_value.__enter__.return_value = MagicMock()
        return steps

    @staticmethod
    def _device(context):
        aps = {
            'ap-1': SimpleNamespace(name='AP-1', alias='ap-1'),
            'ap-2': SimpleNamespace(name='AP-2', alias='ap-2'),
        }
        wlc = SimpleNamespace(
            name='wlc',
            alias='wlc',
            testbed=SimpleNamespace(devices=aps),
        )
        wlc.api = SimpleNamespace(
            get_ap_registration_evidence=Mock(
                return_value={'status': 'confirmed'}),
            get_ap_registration_diagnostics=Mock(return_value={}),
        )
        return wlc

    def test_alias_contract_uses_learned_radio_mac(self):
        context = FakeKIPC(['wlc', 'ap-1'])

        def publish_ap_configured(path, payload):
            if path == 'protocol/wireless/wlc/readiness':
                context.values['protocol/wireless/ap/ap-1/status'] = {
                    'status': 'configured',
                    'ap_name': 'AP-1',
                    'radio_mac': '0011.2233.4455',
                }

        context.on_publish = publish_ap_configured
        device = self._device(context)
        RegisterAp().register_ap(
            device, self._steps(), expected_aps=['ap-1'],
            coordination_context=context, registration_timeout=1,
            check_interval=1)

        device.api.get_ap_registration_evidence.assert_called_once_with(
            radio_mac='0011.2233.4455', ap_name='AP-1')

    def test_missing_radio_mac_fails_without_wlc_evidence(self):
        context = FakeKIPC(['wlc', 'ap-1'])

        def publish_ap_configured(path, payload):
            if path == 'protocol/wireless/wlc/readiness':
                context.values['protocol/wireless/ap/ap-1/status'] = {
                    'status': 'configured',
                    'ap_name': 'AP-1',
                }

        context.on_publish = publish_ap_configured
        device = self._device(context)
        RegisterAp().register_ap(
            device, self._steps(), expected_aps=['ap-1'],
            coordination_context=context, registration_timeout=1,
            check_interval=1)

        device.api.get_ap_registration_evidence.assert_not_called()
        self.assertEqual(
            context.read('protocol/wireless/ap/ap-1/status')['status'],
            'failed')

    def test_initialization_failure_publishes_wlc_failure(self):
        context = FakeKIPC(['wlc', 'ap-1'])
        device = self._device(context)

        RegisterAp().register_ap(
            device, self._steps(), expected_aps='invalid',
            coordination_context=context, registration_timeout=1,
            check_interval=1)

        self.assertEqual(
            context.read('protocol/wireless/wlc/readiness')['status'],
            'failed')

    def test_worker_exit_is_reported_as_registration_failure(self):
        context = FakeKIPC(['wlc', 'ap-1'])

        def publish_ap_configured(path, payload):
            if path == 'protocol/wireless/wlc/readiness':
                context.values['participant/ap-1/lifecycle'] = {
                    'status': 'exited',
                }

        context.on_publish = publish_ap_configured
        device = self._device(context)
        RegisterAp().register_ap(
            device, self._steps(), expected_aps=['ap-1'],
            coordination_context=context, registration_timeout=1,
            check_interval=1)

        self.assertEqual(
            context.read('protocol/wireless/ap/ap-1/status')['status'],
            'failed')
        device.api.get_ap_registration_diagnostics.assert_called_once_with(
            radio_mac=None)

    def test_multiple_aps_can_complete_and_fail_independently(self):
        context = FakeKIPC(['wlc', 'ap-1', 'ap-2'])

        def publish_ap_configured(path, payload):
            if path == 'protocol/wireless/wlc/readiness':
                context.values.update({
                    'protocol/wireless/ap/ap-1/status': {
                        'status': 'configured',
                        'ap_name': 'AP-1',
                        'radio_mac': '0011.2233.4455',
                    },
                    'protocol/wireless/ap/ap-2/status': {
                        'status': 'configured',
                        'ap_name': 'AP-2',
                        'radio_mac': '0011.2233.4466',
                    },
                })

        context.on_publish = publish_ap_configured
        device = self._device(context)
        device.api.get_ap_registration_evidence.side_effect = (
            lambda radio_mac, ap_name: {
                'status': 'confirmed'
                if radio_mac == '0011.2233.4455' else 'pending',
            })
        RegisterAp().register_ap(
            device, self._steps(), expected_aps=['ap-1', 'ap-2'],
            coordination_context=context, registration_timeout=0.01,
            check_interval=0)

        self.assertEqual(
            context.read('protocol/wireless/ap/ap-1/status')['status'],
            'confirmed')
        self.assertEqual(
            context.read('protocol/wireless/ap/ap-2/status')['status'],
            'failed')
        device.api.get_ap_registration_diagnostics.assert_any_call(
            radio_mac='0011.2233.4466')

    def test_failed_ap_finalizes_other_pending_aps(self):
        context = FakeKIPC(['wlc', 'ap-1', 'ap-2'])

        def publish_ap_configured(path, payload):
            if path == 'protocol/wireless/wlc/readiness':
                context.values.update({
                    'protocol/wireless/ap/ap-1/status': {
                        'status': 'failed',
                        'reason': 'CAPWAP failed',
                    },
                    'protocol/wireless/ap/ap-2/status': {
                        'status': 'configured',
                        'ap_name': 'AP-2',
                        'radio_mac': '0011.2233.4466',
                    },
                })

        context.on_publish = publish_ap_configured
        device = self._device(context)
        device.api.get_ap_registration_evidence.return_value = {
            'status': 'pending',
        }
        RegisterAp().register_ap(
            device, self._steps(), expected_aps=['ap-1', 'ap-2'],
            coordination_context=context, registration_timeout=1,
            check_interval=1)

        self.assertEqual(
            context.read('protocol/wireless/ap/ap-1/status')['status'],
            'failed')
        self.assertEqual(
            context.read('protocol/wireless/ap/ap-2/status')['status'],
            'failed')
        device.api.get_ap_registration_diagnostics.assert_any_call(
            radio_mac='0011.2233.4466')


if __name__ == '__main__':
    unittest.main()
