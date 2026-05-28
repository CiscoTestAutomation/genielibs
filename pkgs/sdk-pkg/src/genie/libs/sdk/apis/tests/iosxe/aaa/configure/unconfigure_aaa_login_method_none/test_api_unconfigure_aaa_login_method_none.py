import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_login_method_none


class TestUnconfigureAaaLoginMethodNone(TestCase):

    def test_unconfigure_aaa_login_method_none_default(self):
        """Verify correct CLI commands are sent for valid servergrp."""
        device = Mock()
        result = unconfigure_aaa_login_method_none(device, servergrp='SECURE_LOGIN')
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'line con 0',
                    'no login authentication SECURE_LOGIN',
                    'line vty 0 4',
                    'no login authentication SECURE_LOGIN',
                    'line vty 5 15',
                    'no login authentication SECURE_LOGIN',
                    'no aaa authentication login SECURE_LOGIN none',
                ],
            ),
        )

    def test_unconfigure_aaa_login_method_none_invalid_servergrp(self):
        """Verify ValueError is raised for invalid servergrp."""
        device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_aaa_login_method_none(device, servergrp='bad name!')

    def test_unconfigure_aaa_login_method_none_injection_attempt(self):
        """Verify ValueError is raised for servergrp with shell metacharacters."""
        device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_aaa_login_method_none(device, servergrp='grp;reboot')

    def test_unconfigure_aaa_login_method_none_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.configure.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_login_method_none(device, servergrp='SECURE_LOGIN')


if __name__ == '__main__':
    unittest.main()
