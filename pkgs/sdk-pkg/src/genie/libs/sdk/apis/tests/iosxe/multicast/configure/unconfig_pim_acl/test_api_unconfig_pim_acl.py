import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    unconfig_pim_acl,
)


class TestUnconfigPimAcl(TestCase):

    def test_unconfig_pim_acl(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfig_pim_acl(device, "ssm_source")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no ipv6 pim accept-register list ssm_source")


if __name__ == "__main__":
    unittest.main()
