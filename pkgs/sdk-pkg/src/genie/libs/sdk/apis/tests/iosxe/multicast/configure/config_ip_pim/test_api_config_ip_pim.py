import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import config_ip_pim


class TestConfigIpPim(TestCase):

    def test_config_ip_pim(self):
        device = Mock()
        device.configure.return_value = None

        result = config_ip_pim(device, "loopback3001", "sparse-mode")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "interface loopback3001 \nip pim sparse-mode"
        )


if __name__ == "__main__":
    unittest.main()
