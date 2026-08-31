import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_controller_policy_service_export,
)


class TestUnconfigureControllerPolicyServiceExport(TestCase):

    def test_unconfigure_controller_policy_service_export(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_controller_policy_service_export(
            device,
            "APIC-EM",
            ["default-mdns-service-policy"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "service-export mdns-sd controller APIC-EM",
                "no controller-service-policy default-mdns-service-policy",
            ]
        )


if __name__ == "__main__":
    unittest.main()
