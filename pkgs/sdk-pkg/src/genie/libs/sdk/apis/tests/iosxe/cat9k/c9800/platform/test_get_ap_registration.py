import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import (
    get_ap_registration_evidence,
)


class TestApRegistrationEvidence(unittest.TestCase):

    def test_radio_mac_is_authoritative_when_ap_name_changes(self):
        device = Mock()
        device.execute.return_value = (
            'AP-NEW 0011.2233.4455 1 hour 2 minutes')
        device.parse.side_effect = [
            {
                'ap_name': {
                    'AP-NEW': {
                        'radio_mac': '0011.2233.4455',
                        'state': 'Registered',
                        'ap_ip_address': '192.0.2.20',
                    },
                },
            },
            {
                'base_mac': {
                    '0011.2233.4455': {
                        'ap_name': 'AP-NEW',
                        'status': 'Joined',
                    },
                },
            },
        ]

        evidence = get_ap_registration_evidence(
            device, '00:11:22:33:44:55', ap_name='AP-OLD')

        self.assertEqual(evidence['status'], 'confirmed')
        self.assertTrue(evidence['name_mismatch'])
        self.assertEqual(evidence['radio_mac'], '0011.2233.4455')

    def test_unregistered_state_remains_pending(self):
        device = Mock()
        device.execute.return_value = 'AP-1 0011.2233.4455 1 second'
        device.parse.side_effect = [
            {'ap_name': {
                'AP-1': {
                    'radio_mac': '0011.2233.4455',
                    'state': 'Not Registered',
                },
            }},
            {'base_mac': {}},
        ]

        evidence = get_ap_registration_evidence(
            device, '0011.2233.4455')

        self.assertEqual(evidence['status'], 'pending')

    def test_missing_join_evidence_remains_pending(self):
        device = Mock()
        device.execute.return_value = 'AP-1 0011.2233.4455 1 second'
        device.parse.side_effect = [
            {'ap_name': {
                'AP-1': {
                    'radio_mac': '0011.2233.4455',
                    'state': 'Registered',
                },
            }},
            {'base_mac': {}},
        ]

        evidence = get_ap_registration_evidence(
            device, '0011.2233.4455')

        self.assertEqual(evidence['status'], 'pending')

    def test_missing_uptime_evidence_remains_pending(self):
        device = Mock()
        device.execute.return_value = 'Number of APs: 0'
        device.parse.side_effect = [
            {'ap_name': {
                'AP-1': {
                    'radio_mac': '0011.2233.4455',
                    'state': 'Registered',
                },
            }},
            {'base_mac': {
                '0011.2233.4455': {
                    'ap_name': 'AP-1',
                    'status': 'Joined',
                },
            }},
        ]

        evidence = get_ap_registration_evidence(
            device, '0011.2233.4455')

        self.assertEqual(evidence['status'], 'pending')

    def test_empty_ap_summary_remains_pending(self):
        device = Mock()
        device.parse.side_effect = SchemaEmptyParserError({})

        evidence = get_ap_registration_evidence(
            device, '0011.2233.4455')

        self.assertIsNone(evidence)


if __name__ == '__main__':
    unittest.main()
