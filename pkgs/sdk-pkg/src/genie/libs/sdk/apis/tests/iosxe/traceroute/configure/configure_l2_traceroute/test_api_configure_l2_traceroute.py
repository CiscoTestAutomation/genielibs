import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.traceroute.configure import configure_l2_traceroute


class TestConfigureL2Traceroute(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9200_STK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9200_STK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_l2_traceroute(self):
        result = configure_l2_traceroute(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
