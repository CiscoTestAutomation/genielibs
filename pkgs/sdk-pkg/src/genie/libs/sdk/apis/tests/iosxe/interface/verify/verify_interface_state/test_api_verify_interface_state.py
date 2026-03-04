from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.verify import verify_interface_state
from unittest.mock import Mock


class TestVerifyInterfaceState(TestCase):

    def test_verify_interface_state(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': True,
        		'oper_status': 'up',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ip', 'admin up', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_1(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': True,
        		'oper_status': 'up',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ip', 'up', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_2(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': True,
        		'oper_status': 'up',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ipv6', 'admin up', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_3(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': True,
        		'oper_status': 'up',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ipv6', 'up', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_4(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': False,
        		'oper_status': 'down',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ip', 'admin down', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_5(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': False,
        		'oper_status': 'down',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ip', 'down', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_6(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': False,
        		'oper_status': 'down',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ipv6', 'admin down', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_interface_state_7(self):

        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
        	'GigabitEthernet0/1/6': {
        		'enabled': False,
        		'oper_status': 'down',
        	}
        })
        result = verify_interface_state(self.device, 'GigabitEthernet0/1/6', 'ipv6', 'down', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
