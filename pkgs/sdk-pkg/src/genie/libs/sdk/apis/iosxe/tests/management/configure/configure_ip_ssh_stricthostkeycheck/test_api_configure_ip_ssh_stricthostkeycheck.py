from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_ip_ssh_stricthostkeycheck
from unittest.mock import Mock


class TestConfigureIpSshStricthostkeycheck(TestCase):

    def test_configure_ip_ssh_stricthostkeycheck(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Call the function
        result = configure_ip_ssh_stricthostkeycheck(self.device)
        
        # Verify the configuration command was called
        expected_cmd = 'ip ssh stricthostkeycheck'
        
        # Check that configure was called with the expected command
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_cmd)

    def test_configure_ip_ssh_stricthostkeycheck_success(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Call the function and ensure no exception is raised
        try:
            result = configure_ip_ssh_stricthostkeycheck(self.device)
            # If we get here, the function executed successfully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"configure_ip_ssh_stricthostkeycheck raised an exception: {e}")
        
        # Verify the configuration was attempted
        self.assertTrue(self.device.configure.called)
        
    def test_configure_ip_ssh_stricthostkeycheck_accept_new(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Call the function with accept_new=True
        result = configure_ip_ssh_stricthostkeycheck(self.device, accept_new=True)
        
        # Verify the configuration command was called
        expected_cmd = 'ip ssh stricthostkeycheck accept-new'
        
        # Check that configure was called with the expected command
        self.assertTrue(self.device.configure.called)
        call_args = self.device.configure.call_args_list[0][0][0]
        self.assertEqual(call_args, expected_cmd)

    def test_configure_ip_ssh_stricthostkeycheck_accept_new_success(self):
        self.device = Mock()
        self.device.configure.return_value = None
        
        # Call the function with accept_new=True and ensure no exception is raised
        try:
            result = configure_ip_ssh_stricthostkeycheck(self.device, accept_new=True)
            # If we get here, the function executed successfully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"configure_ip_ssh_stricthostkeycheck with accept_new=True raised an exception: {e}")
        
        # Verify the configuration was attempted
        self.assertTrue(self.device.configure.called)