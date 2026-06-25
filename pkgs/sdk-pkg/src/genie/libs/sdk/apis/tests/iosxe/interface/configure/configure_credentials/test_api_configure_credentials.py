import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.interface.configure import configure_credentials


class TestConfigureCredentials(TestCase):

    def test_configure_credentials_no_aaa(self):
        """Verify correct CLI when 'no aaa' is in running config."""
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = 'no aaa new-model'
        configure_credentials(
            device, interface='Gi1/0/1',
            user_name='admin', password='Secret123',
            t_input='ssh', t_output='ssh',
            vty_start='0', vty_end='4'
        )
        self.assertEqual(
            device.configure.call_args[0][0],
            [
                'username admin secret Secret123',
                'line vty 0 4',
                'login local',
                'transport input ssh',
                'transport output ssh',
            ]
        )

    def test_configure_credentials_with_aaa(self):
        """Verify correct CLI when AAA is enabled."""
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = 'aaa new-model'
        configure_credentials(
            device, interface='Gi1/0/1',
            user_name='admin', password='Secret123',
            t_input='ssh', t_output='ssh',
            vty_start='0', vty_end='15'
        )
        self.assertEqual(
            device.configure.call_args[0][0],
            [
                'username admin secret Secret123',
                'line vty 0 15',
                'login authentication local',
                'transport input ssh',
                'transport output ssh',
            ]
        )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.execute.return_value = 'no aaa'
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_credentials(
                device, interface='Gi1/0/1',
                user_name='admin', password='Secret123',
                t_input='ssh', t_output='ssh',
                vty_start='0', vty_end='4'
            )


if __name__ == '__main__':
    unittest.main()
