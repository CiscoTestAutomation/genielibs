import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import remove_port_channel_interface


class TestRemovePortChannelInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ECR:
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
        self.device = self.testbed.devices['ECR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_remove_port_channel_interface(self):
        result = remove_port_channel_interface(self.device, 23)
        expected_output = None
        self.assertEqual(result, expected_output)
