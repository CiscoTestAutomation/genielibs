import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_routes,
)


class TestConfigureManagementRoutes(TestCase):

    def test_configure_management_routes(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.management = {}

        result = configure_management_routes(device)

        self.assertIsNone(result)
        device.configure.assert_not_called()


if __name__ == "__main__":
    unittest.main()
