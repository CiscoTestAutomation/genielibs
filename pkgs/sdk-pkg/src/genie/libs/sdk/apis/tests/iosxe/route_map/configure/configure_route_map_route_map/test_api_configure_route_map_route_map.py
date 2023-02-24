import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.route_map.configure import configure_route_map_route_map


class TestConfigureRouteMapRouteMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_route_map_route_map(self):
        result = configure_route_map_route_map(self.device, [{'continue_id': '20',
  'local_preference': '500',
  'match_as_path': '12',
  'route_map': 'internal',
  'seq': '10',
  'set_as_path_prepend': '45000',
  'set_metric': '30',
  'set_weight': '100'}])
        expected_output = None
        self.assertEqual(result, expected_output)
