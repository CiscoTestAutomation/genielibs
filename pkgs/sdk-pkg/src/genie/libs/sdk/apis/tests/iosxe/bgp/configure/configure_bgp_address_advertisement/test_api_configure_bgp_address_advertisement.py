import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_address_advertisement


class TestConfigureBgpAddressAdvertisement(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE-B:
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
        self.device = self.testbed.devices['PE-B']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_address_advertisement(self):
        result = configure_bgp_address_advertisement(self.device, '65004', 'ipv4', '1.1.1.1', '255.255.255.255', 'WAN-VRF')
        expected_output = None
        self.assertEqual(result, expected_output)
