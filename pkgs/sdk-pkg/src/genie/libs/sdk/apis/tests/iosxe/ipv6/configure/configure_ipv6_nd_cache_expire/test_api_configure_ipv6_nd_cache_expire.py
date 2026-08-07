import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_nd_cache_expire


class TestConfigureIpv6NdCacheExpire(TestCase):

    def test_configure_ipv6_nd_cache_expire(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_nd_cache_expire(device, 60)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "ipv6 nd cache expire 60",
        )


if __name__ == "__main__":
    unittest.main()
