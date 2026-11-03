import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_pim_ssm,
)


class TestConfigureIpPimSsm(TestCase):

    def test_configure_ip_pim_ssm(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_pim_ssm(device, None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ip pim ssm default")


if __name__ == "__main__":
    unittest.main()
