import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_commands


class TestUnconfigureAaaAccountingCommands(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          startrek-bgl-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: STARTREK
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-bgl-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_aaa_accounting_commands(self):
        result = unconfigure_aaa_accounting_commands(self.device, '15', 'test', 'none', '', None)
        expected_output = None
        self.assertEqual(result, expected_output)
