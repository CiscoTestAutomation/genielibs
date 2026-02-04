import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.verify import verify_subslot_state
from unittest.mock import Mock


class TestVerifySubslotState(TestCase):

    def test_verify_subslot_state(self):
        self.device = Mock()
        self.device.name = 'TestDevice'
        self.device.parse = Mock(return_value={
            'subslots': {
            		'0/0': {
            			'model': '8x1G-8x10G-4x25G',
            			'operational_status': 'ok'
            		}
            	}
        })
        expected_output = True
        actual_output = verify_subslot_state(self.device, '0/0', 'ok', 120, 10)
        self.assertEqual(actual_output, expected_output)
