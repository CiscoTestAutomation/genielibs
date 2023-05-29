import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_mdt_auto_discovery_inter_as


class TestConfigureMdtAutoDiscoveryInterAs(unittest.TestCase):

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
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mdt_auto_discovery_inter_as(self):
        result = configure_mdt_auto_discovery_inter_as(self.device, 'green', 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)
