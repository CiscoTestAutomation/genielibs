import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.configure import unconfigure_netconf_yang


class TestUnconfigureNetconfYang(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
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
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_netconf_yang(self):
        result = unconfigure_netconf_yang(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
