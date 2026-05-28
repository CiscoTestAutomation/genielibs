import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_aaa_login_method_local


class TestConfigureAaaLoginMethodLocal(TestCase):

    def test_configure_aaa_login_method_local_default(self):
        """Verify default auth_method='local' emits correct CLI commands."""
        device = Mock()
        result = configure_aaa_login_method_local(
            device,
            servergrp='SECURE_LOGIN',
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'aaa authentication login SECURE_LOGIN local',
                    'line con 0',
                    'login authentication SECURE_LOGIN',
                    'line vty 0 4',
                    'login authentication SECURE_LOGIN',
                    'transport input ssh',
                    'line vty 5 15',
                    'login authentication SECURE_LOGIN',
                    'transport input ssh',
                ],
            ),
        )

    def test_configure_aaa_login_method_local_with_fallback(self):
        """Verify fallback_method is appended to the auth command."""
        device = Mock()
        configure_aaa_login_method_local(
            device,
            servergrp='MY_LIST',
            auth_method='group radius',
            fallback_method='local',
        )
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'aaa authentication login MY_LIST group radius local',
                    'line con 0',
                    'login authentication MY_LIST',
                    'line vty 0 4',
                    'login authentication MY_LIST',
                    'transport input ssh',
                    'line vty 5 15',
                    'login authentication MY_LIST',
                    'transport input ssh',
                ],
            ),
        )

    def test_configure_aaa_login_method_local_invalid_servergrp(self):
        """Verify ValueError is raised for invalid servergrp."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_aaa_login_method_local(
                device,
                servergrp='invalid name!',
            )

    def test_configure_aaa_login_method_local_invalid_auth_method(self):
        """Verify ValueError is raised for invalid auth_method."""
        device = Mock()
        with self.assertRaises(ValueError):
            configure_aaa_login_method_local(
                device,
                servergrp='SECURE_LOGIN',
                auth_method='none',
            )

    def test_configure_aaa_login_method_local_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            configure_aaa_login_method_local(
                device,
                servergrp='SECURE_LOGIN',
            )


if __name__ == '__main__':
    unittest.main()
