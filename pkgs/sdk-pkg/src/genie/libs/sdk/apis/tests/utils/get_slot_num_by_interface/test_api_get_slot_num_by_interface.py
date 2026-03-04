from unittest import TestCase
from genie.libs.sdk.apis.utils import get_slot_num_by_interface


class TestGetSlotNumByInterface(TestCase):

    def test_get_slot_num_by_interface(self):
        interface = 'GigabitEthernet0/1/2'
        result = get_slot_num_by_interface(interface)
        self.assertEqual(result, '0/1')

        interface = 'GigabitEthernet'
        result = get_slot_num_by_interface(interface)
        self.assertEqual(result, None)

        interface = '0/2/1'
        result = get_slot_num_by_interface(interface)
        self.assertEqual(result, '0/2')
        

        
