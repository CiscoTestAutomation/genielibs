import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.get import get_policy_map_interface_queue_output


class TestGetPolicyMapInterfaceQueueOutput(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          NGSVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['NGSVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_policy_map_interface_queue_output(self):
        result = get_policy_map_interface_queue_output(self.device, 'HundredGigE1/0/13.1')
        expected_output = {'HundredGigE1/0/13.1': {'service_policy': {'output': {'policy_name': {'hqos': {'class_map': {'class-default': {'bytes_output': 0,
                                                                                                                'match': ['any'],
                                                                                                                'match_evaluation': 'match-any',
                                                                                                                'packets': 5017,
                                                                                                                'queue_limit_bytes': 7500000,
                                                                                                                'queueing': True,
                                                                                                                'shape_bc_bps': 40000000,
                                                                                                                'shape_be_bps': 40000000,
                                                                                                                'shape_cir_bps': 10000000000,
                                                                                                                'shape_type': 'average',
                                                                                                                'target_shape_rate': 10000000000,
                                                                                                                'total_drops': 0}}}}},
                                            'output1': {'policy_name': {'policy2': {'class_map': {'class-default': {'bytes_output': 0,
                                                                                                                    'match': ['any'],
                                                                                                                    'match_evaluation': 'match-any',
                                                                                                                    'packets': 5017,
                                                                                                                    'queue_limit_bytes': 7500000,
                                                                                                                    'total_drops': 0},
                                                                                                  'tc7': {'bytes_output': 0,
                                                                                                          'match': ['traffic-class '
                                                                                                                    '7'],
                                                                                                          'match_evaluation': 'match-all',
                                                                                                          'packets': 0,
                                                                                                          'queue_limit_bytes': 7500000,
                                                                                                          'queueing': True,
                                                                                                          'shape_bc_bps': 16000000,
                                                                                                          'shape_be_bps': 16000000,
                                                                                                          'shape_cir_bps': 4000000000,
                                                                                                          'shape_type': 'average',
                                                                                                          'target_shape_rate': 4000000000,
                                                                                                          'total_drops': 0}}}}}}}}
        self.assertEqual(result, expected_output)
