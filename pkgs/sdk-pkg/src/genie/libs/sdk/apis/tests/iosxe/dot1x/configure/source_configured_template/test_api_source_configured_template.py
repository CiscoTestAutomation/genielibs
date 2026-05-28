import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
from genie.libs.sdk.apis.iosxe.dot1x.configure import source_configured_template


class TestSourceConfiguredTemplate(TestCase):

    def test_source_configured_template_default(self):
        """Verify correct CLI commands are sent for valid inputs."""
        device = Mock()
        with patch(
            'genie.libs.sdk.apis.iosxe.dot1x.configure.Common'
        ) as mock_common:
            mock_common.convert_intf_name.return_value = 'GigabitEthernet1/0/1'
            result = source_configured_template(
                device,
                interface='Gi1/0/1',
                template_name='MY_TEMPLATE',
            )
        self.assertIsNone(result)
        mock_common.convert_intf_name.assert_called_once_with('Gi1/0/1')
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface GigabitEthernet1/0/1',
                    'source template MY_TEMPLATE',
                ],
            ),
        )

    def test_source_configured_template_invalid_template_name(self):
        """Verify ValueError is raised for invalid template_name."""
        device = Mock()
        with self.assertRaises(ValueError):
            source_configured_template(
                device,
                interface='Gi1/0/1',
                template_name='bad name!',
            )

    def test_source_configured_template_injection_attempt(self):
        """Verify ValueError for template_name with shell metacharacters."""
        device = Mock()
        with self.assertRaises(ValueError):
            source_configured_template(
                device,
                interface='Gi1/0/1',
                template_name='tmpl;reboot',
            )

    def test_source_configured_template_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with patch(
            'genie.libs.sdk.apis.iosxe.dot1x.configure.Common'
        ) as mock_common:
            mock_common.convert_intf_name.return_value = 'GigabitEthernet1/0/1'
            with self.assertRaises(SubCommandFailure):
                source_configured_template(
                    device,
                    interface='Gi1/0/1',
                    template_name='MY_TEMPLATE',
                )


if __name__ == '__main__':
    unittest.main()
