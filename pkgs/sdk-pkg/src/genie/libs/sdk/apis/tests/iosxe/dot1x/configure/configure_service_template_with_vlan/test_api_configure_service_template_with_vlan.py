import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_service_template_with_vlan
)


class TestConfigureServiceTemplateWithVlan(TestCase):

    def test_configure_service_template_with_vlan(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_service_template_with_vlan(
            device,
            'DefaultCriticalAuthVlan_SRV_TEMPLATE',
            7
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'service-template DefaultCriticalAuthVlan_SRV_TEMPLATE',
            sent_commands
        )
        self.assertIn(
            'vlan 7',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()