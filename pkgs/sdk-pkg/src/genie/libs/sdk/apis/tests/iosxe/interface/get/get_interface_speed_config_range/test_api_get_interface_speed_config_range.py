from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_speed_config_range
from unittest.mock import Mock


class TestGetInterfaceSpeedConfigRange(TestCase):

    def test_get_interface_speed_config_range(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.api.question_mark_retrieve = Mock(return_value='''conf t
                                                                      Enter configuration commands, one per line.  End with CNTL/Z.
                                                                      whitneyx_09(config)#interface GigabitEthernet0/1/0
                                                                      whitneyx_09(config-if)#speed ?
                                                                        10    Force 10 Mbps operation
                                                                        100   Force 100 Mbps operation
                                                                        1000  Force 1000 Mbps operation
                                                                        auto  Enable AUTO speed configuration
                                                                      
                                                                      whitneyx_09(config-if)#speed
                                                                      whitneyx_09#''')
        expected_output = ['10', '100', '1000', 'auto']
        actual_output = get_interface_speed_config_range(self.device, 'GigabitEthernet0/1/0')
        self.assertEqual(actual_output, expected_output)
