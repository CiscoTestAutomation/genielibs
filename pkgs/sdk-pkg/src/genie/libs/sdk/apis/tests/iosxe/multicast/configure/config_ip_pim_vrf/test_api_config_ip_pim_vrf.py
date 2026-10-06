import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import config_ip_pim_vrf


class TestConfigIpPimVrf(TestCase):

    def test_config_ip_pim_vrf(self):
        device = Mock()
        device.configure.return_value = None

        result = config_ip_pim_vrf(device, "2", "autorp listener")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ip pim vrf 2 autorp listener"
        )


if __name__ == "__main__":
    unittest.main()
