import unittest
from unittest.mock import Mock

from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.libs.sdk.apis.iosxe.cat9k.c9200.rommon.get import get_recovery_details


class TestGetRecoveryDetails(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = "Mock-C9200"
        self.device.clean = {
            "device_recovery": {
                "tftp_boot": {
                    "gateway": "1.1.1.0",
                    "image": ["file/base_image.bin"],
                    "ip_address": "1.1.1.1",
                    "subnet_mask": "255.255.255.0",
                    "tftp_server": "1.1.2.1"
                }
            },
            "images": []
        }
        self.device.parse = Mock(return_value={
            "dir": {
                "drec0:": {
                    "files": {
                        "system_image.bin": {
                            "permissions": "-rwxrwxrwx",
                            "size": "490586943"
                        }
                    }
                }
            }
        })

    def test_get_recovery_details(self):
        """drec0: has golden image."""
        result = get_recovery_details(self.device)
        expected = {
            'golden_image': ['drec0:system_image.bin'],
            'tftp_boot': {
                "gateway": "1.1.1.0",
                "image": ["file/base_image.bin"],
                "ip_address": "1.1.1.1",
                "subnet_mask": "255.255.255.0",
                "tftp_server": "1.1.2.1"
            },
            'tftp_image': ['file/base_image.bin'],
        }
        self.assertEqual(result, expected)

    def test_get_recovery_details_empty_drec0(self):
        """ drec0 empty fall back to TFTP."""
        self.device.parse.side_effect = SchemaEmptyParserError(
            None, 'dir drec0:')
        result = get_recovery_details(self.device)
        expected = {
            'golden_image': None,
            'tftp_boot': {
                "gateway": "1.1.1.0",
                "image": ["file/base_image.bin"],
                "ip_address": "1.1.1.1",
                "subnet_mask": "255.255.255.0",
                "tftp_server": "1.1.2.1"
            },
            'tftp_image': ['file/base_image.bin'],
        }
        self.assertEqual(result, expected)

    def test_get_recovery_details_no_recovery_options(self):
        """ No golden image or TFTP image available should raise Exception."""
        self.device.parse.side_effect = SchemaEmptyParserError(
            None, 'dir drec0:')
        self.device.clean = {"device_recovery": {}}
        with self.assertRaises(Exception) as ctx:
            get_recovery_details(self.device)
        self.assertIn('No golden image or TFTP image', str(ctx.exception))

    def test_get_recovery_details_with_tftp_boot_arg(self):
        """When tftp_boot is passed as argument, use it over clean config."""
        self.device.parse.side_effect = SchemaEmptyParserError(
            None, 'dir drec0:')
        custom_tftp = {
            "gateway": "2.2.2.0",
            "image": ["custom/image.bin"],
            "ip_address": "2.2.2.1",
            "subnet_mask": "255.255.0.0",
            "tftp_server": "2.2.3.1"
        }
        result = get_recovery_details(self.device, tftp_boot=custom_tftp)
        expected = {
            'golden_image': None,
            'tftp_boot': custom_tftp,
            'tftp_image': ['custom/image.bin'],
        }
        self.assertEqual(result, expected)