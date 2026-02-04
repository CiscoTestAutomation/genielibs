from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_type_name


class TestGetSlotNumByInterface(TestCase):

    def test_get_interface_type_name(self):
        interface = 'GigabitEthernet0/0/0'
        result = get_interface_type_name(interface)
        self.assertEqual(result, 'GigabitEthernet')

        interface = 'GigabitEthernet'
        result = get_interface_type_name(interface)
        self.assertEqual(result, None)

        interface = '0/0/0'
        result = get_interface_type_name(interface)
        self.assertEqual(result, None)
        

        
