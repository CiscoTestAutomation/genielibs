import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.ios.interface.configure import configure_ip_routing


class TestConfigureIpRouting(TestCase):

    def test_configure_ip_routing(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_routing(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("ip routing")

    def test_configure_ip_routing_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ip_routing(device)


if __name__ == "__main__":
    unittest.main()
