import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_radius_automate_tester


class TestUnconfigureRadiusAutomateTester(TestCase):

    def test_unconfigure_radius_automate_tester_default(self):
        """Verify correct CLI commands are sent for valid inputs."""
        device = Mock()
        result = unconfigure_radius_automate_tester(
            device, server_name='RAD_SERVER', username='testuser'
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'radius server RAD_SERVER',
                    'no automate-tester username testuser',
                ],
            ),
        )

    def test_unconfigure_radius_automate_tester_invalid_server_name(self):
        """Verify ValueError for invalid server_name."""
        device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_radius_automate_tester(
                device, server_name='bad server!', username='testuser'
            )

    def test_unconfigure_radius_automate_tester_invalid_username(self):
        """Verify ValueError for invalid username."""
        device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_radius_automate_tester(
                device, server_name='RAD_SERVER', username='user;drop'
            )

    def test_unconfigure_radius_automate_tester_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_radius_automate_tester(
                device, server_name='RAD_SERVER', username='testuser'
            )


if __name__ == '__main__':
    unittest.main()
