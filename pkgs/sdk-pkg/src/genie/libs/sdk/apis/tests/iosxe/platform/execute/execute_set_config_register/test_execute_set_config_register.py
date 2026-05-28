from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_set_config_register
from unittest.mock import Mock


class TestExecuteSetConfigRegister(TestCase):

    def test_execute_set_config_register_normal_mode(self):
        """Test config register setting in normal mode"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'active'
        device.default.configure = Mock()

        execute_set_config_register(device, '0x2102', 300)

        device.default.configure.assert_called_once_with(
            'config-register 0x2102', timeout=300
        )

    def test_execute_set_config_register_rommon_mode_confreg_flow(self):
        """Test config register setting in rommon mode using confreg command"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'rommon'
        device.default.role = 'active'
        device.default.execute = Mock()

        execute_set_config_register(device, '0x2102', 300)

        device.default.execute.assert_called_once_with(
            'confreg 0x2102', timeout=300
        )

    def test_execute_set_config_register_standby_connection_skipped(self):
        """Test that standby connections are skipped"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'standby'
        device.default.configure = Mock()

        execute_set_config_register(device, '0x2102', 300)

        device.default.configure.assert_not_called()

    def test_execute_set_config_register_multiple_connections(self):
        """Test config register setting with multiple connections"""
        device = Mock()
        device.name = 'test_device'

        # Create multiple mock connections
        conn1 = Mock()
        conn1.state_machine.current_state = 'enable'
        conn1.role = 'active'
        conn1.configure = Mock()

        conn2 = Mock()
        conn2.state_machine.current_state = 'rommon'
        conn2.role = 'active'
        conn2.execute = Mock()

        conn3 = Mock()
        conn3.state_machine.current_state = 'enable'
        conn3.role = 'standby'
        conn3.configure = Mock()

        device.subconnections = [conn1, conn2, conn3]

        execute_set_config_register(device, '0x2102', 300)

        # Verify active connection in enable mode uses configure
        conn1.configure.assert_called_once_with(
            'config-register 0x2102', timeout=300
        )

        # Verify active connection in rommon mode uses execute with confreg
        conn2.execute.assert_called_once_with(
            'confreg 0x2102', timeout=300
        )

        # Verify standby connection is skipped
        conn3.configure.assert_not_called()

    def test_execute_set_config_register_exception_handling(self):
        """Test exception handling when configure fails"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'active'
        device.default.configure = Mock(side_effect=Exception("Configure failed"))

        with self.assertRaises(Exception) as context:
            execute_set_config_register(device, '0x2102', 300)

        self.assertIn("Failed to set config register for 'test_device'", str(context.exception))
        self.assertIn("Configure failed", str(context.exception))

    def test_execute_set_config_register_rommon_exception_handling(self):
        """Test exception handling when execute fails in rommon mode"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'rommon'
        device.default.role = 'active'
        device.default.execute = Mock(side_effect=Exception("Execute failed"))

        with self.assertRaises(Exception) as context:
            execute_set_config_register(device, '0x2102', 300)

        self.assertIn("Failed to set config register for 'test_device'", str(context.exception))
        self.assertIn("Execute failed", str(context.exception))

    def test_execute_set_config_register_fallback_to_default_connection(self):
        """Test fallback to default connection when no subconnections"""
        device = Mock()
        device.name = 'test_device'
        device.subconnections = None
        device.default.state_machine.current_state = 'enable'
        device.default.role = 'active'
        device.default.configure = Mock()

        execute_set_config_register(device, '0x2102', 300)

        device.default.configure.assert_called_once_with(
            'config-register 0x2102', timeout=300
        )

    def test_execute_set_config_register_mixed_connections_rommon_and_enable(self):
        """Test mixed connection states with both rommon and enable modes"""
        device = Mock()
        device.name = 'test_device'

        # Create connections with different states
        enable_conn = Mock()
        enable_conn.state_machine.current_state = 'enable'
        enable_conn.role = 'active'
        enable_conn.configure = Mock()

        rommon_conn = Mock()
        rommon_conn.state_machine.current_state = 'rommon'
        rommon_conn.role = 'active'
        rommon_conn.execute = Mock()

        device.subconnections = [enable_conn, rommon_conn]

        execute_set_config_register(device, '0x2142', 300)

        # Verify enable connection uses configure with config-register command
        enable_conn.configure.assert_called_once_with(
            'config-register 0x2142', timeout=300
        )

        # Verify rommon connection uses execute with confreg command
        rommon_conn.execute.assert_called_once_with(
            'confreg 0x2142', timeout=300
        )