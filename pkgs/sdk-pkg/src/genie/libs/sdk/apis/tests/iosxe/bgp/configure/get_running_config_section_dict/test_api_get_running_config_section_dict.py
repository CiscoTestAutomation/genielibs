from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import get_running_config_section_dict

class TestGetRunningConfigSectionDict(TestCase):

    def test_get_running_config_section_dict(self):
        device = Mock()
        device.execute.return_value = '''
        Building configuration...
        Current configuration : 8848 bytes
        aaa new-model
        boot system bootflash:ir1101-universalk9.2024-08-19_16.16_flian.SSA.bin
        bridge-domain 12
         member Vlan12 service-instance 12
         member evpn-instance profile evpn_va
        '''
        expected_output = {
            'Building configuration...': {},
            'Current configuration : 8848 bytes': {},
            'aaa new-model': {},
            'boot system bootflash:ir1101-universalk9.2024-08-19_16.16_flian.SSA.bin': {},
            'bridge-domain 12': {
                'member Vlan12 service-instance 12': {},
                'member evpn-instance profile evpn_va': {}
            }
        }
        result = get_running_config_section_dict(device)
        self.assertEqual(result, expected_output)