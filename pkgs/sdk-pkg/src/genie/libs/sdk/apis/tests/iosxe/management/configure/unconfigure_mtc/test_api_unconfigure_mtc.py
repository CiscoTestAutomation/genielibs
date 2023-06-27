import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.management.configure import unconfigure_mtc


class TestUnconfigureMtc(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SKYFOX-DUT3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C9500
            type: C9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SKYFOX-DUT3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_mtc(self):
        result = unconfigure_mtc(self.device, 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)
