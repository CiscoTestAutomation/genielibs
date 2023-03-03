import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_shape_map


class TestConfigureShapeMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Startek:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_shape_map(self):
        result = configure_shape_map(
            self.device, 
            'queue1', 
            [{
                'bandwidth': '20',
                'child_policy': 'queue2',
                'class_map_name': 'tc7',
                'priority_level': 1,
                'queue_limit': '30',
                'shape_average': '2000000000'
            }],
            'no service-policy')
        expected_output = None
        self.assertEqual(result, expected_output)
