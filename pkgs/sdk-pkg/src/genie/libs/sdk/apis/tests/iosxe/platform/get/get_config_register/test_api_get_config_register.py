from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.get import get_config_register


class TestGetConfigRegister(TestCase):
    @classmethod
    def setUpClass(self):
        self.device = Mock()
        self.device.parse = Mock(return_value={
            'next_reload_boot_variable': 'bootflash:packages.conf,12;',
            'active': {
                'boot_variable': 'bootflash:packages.conf,12;',
                'configuration_register': '0x2140',
                'next_reload_configuration_register': '0x2100'
            }
        })
        self.device.execute = Mock(return_value='''
                   Configuration Summary
           (Virtual Configuration Register: 0x0)
        enabled are:
         [ 0 ] break/abort has effect
         [ 1 ] console baud: 9600
         boot: ...... the ROM Monitor

        do you wish to change the configuration? y/n  [n]:
        ''')

    def test_get_config_register_cli_curr_reload(self):
        expected_result = '0x2100'
        self.device.state_machine.current_state = 'enable'
        actual_result = get_config_register(self.device, next_reload=True)
        self.assertEqual(actual_result, expected_result)

    def test_get_config_register_cli_next_reload(self):
        expected_result = '0x2140'
        self.device.state_machine.current_state = 'enable'
        actual_result = get_config_register(self.device)
        self.assertEqual(actual_result, expected_result)

    def test_get_config_register_rommon(self):
        expected_result = '0x0'
        self.device.state_machine.current_state = 'rommon'
        actual_result_1 = get_config_register(self.device, next_reload=True)
        actual_result_2 = get_config_register(self.device)
        self.assertEqual(actual_result_1, expected_result)
        self.assertEqual(actual_result_2, expected_result)
