import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.utils import clear_ip_ospf_rib


class TestClearIpOspfRib(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          isr4k-router-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: isr4k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['isr4k-router-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ip_ospf_rib(self):
        result = clear_ip_ospf_rib(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
