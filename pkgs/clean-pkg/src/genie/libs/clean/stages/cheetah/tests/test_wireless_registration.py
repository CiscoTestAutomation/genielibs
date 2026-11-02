import unittest

from genie.libs.clean.wireless_registration import (
    WLC_READINESS,
    WirelessAPRegistration,
    normalize_radio_mac,
)


class FakeKIPC:

    def __init__(self):
        self.group_id = 'registration'
        self.coordinator = 'wlc'
        self.values = {}

    def publish(self, path, payload, **kwargs):
        if kwargs.get('if_unset') and path in self.values:
            return False
        if self.values.get(path, {}).get('_terminal'):
            return False
        self.values[path] = dict(payload)
        self.values[path]['_terminal'] = kwargs.get('terminal', False)
        return True

    def read(self, path, default=None):
        value = self.values.get(path)
        if value is None:
            return default
        return {key: value for key, value in value.items()
                if key != '_terminal'}

    def wait_for(self, path, predicate, timeout):
        value = self.read(path)
        if predicate(value):
            return {'status': 'matched', 'value': value}
        return {'status': 'timeout'}

    def snapshot(self, prefix=None):
        return {
            path: self.read(path)
            for path in self.values
            if prefix is None or path.startswith(prefix)
        }


class TestWirelessAPRegistration(unittest.TestCase):

    def setUp(self):
        self.kipc = FakeKIPC()
        self.registration = WirelessAPRegistration(
            self.kipc,
            [{'ap_id': 'ap-1', 'ap_name': 'AP-1',
              'radio_mac': '00:11:22:33:44:55'}],
        )

    def test_normalizes_radio_mac(self):
        self.assertEqual(
            normalize_radio_mac('0011.2233.4455'), '0011.2233.4455')
        self.assertEqual(
            self.registration.expected_aps['ap-1']['radio_mac'],
            '0011.2233.4455')

    def test_wlc_and_ap_state_transitions_are_durable(self):
        self.registration.signal_wlc_ready({'source': 'wlc'})
        self.assertEqual(
            self.registration.wait_for_wlc_ready(0)['status'], 'ready')

        self.registration.signal_ap_configured(
            'ap-1', 'AP-1', '0011.2233.4455')
        self.assertEqual(
            self.registration.wait_for_ap_configured('ap-1', 0)['status'],
            'configured')

        self.registration.signal_registration_confirmed(
            'ap-1', {'radio_mac': '0011.2233.4455', 'ap_name': 'AP-NEW'})
        self.assertTrue(self.registration.is_registration_confirmed('ap-1'))
        self.assertEqual(
            self.kipc.read(WLC_READINESS)['status'], 'ready')

    def test_registration_diagnostics_are_durable_and_separate(self):
        diagnostics = {'console_tail': 'AP output'}
        self.registration.signal_registration_diagnostics(
            'ap-1', diagnostics)

        self.assertEqual(
            self.kipc.read(
                'protocol/wireless/ap/ap-1/diagnostics'),
            diagnostics)


if __name__ == '__main__':
    unittest.main()
