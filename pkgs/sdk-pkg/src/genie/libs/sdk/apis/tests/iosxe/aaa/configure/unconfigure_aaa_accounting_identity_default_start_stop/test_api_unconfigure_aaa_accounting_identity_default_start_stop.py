import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_accounting_identity_default_start_stop


class TestUnconfigureAaaAccountingIdentityDefaultStartStop(unittest.TestCase):

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
            platform: c9500L
            type: c9500L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_aaa_accounting_identity_default_start_stop(self):
        result = unconfigure_aaa_accounting_identity_default_start_stop(self.device, 'group', 'My-Radius')
        expected_output = None
        self.assertEqual(result, expected_output)
