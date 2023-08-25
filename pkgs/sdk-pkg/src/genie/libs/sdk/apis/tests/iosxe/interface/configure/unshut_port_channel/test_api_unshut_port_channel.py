import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unshut_port_channel


class TestUnshutPortChannel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-9500-Dist3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-9500-Dist3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unshut_port_channel(self):
        result = unshut_port_channel(self.device, '15')
        expected_output = None
        self.assertEqual(result, expected_output)
