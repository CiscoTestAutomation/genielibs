from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cdp.configure import configure_cdp

class TestConfigureCdp(TestCase):

    def test_configure_cdp(self):
        device = Mock()

        # configure_cdp(None, timeout) calls device.parse('show interfaces', ...)
        # Must return dict indexed by interface name with a 'type' field.
        device.parse.return_value = {
            'GigabitEthernet1/0/1': {'type': 'GigabitEthernet'},
            'GigabitEthernet1/0/2': {'type': 'GigabitEthernet'},
        }

        result = configure_cdp(device, None, 300)
        self.assertEqual(result, None)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cdp run',
              'interface GigabitEthernet1/0/1',
              'cdp enable',
              'interface GigabitEthernet1/0/2',
              'cdp enable'],)
        )

    def test_configure_cdp_1(self):
        device = Mock()
        device.api = Mock()
        device.api.get_interface_information.return_value = {
            'TenGigabitEthernet1/0/19': {'type': 'TenGigabitEthernet'},
            'TenGigabitEthernet1/0/20': {'type': 'TenGigabitEthernet'},
        }

        result = configure_cdp(device, ['TenGigabitEthernet1/0/19', 'TenGigabitEthernet1/0/20'])
        self.assertEqual(result, None)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'cdp run',
                'interface TenGigabitEthernet1/0/19',
                'cdp enable',
                'interface TenGigabitEthernet1/0/20',
                'cdp enable'
            ],)
        )