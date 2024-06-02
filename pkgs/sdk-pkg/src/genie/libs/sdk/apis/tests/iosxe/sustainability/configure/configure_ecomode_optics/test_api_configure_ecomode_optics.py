import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sustainability.configure import configure_ecomode_optics


class TestConfigureEcomodeOptics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Peer1-topo1-ott:
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
        self.device = self.testbed.devices['Peer1-topo1-ott']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ecomode_optics(self):
        result = configure_ecomode_optics(self.device, '1')
        expected_output = None
        self.assertEqual(result, expected_output)
