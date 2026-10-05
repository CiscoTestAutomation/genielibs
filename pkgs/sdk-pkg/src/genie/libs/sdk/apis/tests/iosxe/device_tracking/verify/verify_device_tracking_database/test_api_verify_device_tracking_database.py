from unittest import TestCase
from unittest.mock import Mock, patch
from genie.metaparser.util.exceptions import SchemaEmptyParserError
import genie.libs.sdk.apis.iosxe.device_tracking.verify as verify_module
from genie.libs.sdk.apis.iosxe.device_tracking.verify import \
    verify_device_tracking_database


class NoSleepTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations <= 2

    def sleep(self):
        pass


class TestVerifyDeviceTrackingDatabase(TestCase):
    def setUp(self):
        self.device = Mock()
        self.parsed_output = {
            'device': {
                '1': {
                    'interface': 'Gi0/1/0',
                    'network_layer_address': '50.0.0.9',
                    'link_layer_address': '000f.0001.0001',
                    'vlan_id': 50,
                    'state': 'REACHABLE',
                },
                '2': {
                    'interface': 'Gi0/1/0',
                    'network_layer_address': '50.0.0.8',
                    'link_layer_address': '000e.0001.0001',
                    'vlan_id': 50,
                    'state': 'REACHABLE',
                },
            }
        }
        self.device.parse.return_value = self.parsed_output

    def test_verify_device_tracking_database(self):
        with patch.object(verify_module, 'Timeout', NoSleepTimeout):
            result = verify_device_tracking_database(
                self.device,
                interface='GigabitEthernet0/1/0',
                network_layer_address='50.0.0.9',
                link_layer_address='000f.0001.0001',
                vlan_id=50,
                state='REACHABLE',
                max_time=1,
                interval_time=1
            )
            self.assertTrue(result)

            result = verify_device_tracking_database(
                self.device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.9',
                link_layer_address='000f.0001.0001',
                vlan_id=50,
                state='REACHABLE',
                max_time=1,
                interval_time=1
            )
            self.assertTrue(result)

            result = verify_device_tracking_database(
                self.device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.8',
                link_layer_address='000f.0001.0001',
                vlan_id=50,
                state='REACHABLE',
                max_time=1,
                interval_time=1
            )
            self.assertFalse(result)

            result = verify_device_tracking_database(
                self.device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.8',
                link_layer_address='000f.0001.0001',
                vlan_id=50,
                max_time=1,
                interval_time=1
            )
            self.assertFalse(result)

            result = verify_device_tracking_database(
                self.device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.9',
                link_layer_address='000f.0001.0001',
                vlan_id=30,
                max_time=1,
                interval_time=1
            )
            self.assertFalse(result)

            result = verify_device_tracking_database(
                self.device,
                interface='Gi0/1/0',
                unknown_parameter='50.0.0.9',
                max_time=1,
                interval_time=1
            )
            self.assertFalse(result)

        self.device.parse.assert_called_with('show device-tracking database')

    def test_verify_device_tracking_database_empty_parser_retry(self):
        device = Mock()
        device.parse.side_effect = [
            SchemaEmptyParserError('empty'),
            self.parsed_output
        ]

        with patch.object(verify_module, 'Timeout', NoSleepTimeout):
            result = verify_device_tracking_database(
                device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.9',
                link_layer_address='000f.0001.0001',
                vlan_id=50,
                state='REACHABLE',
                max_time=1,
                interval_time=1
            )

        self.assertTrue(result)
        self.assertEqual(device.parse.call_count, 2)

    def test_verify_device_tracking_database_missing_device_key(self):
        device = Mock()
        device.parse.return_value = {}

        with patch.object(verify_module, 'Timeout', NoSleepTimeout):
            result = verify_device_tracking_database(
                device,
                interface='Gi0/1/0',
                network_layer_address='50.0.0.9',
                max_time=1,
                interval_time=1
            )

        self.assertFalse(result)
        self.assertEqual(device.parse.call_count, 2)
