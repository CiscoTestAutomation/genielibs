import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.utils import check_config_options
from unittest.mock import Mock


class TestCheckConfigOptions(unittest.TestCase):
    """ Unit tests for check_config_options function. """

    def test_all_options_present(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.state_machine.go_to = Mock()
        self.device.configure = Mock()
       
        """ Test case where all expected options are present. """
        cmd = 'interface GigabitEthernet0/1'
        options = ['description', 'ip address', 'shutdown']
        help_output = """
          description    Set a description for the interface
          ip address     Set the IP address for the interface
          shutdown       Disable the interface
        """
        self.device.configure.return_value = help_output

        result = check_config_options(self.device, cmd, options)
        self.assertTrue(result)   

    def test_missing_options(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.state_machine.go_to = Mock()
        self.device.configure = Mock()
       
        """ Test case where some expected options are missing. """
        cmd = 'interface GigabitEthernet0/1'
        options = ['description', 'ip address', 'shutdown', 'speed']
        help_output = """
          description    Set a description for the interface
          ip address     Set the IP address for the interface
          shutdown       Disable the interface
        """
        self.device.configure.return_value = help_output

        result = check_config_options(self.device, cmd, options)
        self.assertFalse(result)
    
    def test_no_options(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.state_machine.go_to = Mock()
        self.device.configure = Mock()
       
        """ Test case where no expected options are provided. """
        cmd = 'interface GigabitEthernet0/1'
        options = []
        help_output = """
          description    Set a description for the interface
          ip address     Set the IP address for the interface
          shutdown       Disable the interface
        """
        self.device.configure.return_value = help_output

        result = check_config_options(self.device, cmd, options)
        self.assertTrue(result)
