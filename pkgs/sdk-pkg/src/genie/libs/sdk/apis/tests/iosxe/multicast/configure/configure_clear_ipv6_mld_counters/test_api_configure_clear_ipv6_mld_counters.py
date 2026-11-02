import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_clear_ipv6_mld_counters,
)


class TestConfigureClearIpv6MldCounters(TestCase):

    def test_configure_clear_ipv6_mld_counters(self):
        device = Mock()
        device.execute.return_value = None

        result = configure_clear_ipv6_mld_counters(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "clear ipv6 mld counters")


if __name__ == "__main__":
    unittest.main()
