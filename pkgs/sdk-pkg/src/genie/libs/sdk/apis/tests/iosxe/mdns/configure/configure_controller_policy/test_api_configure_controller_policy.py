import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_controller_policy,
)


class TestConfigureControllerPolicy(TestCase):

    def test_configure_controller_policy(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_controller_policy(device, "DNAC", "cntrl_list")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd controller service-policy DNAC",
                "service-list cntrl_list",
            ]
        )


if __name__ == "__main__":
    unittest.main()
