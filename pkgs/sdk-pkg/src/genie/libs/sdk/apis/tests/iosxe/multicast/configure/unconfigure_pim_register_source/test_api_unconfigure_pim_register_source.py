import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_pim_register_source


class TestUnconfigurePimRegisterSource(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SG_HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500h
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SG_HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_pim_register_source(self):
        result = unconfigure_pim_register_source(self.device, 'Loopback101', 'red', False)
        expected_output = None
        self.assertEqual(result, expected_output)
