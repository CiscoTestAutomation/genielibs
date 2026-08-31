import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_controller_service_policy,
)


class TestConfigureControllerServicePolicy(TestCase):

    def test_configure_controller_service_policy(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_controller_service_policy(
            device,
            "cntrl-policy77",
            "cntrl-list77",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd controller service-policy cntrl-policy77",
                "service-list cntrl-list77",
            ]
        )


if __name__ == "__main__":
    unittest.main()
