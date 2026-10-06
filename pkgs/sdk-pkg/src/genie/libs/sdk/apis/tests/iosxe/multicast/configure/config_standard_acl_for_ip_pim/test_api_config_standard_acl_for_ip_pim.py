import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    config_standard_acl_for_ip_pim,
)


class TestConfigStandardAclForIpPim(TestCase):

    def test_config_standard_acl_for_ip_pim(self):
        device = Mock()
        device.configure.return_value = None

        result = config_standard_acl_for_ip_pim(
            device,
            "vrf3001-BidigroupRP",
            "permit",
            "229.1.1.1",
            "0.0.255.255",
            "vrf3001",
            "30.0.1.1",
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "ip access-list standard vrf3001-BidigroupRP",
                "permit 229.1.1.1 0.0.255.255",
                "ip pim bidir-enable",
                (
                    "ip pim vrf vrf3001 rp-address 30.0.1.1 "
                    "vrf3001-BidigroupRP bidir"
                ),
            ]
        )


if __name__ == "__main__":
    unittest.main()
