from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import perform_telnet
from unittest.mock import Mock, call

class TestPerformTelnet(TestCase):

    def test_perform_telnet(self):
        self.device = Mock()
        perform_telnet(self.device, 'SecG-A3-9410HA', '10.8.12.26', 'admin1', 'cisco123', 'Mgmt-vrf', 'cisco123', 60)

        self.assertEqual(
            self.device.execute.call_args[0][0],
            'telnet 10.8.12.26 /vrf Mgmt-vrf'
        )

    def test_perform_telnet_1(self):
        self.device = Mock()
        perform_telnet(self.device, 'SecG-A3-9410HA', '10.8.12.5', 'admin1', 'cisco123', None, 'cisco123', 60)

        self.assertEqual(
            self.device.execute.call_args[0][0],
            'telnet 10.8.12.5'
        )

    def test_perform_telnet_authentication_failure(self):
        device = Mock()
        device.execute.return_value = """
        Trying 192.168.1.47 ... Open

          User Access Verification

          Username: test
          Password:

          % Authentication failed

          Username: test
          Password:

          % Authentication failed

          Username: test
          Password:

          % Authentication failed
        [Connection to 10.8.12.26 closed by foreign host]
        """

        result = perform_telnet(device, 'SecG-A3-9410HA', '10.8.12.26', 'admin1', 'cisco123', None, 'cisco123', 60)

        self.assertEqual(
            device.execute.call_args[0][0],
            'telnet 10.8.12.26'
        )
        # Validate that the api returns False on authentication failure
        self.assertFalse(result)

    def test_perform_telnet_timeout_failure(self):
        device = Mock()
        device.execute.return_value = """
        Password:
        % Password: timeout expired!
        """
        result = perform_telnet(device, 'SecG-A3-9410HA', '10.8.12.26', 'admin1', 'cisco123', None, 'cisco123', 60)

        self.assertEqual(
            device.execute.call_args[0][0],
            'telnet 10.8.12.26'
        )
        # Validate that the api returns False on timeout failure
        self.assertFalse(result)

    def test_perform_telnet_with_remote_cmd(self):
        device = Mock()
        remote_device = Mock()

        hostname = 'SecG-A3-9410HA'

        remote_device.execute.return_value = "remote command output"
        # Define side effect function for device.execute
        def execute_side_effect(cmd, *args, **kwargs):
            dialog = kwargs.get('reply')
            if dialog is not None:
                for stmt in dialog:
                    if stmt.pattern == hostname + "#":
                        fake_spawn = Mock()
                        # This calls telnet_pass_case(fake_spawn)
                        stmt.action(fake_spawn)
                        break
            return hostname + "#"

        device.execute.side_effect = execute_side_effect

        result = perform_telnet(
            device,
            hostname,
            '10.8.12.26',
            'admin1',
            'cisco123',
            None,
            'cisco123',
            60,
            remote_device=remote_device,
            remote_cmd='show version'
        )

        # Validate telnet command
        self.assertEqual(
            device.execute.call_args[0][0],
            'telnet 10.8.12.26'
        )

        # Validate remote device command call
        remote_device.execute.assert_called_once_with('show version')

        # API returns (True, "If remote command output")
        self.assertEqual(result, (True, "remote command output"))
