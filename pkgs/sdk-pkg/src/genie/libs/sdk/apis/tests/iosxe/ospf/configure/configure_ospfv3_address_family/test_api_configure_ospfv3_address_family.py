import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_address_family


class TestConfigureOspfv3AddressFamily(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ACE:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ASR1K
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ACE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ospfv3_address_family(self):
        result = configure_ospfv3_address_family(self.device, 1, 'ipv6', 'unicast', 'connected')
        expected_output = None
        self.assertEqual(result, expected_output)
