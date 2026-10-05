import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import config_pim_acl


class TestConfigPimAcl(TestCase):

    def test_config_pim_acl(self):
        device = Mock()
        device.configure.return_value = None

        result = config_pim_acl(device, "ssm_source")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ipv6 pim accept-register list ssm_source"
        )


if __name__ == "__main__":
    unittest.main()
