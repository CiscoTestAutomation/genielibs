import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_redistribute_connected


class TestConfigureRedistributeConnected(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IR1101:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IR1101']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_redistribute_connected(self):
        result = configure_redistribute_connected(self.device, 1, 'ipv4', None, 'rm-adv-loopback')
        expected_output = None
        self.assertEqual(result, expected_output)
