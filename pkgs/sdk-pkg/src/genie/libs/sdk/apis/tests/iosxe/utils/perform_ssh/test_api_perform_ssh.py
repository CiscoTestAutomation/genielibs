from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import perform_ssh
from unittest.mock import Mock, call

class TestPerformSsh(TestCase):

    def test_perform_ssh(self):
        self.device = Mock()
        perform_ssh(self.device, 'Switch', '1.1.1.1', 'test-user', 'cisco@123', None, 'cisco@123', 60, 22, None, None)
        self.assertEqual(
            self.device.execute.call_args[0][0],
            'ssh -l test-user -p 22 1.1.1.1'
        )


    def test_perform_ssh_authentication_failure(self):
        device = Mock()
        device.execute.return_value = """
        ssh -l test -p 1.1.1.1
        Password:

        Password:

        Password:

        Password:

        [Connection to 1.1.1.1 closed by foreign host]
        """

        result = perform_ssh(device, 'Switch', '1.1.1.1', 'test-user', 'cisco@123', None, 'cisco@123', 60, 22, None, None)

        self.assertEqual(
            device.execute.call_args[0][0],
            'ssh -l test-user -p 22 1.1.1.1'
        )
        # Validate that the api returns False on authentication failure
        self.assertFalse(result)

    def test_perform_ssh_timeout_failure(self):
        device = Mock()
        device.execute.return_value = """
        Password:
        % Password: timeout expired!
        """
        result = perform_ssh(device, 'Switch', '1.1.1.1', 'test-user', 'cisco@123', None, 'cisco@123', 60, 22, None, None)

        self.assertEqual(
            device.execute.call_args[0][0],
            'ssh -l test-user -p 22 1.1.1.1'
        )
        # Validate that the api returns False on timeout failure
        self.assertFalse(result)
