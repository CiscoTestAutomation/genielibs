import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.cat9k.c9200.c9200cx.rommon.get import get_recovery_details


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
        self.device.parse = Mock(return_value={
                                    "dir": {
                                        "dir": "drec0:",
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
        result = get_recovery_details(self.device)
        expected_result = {'golden_image': ['drec0:system_image.bin'], 'tftp_image': None}

        self.assertEqual(
            result,
            expected_result
        )