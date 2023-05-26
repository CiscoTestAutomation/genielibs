import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.verify import verify_flood_suppress


class TestVerifyFloodSuppress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Leaf-01:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Leaf-01']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_flood_suppress(self):
        result = verify_flood_suppress(self.device, '201')
        expected_output = True
        self.assertEqual(result, expected_output)
