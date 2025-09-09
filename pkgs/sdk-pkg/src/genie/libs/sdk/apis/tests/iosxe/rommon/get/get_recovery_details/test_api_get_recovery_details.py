import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.rommon.get import get_recovery_details


class TestGetRecoveryDetails(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.clean = {
            "device_recovery": {
                "golden_image": ["Golden image"],
                "tftp_boot":{
                    "gateway": "1.1.1.0",
                    "image": ["file/base_image.bin"],
                    "ip_address": "1.1.1.1",
                    "subnet_mask": "255.255.255.0",
                    "tftp_server": "1.1.2.1"
                }
            }
        }
    def test_get_recovery_details(self):
        result = get_recovery_details(self.device)
        expected_result ={
            "golden_image": [
                "Golden image"
            ],
            "tftp_boot": {
                "gateway": "1.1.1.0",
                "image": [
                    "file/base_image.bin"
                ],
                "ip_address": "1.1.1.1",
                "subnet_mask": "255.255.255.0",
                "tftp_server": "1.1.2.1"
            },
            "tftp_image": [
                "file/base_image.bin"
            ]
        }

        self.assertEqual(
            result,
            expected_result
        )