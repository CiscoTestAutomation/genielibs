import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import config_rp_address


class TestConfigRpAddress(TestCase):

    def test_config_rp_address(self):
        device = Mock()
        device.configure.return_value = None

        result = config_rp_address(device, "vrf3001", "30.0.1.1")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ip pim vrf vrf3001 rp-address 30.0.1.1"
        )


if __name__ == "__main__":
    unittest.main()
