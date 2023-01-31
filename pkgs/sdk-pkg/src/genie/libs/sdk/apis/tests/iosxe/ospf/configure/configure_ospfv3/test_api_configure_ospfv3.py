import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3


class TestConfigureOspfv3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          UUT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['UUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ospfv3(self):
        result = configure_ospfv3(self.device, '1', '1.1.1.1', None, True, True, 'ipv4', None, None, None, True, 'connected', 0, 1)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ospfv3_1(self):
        result = configure_ospfv3(self.device, '1', '1.1.1.1', None, True, True, 'ipv4', None, 'unicast', None, True, 'connected', 1, 1)
        expected_output = None
        self.assertEqual(result, expected_output)
