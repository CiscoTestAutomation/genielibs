import os
import unittest
from unittest.mock import patch, MagicMock, call
from genie.libs.sdk.apis.iosxe.cat9k.configure import unconfigure_ignore_startup_config
from unicon.core.errors import SubCommandFailure


class TestUnconfigureIgnoreStartupConfigStandby(unittest.TestCase):

    def setUp(self):
        # Create a mock device and connection
        self.device = MagicMock()
        self.device.name = "mock_device"
        
        # Create standby connection
        self.standby_connection = MagicMock()
        self.standby_connection.state_machine.current_state = "any_state"
        self.standby_connection.role = "standby"
        
        # Create active connection
        self.active_connection = MagicMock()
        self.active_connection.state_machine.current_state = "any_state"
        # Explicitly set role attribute to something other than standby
        self.active_connection.role = "active"
        
        # Create rommon connection
        self.rommon_connection = MagicMock()
        self.rommon_connection.state_machine.current_state = "rommon"
        
        # Mock configure method
        self.standby_connection.configure = MagicMock()
        self.active_connection.configure = MagicMock()
        self.rommon_connection.execute = MagicMock()

    def test_standby_connection_is_skipped(self):
        """Test that standby connection is skipped"""
        # Set the device to have both standby and active connections
        self.device.subconnections = [self.active_connection, self.standby_connection]
        
        # Call the function
        unconfigure_ignore_startup_config(self.device)
        
        # Verify active connection's configure method was called
        self.active_connection.configure.assert_called_once_with('no system ignore startupconfig switch all')
        
        # Verify standby connection's configure method was NOT called
        self.standby_connection.configure.assert_not_called()

    def test_rommon_connection_is_handled(self):
        """Test that rommon connection works correctly"""
        # Set the device to have rommon connection
        self.device.subconnections = [self.rommon_connection]
        
        # Call the function
        unconfigure_ignore_startup_config(self.device)
        
        # Verify rommon connection's execute method was called with right parameter
        self.rommon_connection.execute.assert_called_once_with('SWITCH_IGNORE_STARTUP_CFG=0')

