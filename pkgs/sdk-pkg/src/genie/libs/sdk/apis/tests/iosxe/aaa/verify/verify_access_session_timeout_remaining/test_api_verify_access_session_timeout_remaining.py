import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.aaa.verify import (
    verify_access_session_timeout_remaining,
)


INTERFACE = "GigabitEthernet0/1/0"
MAC = "0030.0000.0001"


def _build_device(remaining):
    parsed = {
        "interfaces": {
            INTERFACE: {
                "mac_address": {
                    MAC: {
                        "user_name": "auto601",
                        "status": "Authorized",
                        "session_timeout": {
                            "type": "local",
                            "timeout": "100s",
                            "remaining": remaining,
                        },
                    }
                }
            }
        }
    }
    device = Mock()
    device.api.get_show_access_session_interface_detail = Mock(
        return_value=parsed)
    return device


class TestVerifyAccessSessionTimeoutRemaining(unittest.TestCase):

    def test_within_range(self):
        device = _build_device("10s")

        result = verify_access_session_timeout_remaining(
            device, MAC, INTERFACE, max_remain=15, min_remain=5,
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_out_of_range(self):
        device = _build_device("91s")

        result = verify_access_session_timeout_remaining(
            device, MAC, INTERFACE, max_remain=15, min_remain=5,
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_no_output(self):
        device = Mock()
        device.api.get_show_access_session_interface_detail = Mock(
            return_value={})

        result = verify_access_session_timeout_remaining(
            device, MAC, INTERFACE, max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
