import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_default_mdns_controller,
)


class TestConfigureDefaultMdnsController(TestCase):

    def test_configure_default_mdns_controller(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_default_mdns_controller(
            device,
            "DNAC",
            "98.98.98.10",
            "TwentyFiveGigE1/0/1",
            "cntrl_list",
            "all",
            "cntrl_policy",
            "any",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd controller service-list cntrl_list",
                "match all message-type any",
                "mdns-sd controller service-policy cntrl_policy",
                "service-list cntrl_list",
                "service-export mdns-sd controller DNAC",
                "controller-address 98.98.98.10",
                "controller-source-interface TwentyFiveGigE1/0/1",
            ]
        )


if __name__ == "__main__":
    unittest.main()
