import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import copy_running_config_to_scp


class TestCopyRunningConfigToScp(TestCase):

    def test_copy_running_config_to_scp_default(self):
        """Verify correct SCP command is executed."""
        device = Mock()
        device.name = 'Router1'
        copy_running_config_to_scp(
            device, host='10.1.1.1', file='/backup/running.cfg',
            username='admin', password='Secret123'
        )
        call_args = device.execute.call_args
        self.assertIn('copy running-config scp://admin@10.1.1.1///backup/running.cfg',
                      call_args[0][0])

    def test_copy_running_config_to_scp_no_username(self):
        """Verify ValueError when username is empty."""
        device = Mock()
        device.name = 'Router1'
        with self.assertRaises(ValueError):
            copy_running_config_to_scp(
                device, host='10.1.1.1', file='/backup/running.cfg',
                username='', password='Secret123'
            )

    def test_device_failure(self):
        """Verify SubCommandFailure is raised on device error."""
        from unicon.core.errors import SubCommandFailure
        device = Mock()
        device.name = 'Router1'
        device.execute.side_effect = SubCommandFailure('mock error')
        with self.assertRaises(SubCommandFailure):
            copy_running_config_to_scp(
                device, host='10.1.1.1', file='/backup/running.cfg',
                username='admin', password='Secret123'
            )


if __name__ == '__main__':
    unittest.main()
