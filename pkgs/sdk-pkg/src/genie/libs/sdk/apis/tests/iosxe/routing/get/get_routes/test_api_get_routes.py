import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_routes


class TestGetRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_routes(self):
        result = get_routes(self.device)
        expected_output = ['1.1.1.2/32',
 '1.1.1.3/32',
 '1.1.1.4/32',
 '1.1.1.5/32',
 '1.1.1.6/32',
 '1.1.1.7/32',
 '1.1.1.8/32',
 '1.1.1.9/32',
 '99.2.3.0/24',
 '99.2.3.3/32',
 '99.2.4.0/24',
 '99.2.5.0/24',
 '99.3.4.0/24',
 '99.3.4.3/32',
 '99.3.5.0/24',
 '99.3.5.3/32',
 '99.4.5.0/24',
 '99.4.6.0/24',
 '99.4.7.0/24',
 '99.5.6.0/24',
 '99.5.7.0/24',
 '99.6.7.0/24',
 '99.6.8.0/24',
 '99.6.9.0/24',
 '99.7.8.0/24',
 '99.7.9.0/24',
 '99.8.9.0/24',
 '100.2.3.0/24',
 '100.2.3.3/32',
 '100.2.4.0/24',
 '100.2.5.0/24',
 '100.3.4.0/24',
 '100.3.4.3/32',
 '100.3.5.0/24',
 '100.3.5.3/32',
 '100.4.5.0/24',
 '100.4.6.0/24',
 '100.4.7.0/24',
 '100.5.6.0/24',
 '100.5.7.0/24',
 '100.6.7.0/24',
 '100.6.8.0/24',
 '100.6.9.0/24',
 '100.7.8.0/24',
 '100.7.9.0/24',
 '100.8.9.0/24',
 '200.2.0.0/24',
 '200.2.0.2/32']
        self.assertEqual(result, expected_output)
