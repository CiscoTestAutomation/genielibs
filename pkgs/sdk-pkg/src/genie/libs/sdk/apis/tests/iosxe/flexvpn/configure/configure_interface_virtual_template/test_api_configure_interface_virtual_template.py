import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.flexvpn.configure import (
    configure_interface_virtual_template
)


class TestConfigureInterfaceVirtualTemplate(TestCase):

    def test_configure_interface_virtual_template(self):
        # Create a mock device
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume enable mode

        # Call the API
        result = configure_interface_virtual_template(
            device,
            200,                    # virtual_template
            'tunnel',               # interface_type
            'loopback',             # unnumbered_type
            100,                    # unnumbered_id
            None,                   # nhrp_network_id
            None,                   # nhrp_redirect
            'IPSEC_PROFILE',        # ipsec_profile
            False,                  # tunnel_mode
            '',                     # tunnel_source
            True,                   # ipv6_enable
            None,                   # tunnel_destination
            False,                  # tunnel_key
            None,                   # mtu
            None,                   # tcp_mss
            None,                   # ipsec_mode
            None                    # additional_params
        )

        # API returns None on success
        self.assertIsNone(result)

        # Ensure configure() was called once
        device.configure.assert_called_once()

        # Validate commands sent to device.configure()
        sent_commands = device.configure.mock_calls[0].args[0]

        expected_commands = [
            'interface Virtual-Template 200 type tunnel',
            'ip unnumbered loopback 100',
            'tunnel protection ipsec profile IPSEC_PROFILE',
            'ipv6 enable'
        ]

        self.assertEqual(sent_commands, expected_commands)


if __name__ == '__main__':
    unittest.main()