from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cloud_mgmt.verify import verify_cloud_mgmt_device_registration
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class TestVerifyCloudMgmtDeviceRegistration(TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_device'

    def test_device_registered_success(self):
        """Test successful device registration verification"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'cloud_id': 'Q4NS-HCWU-CZR2',
                        'pid': 'IE-3500-8U3X',
                        'serial_number': 'FCW2805Y304',
                        'status': 'Registered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_cloud_id='Q4NS-HCWU-CZR2',
            expected_registration_status='Registered',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_device_not_registered(self):
        """Test device not registered verification failure"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'cloud_id': 'XXXX-XXXX-XXXX',
                        'status': 'Unregistered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_registration_status='Registered',
            max_time=3,
            check_interval=1
        )
        self.assertFalse(result)

    def test_parser_empty_output(self):
        """Test handling of empty parser output"""
        self.device.parse.side_effect = SchemaEmptyParserError(None)

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_cloud_id='Q4NS-HCWU-CZR2',
            max_time=3,
            check_interval=1
        )
        self.assertFalse(result)

    def test_cloud_id_mismatch(self):
        """Test cloud ID mismatch"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'cloud_id': 'DIFFERENT-ID',
                        'status': 'Registered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_cloud_id='Q4NS-HCWU-CZR2',
            max_time=3,
            check_interval=1
        )
        self.assertFalse(result)

    def test_pid_verification_success(self):
        """Test successful PID verification"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'cloud_id': 'Q4NS-HCWU-CZR2',
                        'pid': 'IE-3500-8U3X',
                        'serial_number': 'FCW2805Y304',
                        'status': 'Registered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_pid='IE-3500-8U3X',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_serial_number_verification_success(self):
        """Test successful serial number verification"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'cloud_id': 'Q4NS-HCWU-CZR2',
                        'pid': 'IE-3500-8U3X',
                        'serial_number': 'FCW2805Y304',
                        'status': 'Registered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_serial_number='FCW2805Y304',
            max_time=3,
            check_interval=1
        )
        self.assertTrue(result)

    def test_values_from_different_devices_do_not_match(self):
        """Test all expected values must belong to one device record"""
        self.device.parse.return_value = {
            'cloud-mgmt_device_registration': {
                'devices': {
                    '1': {
                        'pid': 'IE-3500-8U3X',
                        'serial_number': 'FCW2805Y304',
                        'status': 'Registered'
                    },
                    '2': {
                        'cloud_id': 'Q4NS-HCWU-CZR2',
                        'pid': 'IE-3500-8P2S',
                        'serial_number': 'FCW2805Y305',
                        'status': 'Unregistered'
                    }
                }
            }
        }

        result = verify_cloud_mgmt_device_registration(
            self.device,
            expected_cloud_id='Q4NS-HCWU-CZR2',
            expected_pid='IE-3500-8U3X',
            expected_registration_status='Registered',
            max_time=1,
            check_interval=1
        )
        self.assertFalse(result)

    def test_no_expected_values_returns_false(self):
        """Test that omitting all expected values returns False without calling parse"""
        result = verify_cloud_mgmt_device_registration(self.device, max_time=1, check_interval=1)
        self.assertFalse(result)
        self.device.parse.assert_not_called()
