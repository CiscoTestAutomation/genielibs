import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipv6.configure import configure_ipv6_local_pool


class TestConfigureIpv6LocalPool(TestCase):

    def test_configure_ipv6_local_pool(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_local_pool(
            device,
            "cisco1",
            "2002::/40",
            "48",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "ipv6 local pool cisco1 2002::/40 48",
        )


if __name__ == "__main__":
    unittest.main()
