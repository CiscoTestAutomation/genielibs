import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_debug_ip_pim,
)


class TestConfigureDebugIpPim(TestCase):

    def test_configure_debug_ip_pim(self):
        device = Mock()
        device.execute.return_value = None

        result = configure_debug_ip_pim(device)

        self.assertIsNone(result)
        device.execute.assert_called_once()
        command = device.execute.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "debug ip pim")


if __name__ == "__main__":
    unittest.main()
