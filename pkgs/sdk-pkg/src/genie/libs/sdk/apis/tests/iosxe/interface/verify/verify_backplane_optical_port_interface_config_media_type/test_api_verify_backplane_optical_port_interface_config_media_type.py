from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.verify import verify_backplane_optical_port_interface_config_media_type
from unittest.mock import Mock


class TestVerifyBackplaneOpticalPortInterfaceConfigMediaType(TestCase):

    def test_verify_backplane_optical_port_interface_config_media_type(self):
        self.device = Mock()
        results_map = {
            'show run interface TenGigabitEthernet1/2': 'Building configuration...\nCurrent configuration : 61 bytes\n!\ninterface TenGigabitEthernet1/2\n media-type backplane\nend',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = verify_backplane_optical_port_interface_config_media_type(self.device, 'TenGigabitEthernet1/2', 'backplane', 60, 10, True)
        self.assertIn(
            'show run interface TenGigabitEthernet1/2',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = True
        self.assertEqual(result, expected_output)


