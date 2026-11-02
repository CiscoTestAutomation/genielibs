import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_igmp_ssm_map,
)


class TestConfigureIpIgmpSsmMap(TestCase):

    def test_configure_ip_igmp_ssm_map(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_igmp_ssm_map(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ip igmp ssm-map enable")


if __name__ == "__main__":
    unittest.main()
