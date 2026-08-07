import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipv6.configure import (
    configure_ipv6_dhcp_pool_preifx_delegation_pool,
)


class TestConfigureIpv6DhcpPoolPreifxDelegationPool(TestCase):

    def test_configure_ipv6_dhcp_pool_preifx_delegation_pool(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_dhcp_pool_preifx_delegation_pool(
            device,
            "cisco2",
            "cisco1",
            False,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ipv6 dhcp pool cisco2",
                "prefix-delegation pool cisco1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
