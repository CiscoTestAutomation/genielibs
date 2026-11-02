import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_igmp_snooping_tcn_flood,
)


class TestConfigureIpIgmpSnoopingTcnFlood(TestCase):

    def test_configure_ip_igmp_snooping_tcn_flood(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_tcn_flood(device, "3")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ip igmp snooping tcn flood query count 3",
        )


if __name__ == "__main__":
    unittest.main()
